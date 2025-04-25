from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import select
from db.session import get_session, create_db_and_tables
from routers.cricketers import router as cricketers
from routers.team import router as teams
from routers.match_performance import router as match_performances
from models import cricketer as model_cricketer, team as model_team, match_performance as model_match_performance
from utils.dummy_data import creat_dummy_cricketers, creat_dummy_match_performance, creat_dummy_teams


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

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(cricketers)
app.include_router(teams)
app.include_router(match_performances)
