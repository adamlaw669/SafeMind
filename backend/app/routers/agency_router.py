import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user_schema import UserOut
from app.schemas.emergency_schema import EmergencyReportResponse
from app.schemas.agency_schema import AgencyResponse, AgencyUpdateRequest, AgentActionResponse
from app.models.emergency import EmergencyReport
from app.models.agency import Agency
from app.core.dependencies import get_current_user
from app.crud import report_crud, agency_crud
from app.services import log_service
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/reports", response_model=List[EmergencyReportResponse])
async def get_agency_emergency_reports(
    skip: int = 0,
    limit: int = 50,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[EmergencyReportResponse]:
    """
    List all emergency reports visible to the agency, sorted by newest first.
    
    Pagination supported via skip and limit parameters.
    Only accessible by agency personnel.
    """
    # Authorization check: user must be part of an agency
    if not current_user.agency_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agency personnel can access reports"
        )
    
    # Validate pagination parameters
    skip = max(0, skip)
    limit = min(100, max(1, limit))
    
    try:
        # Get all reports for the agency, sorted by newest first
        reports = db.query(EmergencyReport).filter(
            EmergencyReport.user.has(agency_id=current_user.agency_id)
        ).order_by(
            EmergencyReport.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        logger.info(
            f"Agency {current_user.agency_id} retrieved {len(reports)} emergency reports "
            f"(skip={skip}, limit={limit})"
        )
        
        return [EmergencyReportResponse.model_validate(report) for report in reports]
        
    except Exception as e:
        logger.error(f"Error retrieving agency reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reports"
        )


@router.patch("/report/{report_id}/status", response_model=EmergencyReportResponse)
async def update_report_status(
    report_id: int,
    request: AgencyUpdateRequest,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EmergencyReportResponse:
    """
    Update emergency report status.
    
    Valid statuses: PENDING, IN_PROGRESS, RESOLVED, ESCALATED
    Logs the action for audit trail.
    """
    # Authorization check
    if not current_user.agency_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agency personnel can update reports"
        )
    
    if report_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )
    
    # Validate status value
    valid_statuses = ["PENDING", "IN_PROGRESS", "RESOLVED", "ESCALATED"]
    if request.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    try:
        # Retrieve report
        report = report_crud.get_report(db=db, report_id=report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Emergency report not found"
            )
        
        # Verify agency ownership
        if report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this report"
            )
        
        # Store old status for logging
        old_status = report.status
        
        # Update status
        report.status = request.status
        db.commit()
        db.refresh(report)
        
        # Log the action
        await log_service.log_status_change(
            agent_id=current_user.id,
            report_id=report_id,
            old_status=old_status,
            new_status=request.status,
            db=db
        )
        
        logger.info(
            f"Report {report_id} status updated from {old_status} to {request.status} "
            f"by user {current_user.id}"
        )
        
        return EmergencyReportResponse.model_validate(report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating report status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update report status"
        )


@router.post("/respond/{report_id}", response_model=AgentActionResponse)
async def respond_to_emergency(
    report_id: int,
    request: AgencyUpdateRequest,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AgentActionResponse:
    """
    Agency responds to an emergency report (mark as handled, escalated, etc).
    
    Response types: HANDLED, ESCALATED, IN_PROGRESS
    Creates comprehensive log entry and updates report status.
    """
    # Authorization check
    if not current_user.agency_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agency personnel can respond to reports"
        )
    
    if report_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )
    
    # Validate response type
    valid_response_types = ["HANDLED", "ESCALATED", "IN_PROGRESS"]
    if request.status not in valid_response_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid response type. Must be one of: {', '.join(valid_response_types)}"
        )
    
    try:
        # Retrieve report
        report = report_crud.get_report(db=db, report_id=report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Emergency report not found"
            )
        
        # Verify agency ownership
        if report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to respond to this report"
            )
        
        # Map response type to report status
        response_to_status_map = {
            "HANDLED": "RESOLVED",
            "ESCALATED": "ESCALATED",
            "IN_PROGRESS": "IN_PROGRESS"
        }
        
        new_status = response_to_status_map.get(request.status, "IN_PROGRESS")
        old_status = report.status
        
        # Update report
        report.status = new_status
        report.handled_at = db.func.now()
        report.handled_by_user_id = current_user.id
        
        db.commit()
        db.refresh(report)
        
        # Log the response action
        await log_service.log_report_response(
            agent_id=current_user.id,
            report_id=report_id,
            response_type=request.status,
            notes=request.notes,
            db=db
        )
        
        logger.info(
            f"Emergency report {report_id} responded to by user {current_user.id} "
            f"with response type: {request.status}"
        )
        
        return AgentActionResponse(
            success=True,
            message=f"Report {request.status.lower()} successfully",
            report_id=report_id,
            new_status=new_status,
            action_type=request.status,
            timestamp=report.handled_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error responding to emergency: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to respond to emergency"
        )


@router.get("/info", response_model=AgencyResponse)
async def get_agency_info(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AgencyResponse:
    """
    Get current agency information for authenticated user.
    """
    if not current_user.agency_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not part of an agency"
        )
    
    try:
        agency = agency_crud.get_agency(db=db, agency_id=current_user.agency_id)
        
        if not agency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found"
            )
        
        return AgencyResponse.model_validate(agency)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving agency info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agency information"
        )


@router.get("/")
async def list_agencies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all agencies."""
    return {"agencies": []}

@router.get("/{agency_id}")
async def get_agency(
    agency_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific agency."""
    return {"id": agency_id, "name": "Agency"}
