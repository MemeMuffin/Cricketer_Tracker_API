"""CRUD operations for Match Performance Table"""

from sqlmodel import Session, select, func
from fastapi import HTTPException
from models.ranking import Ranking
from models.cricketer import Cricketer
from models.match_performance import MatchPerformance
from crud.ranking import update_rankings, create_ranking, delete_ranking


def create_match_perfomance(session: Session, match_performance: MatchPerformance) -> MatchPerformance:
    """Creates new cricketer"""
    db_match_performance = MatchPerformance(**match_performance.model_dump())
    # is_existing = session.exec(
    #     select(MatchPerformance).where(MatchPerformance.match_date == db_match_performance.match_date)
    # ).first()
    is_existing_cricketer = session.exec(
        select(Cricketer).where(Cricketer.id == db_match_performance.cricketer_id)
    ).first()
    if not is_existing_cricketer:
        raise HTTPException(status_code=404, detail="The cricketer does not exists")
    # if is_existing:
    #     raise HTTPException(status_code=403, detail="Match performance already exists.")
    session.add(db_match_performance)
    session.commit()
    session.refresh(db_match_performance)
    is_existing_rankings = session.exec(select(func.count()).select_from(Ranking)).one()
    if is_existing_rankings > 0:
        update_rankings(session, db_match_performance)
    else:
        create_ranking(session)
    return db_match_performance


def get_match_perfomance(session: Session) -> list[MatchPerformance]:
    """Gets all cricketers"""
    return session.exec(select(MatchPerformance).order_by(MatchPerformance.match_date)).all()


def get_match_perfomance_by_id(session: Session, match_performance_id: int) -> MatchPerformance | None:
    """Get cricketer by id"""
    return session.get(MatchPerformance, match_performance_id)


def delete_match_perfomance(session: Session, match_performance_id: int) -> MatchPerformance | None:
    """Delete's specified criketer"""
    match_performance = session.get(MatchPerformance, match_performance_id)
    if match_performance:
        session.delete(match_performance)
        with session.no_autoflush:
            delete_ranking(session, match_performance)
        session.commit()
    return match_performance
