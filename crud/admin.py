"""CRUD operations for administrator"""

from sqlmodel import Session, select
from fastapi import HTTPException
from utils.authentication import hash_password
from models.admin import Administrator
from models.superuser import Superuser


def create_administrator(session: Session, new_administrator: Administrator) -> Administrator:
    """Creates new administrator"""
    db_administrator = Administrator(**new_administrator.model_dump())
    is_existing = session.exec(select(Administrator).where(Administrator.username == db_administrator.username)).first()
    if is_existing:
        raise HTTPException(status_code=403, detail="Administrator already exists.")
    db_administrator.password = hash_password(db_administrator.password)
    session.add(db_administrator)
    session.commit()
    session.refresh(db_administrator)

    if db_administrator.is_superuser:
        new_superuser = Superuser(
            name=db_administrator.name,
            username=db_administrator.username,
            password=db_administrator.password,
            admin_id=db_administrator.id,
        )
        session.add(new_superuser)
        session.commit()
        session.refresh(new_superuser)

    return db_administrator


def update_administrator(session: Session, id: int, updated_administrator: Administrator) -> Administrator:
    """Updates existing administrator"""
    to_be_updated = session.exec(select(Administrator).where(Administrator.id == id)).first()
    if to_be_updated:
        updated_data = updated_administrator.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(to_be_updated, key, value)
    else:
        raise HTTPException(status_code=404, detail="Administrator not found.")

    session.commit()
    session.refresh(to_be_updated)

    return to_be_updated


def read_all(session: Session) -> list[Administrator]:
    """Reads all the stored administrator"""
    return session.exec(select(Administrator)).all()


def read_by_id(session: Session, id: int) -> Administrator:
    """Read Administrator by id"""
    to_be_read = session.exec(select(Administrator).where(Administrator.id == id)).first()
    if to_be_read:
        return to_be_read
    raise HTTPException(status_code=404, detail="Administrator not found.")


def delete_by_id(session: Session, id: int) -> Administrator:
    """Deletes Administrator"""
    to_be_deleted = session.exec(select(Administrator).where(Administrator.id == id)).first()
    if to_be_deleted:
        session.delete(to_be_deleted)
        session.commit()
        return to_be_deleted
    raise HTTPException(status_code=404, detail="Administrator not found.")
