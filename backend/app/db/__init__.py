from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.base import SessionLocal, Base, engine

__all__ = ["Base", "engine", "get_db"]


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
