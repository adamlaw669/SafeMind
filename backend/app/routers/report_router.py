from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.security import get_current_user
from app.schemas.user_schema import UserOut
from app.schemas.report_schema import ReportCreate, ReportResponse
from app.crud import report_crud

# This is the object main.py is looking for
router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Create a new standard report.
    """
    return report_crud.create_report(db=db, report=report_in, user_id=current_user.id)

@router.get("/", response_model=List[ReportResponse])
def read_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Retrieve all reports.
    """
    return report_crud.get_reports(db, skip=skip, limit=limit)

@router.get("/{report_id}", response_model=ReportResponse)
def read_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Get a specific report by ID.
    """
    report = report_crud.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report