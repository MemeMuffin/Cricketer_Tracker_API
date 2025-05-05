from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import select, func
from db.session import get_session, create_db_and_tables
from routers.auth import router as authentication
from routers.superuser import router as superusers
from routers.admin import router as administrators
from routers.cricketers import router as cricketers
from routers.team import router as teams
from routers.match_performance import router as match_performances
from routers.ranking import router as rankings
from models import (
    cricketer as model_cricketer,
    team as model_team,
    match_performance as model_match_performance,
    superuser,
    admin,
    ranking,
)
from crud.ranking import create_ranking
from utils.dummy_data import (
    creat_dummy_cricketers,
    creat_dummy_match_performance,
    creat_dummy_teams,
    create_dummy_admin,
    create_dummy_superuser,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Generates and intializes db and its tables"""
    create_db_and_tables()
    with next(get_session()) as session:
        existing_cricketers = session.exec(select(model_cricketer.Cricketer)).all()
        if not existing_cricketers:
            creat_dummy_cricketers(session)
        existing_teams = session.exec(select(model_team.Team)).all()
        if not existing_teams:
            creat_dummy_teams(session)
        existing_match_performances = session.exec(select(model_match_performance.MatchPerformance)).all()
        if not existing_match_performances:
            creat_dummy_match_performance(session)
        existing_superusers = session.exec(select(superuser.Superuser)).all()
        if not existing_superusers:
            create_dummy_superuser(session)
        existing_admin = session.exec(select(admin.Administrator)).all()
        if not existing_admin:
            create_dummy_admin(session)
        is_existing_rankings = session.exec(select(func.count()).select_from(ranking.Ranking)).one()
        if not is_existing_rankings > 0:
            create_ranking(session)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def welcome():
    """Simple function to check for working app"""
    return {
        "message": "Hello, Welcome to my cricketer tracker API.Add /docs to url to check requests.",
        "Dummy Superuser": "rebecca45: iH8DPgcpQ#",
        "Dummy administrator": "williamskaren: n5wUZr5F+t",
    }


app.include_router(authentication)
app.include_router(superusers)
app.include_router(administrators)
app.include_router(cricketers)
app.include_router(teams)
app.include_router(match_performances)
app.include_router(rankings)
