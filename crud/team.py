"""CRUD operations for Team Table"""

from sqlmodel import Session, select
from fastapi import HTTPException
from models.team import Team


def create_team(session: Session, team: Team) -> Team:
    """Creates new cricketer"""
    db_team = Team(**team.model_dump())
    is_existing = session.exec(select(Team).where(Team.name == db_team.name)).first()
    if is_existing:
        raise HTTPException(status_code=403, detail="Team already exists.")
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def get_teams(session: Session) -> list[Team]:
    """Gets all cricketers"""
    return session.exec(select(Team)).all()


def get_team_by_id(session: Session, team_id: int) -> Team | None:
    """Get cricketer by id"""
    return session.get(Team, team_id)


def delete_team(session: Session, team_id: int) -> Team | None:
    """Delete's specified criketer"""
    team = session.get(Team, team_id)
    if team:
        session.delete(team)
        session.commit()
    return team
