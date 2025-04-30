"""CRUD operations for superuser"""

from sqlmodel import Session, select
from fastapi import HTTPException
from utils.authentication import hash_password
from models.superuser import Superuser


def create_superuser(session: Session, new_superuser: Superuser) -> Superuser:
    """Creates new superusers"""
    db_superuser = Superuser(**new_superuser.model_dump())
    is_existing = session.exec(select(Superuser).where(Superuser.username == db_superuser.username)).first()
    if is_existing:
        raise HTTPException(status_code=403, detail="Superuser already exists.")
    db_superuser.password = hash_password(db_superuser.password)
    session.add(db_superuser)
    session.commit()
    session.refresh(db_superuser)

    return db_superuser


def read_all(session: Session) -> list[Superuser]:
    """Reads all superusers stored"""
    return session.exec(select(Superuser)).all()


def read_by_id(session: Session, id: int) -> Superuser:
    """Reads superuser by id"""
    to_be_read = session.exec(select(Superuser).where(Superuser.id == id)).first()
    if to_be_read:
        return to_be_read
    raise HTTPException(status_code=404, detail="Superuser not found.")


def update_superuser(session: Session, updated_superuser: Superuser, id: int) -> Superuser:
    """Updates existing superuser"""
    to_be_updated = session.exec(select(Superuser).where(Superuser.id == id)).first()

    if to_be_updated:
        updated_data = updated_superuser.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(to_be_updated, key, value)
    else:
        raise HTTPException(status_code=404, detail="Superuser not found.")

    session.commit()
    session.refresh(to_be_updated)
    return to_be_updated


def delete_superuser(session: Session, id: int) -> Superuser:
    """Deletes given superuser"""
    to_be_deleted = session.exec(select(Superuser).where(Superuser.id == id)).first()
    if to_be_deleted:
        session.delete(to_be_deleted)
        session.commit()
        return to_be_deleted
    raise HTTPException(status_code=404, detail="Superuser not found.")
