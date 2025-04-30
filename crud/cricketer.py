"""CRUD operations for Cricketer Table"""

from sqlmodel import Session, select
from fastapi import HTTPException
from models.cricketer import Cricketer
from models.team import Team


def create_cricketer(session: Session, cricketer: Cricketer) -> Cricketer:
    """Creates new cricketer"""
    db_cricketer = Cricketer(**cricketer.model_dump())
    is_existing = session.exec(select(Cricketer).where(Cricketer.name == db_cricketer.name)).first()
    if is_existing:
        raise HTTPException(status_code=403, detail="Match performance already exists.")
    cricketer_team_id = session.exec(select(Team).where(Team.id == cricketer.team_id)).first()
    if not cricketer_team_id:
        raise HTTPException(status_code=404, detail="Team does not exist.")
    session.add(db_cricketer)
    session.commit()
    session.refresh(db_cricketer)
    return db_cricketer


def get_cricketers(session: Session) -> list[Cricketer]:
    """Gets all cricketers"""
    return session.exec(select(Cricketer)).all()


def get_cricketer_by_id(session: Session, cricketer_id: int) -> Cricketer | None:
    """Get cricketer by id"""
    return session.get(Cricketer, cricketer_id)


def delete_cricketer(session: Session, cricketer_id: int) -> Cricketer:
    """Delete's specified criketer"""
    cricketer = session.get(Cricketer, cricketer_id)
    if cricketer:
        session.delete(cricketer)
        session.commit()
    return cricketer
