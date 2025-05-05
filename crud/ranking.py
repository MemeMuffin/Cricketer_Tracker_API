"""CRUD operation for ranking"""

from sqlmodel import Session, func, select
from models.cricketer import Cricketer
from models.match_performance import MatchPerformance
from models.ranking import Ranking


def create_ranking(session: Session):
    """Creates new ranking"""
    results = session.exec(
        select(
            MatchPerformance.cricketer_id,
            func.sum(MatchPerformance.runs).label("total_runs"),
            func.sum(MatchPerformance.wickets).label("total_wickets"),
        ).group_by(MatchPerformance.cricketer_id)
    ).all()

    rankings = []
    i = 1
    for cricketer_id, total_runs, total_wickets in results:
        score = total_runs + (total_wickets * 20)
        cricketer = session.get(Cricketer, cricketer_id)
        rank = Ranking(
            name=cricketer.name,
            total_runs=total_runs,
            total_wickets=total_wickets,
            score=score,
            rank_position=i,
            cricketer_id=cricketer_id,
        )
        i = i + 1
        rankings.append(rank)

    pos = 1
    rankings.sort(key=lambda x: x.score)
    for rank in rankings:
        rank.rank_position = pos
        session.add(rank)
        pos += 1
    session.commit()
    return rankings


def update_rankings(session: Session, new_match_performance: MatchPerformance):
    """Updates the ranking system"""

    score = new_match_performance.runs + (new_match_performance.wickets * 20)
    cricketer = session.get(Cricketer, new_match_performance.cricketer_id)
    ranking = session.exec(select(Ranking).where(Ranking.cricketer_id == new_match_performance.cricketer_id)).first()
    if ranking:
        ranking.total_runs += new_match_performance.runs
        ranking.total_wickets += new_match_performance.wickets
        ranking.score = ranking.total_runs + (ranking.total_wickets * 20)
    else:
        ranking = Ranking(
            name=cricketer.name,
            total_runs=new_match_performance.runs,
            total_wickets=new_match_performance.wickets,
            score=score,
            rank_position=None,
            cricketer_id=cricketer.id,
        )
        session.add(ranking)
    session.commit()

    all_rankings = session.exec(select(Ranking)).all()
    all_rankings.sort(key=lambda x: x.score)

    for i, rank in enumerate(all_rankings, start=1):
        rank.rank_position = i
        session.add(rank)

    session.commit()
    return all_rankings


def show_rankings(session: Session) -> list[Ranking]:
    """Shows all the Ranks"""
    return session.exec(select(Ranking).order_by(Ranking.rank_position)).all()


def delete_ranking(session: Session, deleted_match_performance: MatchPerformance):
    """Deletes or updates ranking when a match performance is deleted"""
    is_existing = session.exec(
        select(MatchPerformance).where(
            MatchPerformance.cricketer_id == deleted_match_performance.cricketer_id,
            MatchPerformance.id != deleted_match_performance.id,
        )
    ).all()
    ranking = session.exec(
        select(Ranking).where(Ranking.cricketer_id == deleted_match_performance.cricketer_id)
    ).first()
    if ranking:
        if is_existing:
            ranking.total_runs = max(0, ranking.total_runs - (deleted_match_performance.runs or 0))
            ranking.total_wickets = max(0, ranking.total_wickets - (deleted_match_performance.wickets or 0))
            ranking.score = ranking.total_runs + (ranking.total_wickets * 20)
        else:
            session.delete(ranking)

    session.commit()
