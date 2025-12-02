"""
API Dependencies module.
Common dependencies for API endpoints.
"""

from typing import Generator
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Yields a session and ensures it's closed after use.

    Usage:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication dependencies will be added in Phase 4
# - get_current_user
# - get_current_active_user
# - get_current_admin
# - get_current_editor
