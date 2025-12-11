import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.emergency_schema import EmergencyReportCreate, EmergencyReportResponse
from app.models.emergency import EmergencyReport
from app.schemas.user_schema import UserOut
from app.core.security import get_current_user
from app.crud import report_crud
from app.services.emergency_service import process_emergency_report

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", response_model=EmergencyReportResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency_report(
    report_data: EmergencyReportCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EmergencyReportResponse:
    """
    Create a new emergency report.
    
    - Mark as critical (is_critical=True)
    - Trigger NLP analysis
    - Broadcast via WebSocket
    - Send notifications
    - Schedule follow-ups
    """
    try:
        # Validate input
        if not report_data.description or len(report_data.description.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description cannot be empty"
            )
        
        # Create emergency report via CRUD
        db_report = report_crud.create_emergency_report(
            db=db,
            user_id=current_user.id,
            description=report_data.description,
            location=report_data.location,
            is_critical=True
        )
        
        logger.info(f"Emergency report {db_report.id} created by user {current_user.id}")
        
        # Process report asynchronously (NLP, notifications, WebSocket, follow-up)
        await process_emergency_report(db_report, db)
        
        # Refresh to get updated data
        db.refresh(db_report)
        
        return EmergencyReportResponse.model_validate(db_report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating emergency report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create emergency report"
        )


@router.get("/{report_id}", response_model=EmergencyReportResponse)
async def get_emergency_report(
    report_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EmergencyReportResponse:
    """
    Get a specific emergency report by ID.
    
    Only the report owner or authorized agency personnel can access.
    """
    if report_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )
    
    report = report_crud.get_report(db=db, report_id=report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency report not found"
        )
    
    # Authorization check: user must be report owner or from same agency
    if report.user_id != current_user.id and report.user.agency_id != current_user.agency_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this report"
        )
    
    logger.info(f"Emergency report {report_id} retrieved by user {current_user.id}")
    
    return EmergencyReportResponse.model_validate(report)


@router.get("/user/{user_id}", response_model=list[EmergencyReportResponse])
async def get_user_emergency_reports(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[EmergencyReportResponse]:
    """
    Get all emergency reports for a specific user.
    
    Pagination supported via skip and limit parameters.
    Only the user or authorized agency personnel can access.
    """
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    # Authorization check
    if user_id != current_user.id and current_user.agency_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these reports"
        )
    
    # Validate pagination
    skip = max(0, skip)
    limit = min(100, max(1, limit))
    
    reports = report_crud.get_reports_by_user(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    
    logger.info(f"Retrieved {len(reports)} emergency reports for user {user_id}")
    
    return [EmergencyReportResponse.model_validate(report) for report in reports]
