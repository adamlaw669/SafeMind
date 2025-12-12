from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.base import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/")
async def create_report(
    text: str,
    location: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new report."""
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report text cannot be empty"
        )
    
    # Import here to avoid circular imports
    from app.models.report import Report
    
    report = Report(
        user_id=current_user.id,
        text=text,
        location=location,
        created_at=datetime.utcnow()
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return {
        "id": report.id,
        "user_id": report.user_id,
        "text": report.text,
        "location": report.location,
        "created_at": report.created_at
    }

@router.get("/{report_id}")
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific report."""
    from app.models.report import Report
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return {
        "id": report.id,
        "user_id": report.user_id,
        "text": report.text,
        "location": report.location,
        "created_at": report.created_at
    }

@router.get("/user/{user_id}")
async def list_user_reports(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all reports for a user."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' reports"
        )
    
    from app.models.report import Report
    
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "text": r.text,
            "location": r.location,
            "created_at": r.created_at
        }
        for r in reports
    ]

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a report."""
    from app.models.report import Report
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other users' reports"
        )
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}