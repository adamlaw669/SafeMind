import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user_schema import UserOut
from app.schemas.followup_schema import FollowupRequest, FollowupResponse, FollowupCheckinRequest
from app.models.followup import FollowUp
from app.models.emergency import EmergencyReport
from app.core.security import get_current_user
from app.crud import followup_crud, report_crud
from app.services import followup_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{report_id}/schedule", response_model=FollowupResponse, status_code=status.HTTP_201_CREATED)
async def schedule_followup(
    report_id: int,
    request: FollowupRequest,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FollowupResponse:
    """
    Schedule a follow-up check-in for an emergency report.
    
    - Validates report exists
    - Authorizes user (must be report owner or agency personnel)
    - Calls followup_service to schedule
    - Returns created follow-up
    """
    if report_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )
    
    if not request.hours or request.hours <= 0 or request.hours > 720:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hours must be between 1 and 720 (30 days)"
        )
    
    try:
        # Validate report exists
        report = report_crud.get_report(db=db, report_id=report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Emergency report not found"
            )
        
        # Authorization: user must be report owner or from same agency
        if report.user_id != current_user.id and report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to schedule follow-up for this report"
            )
        
        # Schedule follow-up via service
        follow_up = await followup_service.schedule_checkin(
            report_id=report_id,
            hours=request.hours,
            db=db,
            notes=request.notes
        )
        
        logger.info(
            f"Follow-up scheduled for report {report_id} by user {current_user.id} "
            f"in {request.hours} hours"
        )
        
        return FollowupResponse.model_validate(follow_up)
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error scheduling follow-up: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule follow-up"
        )


@router.get("/{report_id}", response_model=List[FollowupResponse])
async def get_report_followups(
    report_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[FollowupResponse]:
    """
    Get all follow-ups for a specific emergency report.
    
    Pagination supported via skip and limit.
    Only report owner or agency personnel can access.
    """
    if report_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )
    
    skip = max(0, skip)
    limit = min(100, max(1, limit))
    
    try:
        # Validate report exists
        report = report_crud.get_report(db=db, report_id=report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Emergency report not found"
            )
        
        # Authorization check
        if report.user_id != current_user.id and report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view follow-ups for this report"
            )
        
        # Retrieve follow-ups
        follow_ups = followup_crud.get_followups_by_report(
            db=db,
            report_id=report_id,
            skip=skip,
            limit=limit
        )
        
        logger.info(
            f"Retrieved {len(follow_ups)} follow-ups for report {report_id} by user {current_user.id}"
        )
        
        return [FollowupResponse.model_validate(fu) for fu in follow_ups]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report follow-ups: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve follow-ups"
        )


@router.get("/user/pending", response_model=List[FollowupResponse])
async def get_user_pending_followups(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[FollowupResponse]:
    """
    Get all pending follow-ups for the current user.
    
    Returns follow-ups that are due or overdue.
    """
    try:
        follow_ups = await followup_service.get_pending_followups_for_user(
            user_id=current_user.id,
            db=db
        )
        
        logger.info(f"Retrieved {len(follow_ups)} pending follow-ups for user {current_user.id}")
        
        return [FollowupResponse.model_validate(fu) for fu in follow_ups]
        
    except Exception as e:
        logger.error(f"Error retrieving pending follow-ups: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pending follow-ups"
        )


@router.post("/checkin", response_model=FollowupResponse)
async def submit_followup_checkin(
    request: FollowupCheckinRequest,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FollowupResponse:
    """
    Submit a check-in response to a follow-up.
    
    - User responds to how they're doing
    - Updates follow-up status to COMPLETED
    - Evaluates response for crisis indicators
    - May trigger escalation if needed
    - Broadcasts update to agencies
    """
    if request.followup_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid follow-up ID"
        )
    
    if not request.response or len(request.response.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response cannot be empty"
        )
    
    if len(request.response) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response cannot exceed 1000 characters"
        )
    
    try:
        # Process check-in via service
        follow_up = await followup_service.process_checkin(
            follow_up_id=request.followup_id,
            user_id=current_user.id,
            response=request.response,
            db=db
        )
        
        logger.info(
            f"Follow-up check-in submitted for follow-up {request.followup_id} "
            f"by user {current_user.id}"
        )
        
        return FollowupResponse.model_validate(follow_up)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing follow-up check-in: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process check-in"
        )


@router.get("/{followup_id}", response_model=FollowupResponse)
async def get_followup(
    followup_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FollowupResponse:
    """
    Get a specific follow-up by ID.
    
    Only the user who owns the follow-up or agency personnel can access.
    """
    if followup_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid follow-up ID"
        )
    
    try:
        follow_up = followup_crud.get_followup(db=db, followup_id=followup_id)
        
        if not follow_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow-up not found"
            )
        
        # Authorization check
        report = follow_up.emergency_report
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associated report not found"
            )
        
        if follow_up.user_id != current_user.id and report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this follow-up"
            )
        
        logger.info(f"Follow-up {followup_id} retrieved by user {current_user.id}")
        
        return FollowupResponse.model_validate(follow_up)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving follow-up: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve follow-up"
        )


@router.patch("/{followup_id}/cancel")
async def cancel_followup(
    followup_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending follow-up.
    
    Only the user who owns the follow-up or agency can cancel.
    """
    if followup_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid follow-up ID"
        )
    
    try:
        follow_up = followup_crud.get_followup(db=db, followup_id=followup_id)
        
        if not follow_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow-up not found"
            )
        
        # Authorization check
        report = follow_up.emergency_report
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associated report not found"
            )
        
        if follow_up.user_id != current_user.id and report.user.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this follow-up"
            )
        
        # Cannot cancel if already completed
        if follow_up.status == "COMPLETED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel a completed follow-up"
            )
        
        # Update status
        follow_up.status = "CANCELLED"
        follow_up.completed_at = db.func.now()
        db.commit()
        db.refresh(follow_up)
        
        logger.info(f"Follow-up {followup_id} cancelled by user {current_user.id}")
        
        return {
            "success": True,
            "message": "Follow-up cancelled successfully",
            "followup_id": followup_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling follow-up: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel follow-up"
        )
