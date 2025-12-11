from sqlalchemy.orm import Session
from app.models.agency import Agency
from app.schemas.agency_schema import AgencyCreate, AgencyUpdateRequest

def create_agency(db: Session, data: AgencyCreate) -> Agency:
    new_agency = Agency(
        name=data.name,
        contact_email=data.contact_email,
        phone=data.phone,
        location=data.location,
        is_verified=False,
        is_active=True
    )
    db.add(new_agency)
    db.commit()
    db.refresh(new_agency)
    return new_agency


def get_agency_by_id(db: Session, agency_id: int) -> Agency | None:
    return db.query(Agency).filter(Agency.id == agency_id).first()


def list_agencies(db: Session):
    return db.query(Agency).all()


def update_agency(db: Session, agency: Agency, data: AgencyUpdateRequest) -> Agency:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(agency, field, value)
    db.commit()
    db.refresh(agency)
    return agency


def verify_agency(db: Session, agency: Agency) -> Agency:
    agency.is_verified = True
    db.commit()
    db.refresh(agency)
    return agency


def deactivate_agency(db: Session, agency: Agency) -> Agency:
    agency.is_active = False
    db.commit()
    db.refresh(agency)
    return agency
