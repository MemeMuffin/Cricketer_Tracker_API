"""CRUD operations for Team Table"""

from sqlmodel import Session, select
from models.team import Team


def create_cricketer(session: Session, team: Team) -> Team:
    """Creates new cricketer"""
    db_team = Team(**team.model_dump())
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def get_cricketers(session: Session) -> list[Team]:
    """Gets all cricketers"""
    return session.exec(select(Team)).all()


def get_cricketer_by_id(session: Session, team_id: int) -> Team | None:
    """Get cricketer by id"""
    return session.get(Team, team_id)


def delete_cricketer(session: Session, team_id: int) -> Team | None:
    """Delete's specified criketer"""
    team = session.get(Team, team_id)
    if team:
        session.delete(team)
        session.commit()
    return team
