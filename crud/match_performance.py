"""CRUD operations for Match Performance Table"""

from sqlmodel import Session, select
from models.match_performance import MatchPerformance


def create_match_perfomance(session: Session, match_performance: MatchPerformance) -> MatchPerformance:
    """Creates new cricketer"""
    db_match_performance = MatchPerformance(**match_performance.model_dump())
    session.add(db_match_performance)
    session.commit()
    session.refresh(db_match_performance)
    return db_match_performance


def get_match_perfomance(session: Session) -> list[MatchPerformance]:
    """Gets all cricketers"""
    return session.exec(select(MatchPerformance)).all()


def get_match_perfomance_by_id(session: Session, match_performance_id: int) -> MatchPerformance | None:
    """Get cricketer by id"""
    return session.get(MatchPerformance, match_performance_id)


def delete_match_perfomance(session: Session, match_performance_id: int) -> MatchPerformance | None:
    """Delete's specified criketer"""
    match_performance = session.get(MatchPerformance, match_performance_id)
    if match_performance:
        session.delete(match_performance)
        session.commit()
    return match_performance
