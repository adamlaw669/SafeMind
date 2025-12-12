from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_token
from app.models.report import Report

router = APIRouter(prefix="/api/reports", tags=["reports"])

def get_auth_header():
    return None

@router.post("/")
def create_report(report_data: dict, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not report_data.get("text") or report_data["text"].strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty"
        )
    
    token = authorization.replace("Bearer ", "")
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    report = Report(
        user_id=int(user_id),
        text=report_data["text"],
        location=report_data.get("location", "")
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"id": report.id, "text": report.text, "location": report.location}

@router.get("/{report_id}")
def get_report(report_id: int, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return report

@router.get("/user/{user_id}")
def list_user_reports(user_id: int, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    return reports

@router.delete("/{report_id}")
def delete_report(report_id: int, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(report)
    db.commit()
    return {"message": "Deleted"}

@router.post("/emergency/alert")
def emergency_alert(alert_data: dict, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = authorization.replace("Bearer ", "")
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    report = Report(
        user_id=int(user_id),
        text=alert_data["text"],
        location=alert_data.get("location", ""),
        is_emergency=True
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"id": report.id, "message": "Emergency alert created"}
