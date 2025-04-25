"""Utitilty for creating dummy data in db"""

import random
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, select, func
from faker import Faker
from db.session import get_session
from models import cricketer as model_cricketer, team as model_team, match_performance as model_match_performance


def creat_dummy_cricketers(session: Annotated[Session, Depends(get_session)], records=5):
    """Creates dummy data for testing api"""
    existing_cricketers = session.exec(select(func.count()).select_from(model_cricketer.Cricketer)).one()

    if existing_cricketers > 0:
        return []

    fake = Faker()

    cricketers: list[model_cricketer.Cricketer] = []
    for _ in range(records):
        cricketer = model_cricketer.Cricketer(
            name=fake.name(),
            age=random.randint(20, 35),
            country=fake.country(),
            role=random.choice(["All Rounder", "Bowler", "Batsman"]),
            team_id=random.randint(1, 3),
        )
        cricketers.append(cricketer)

    session.add_all(cricketers)
    session.commit()

    with open("dummy_data.txt", "w") as file:
        file.write("Cricketers:\n")
        for key in cricketers:
            session.refresh(key)
            file.write(f"{key.model_dump()}" "\n")

    return cricketers


def creat_dummy_teams(session: Annotated[Session, Depends(get_session)], records=5):
    """Creates dummy data for testing api"""
    existing_teams = session.exec(select(func.count()).select_from(model_team.Team)).one()

    if existing_teams > 0:
        return []

    fake = Faker()

    teams: list[model_team.Team] = []
    for _ in range(records):
        team = model_team.Team(name=fake.unique.company(), country=fake.country())
        teams.append(team)

    session.add_all(teams)
    session.commit()

    with open("dummy_data.txt", "a") as file:
        file.write("Teams:\n")
        for key in teams:
            session.refresh(key)
            file.write(f"{key.model_dump()}" "\n")

    return teams


def creat_dummy_match_performance(session: Annotated[Session, Depends(get_session)], records=5):
    """Creates dummy data for testing api"""
    existing_match_performance = session.exec(
        select(func.count()).select_from(model_match_performance.MatchPerformance)
    ).one()

    if existing_match_performance > 0:
        return []

    fake = Faker()

    match_performances: list[model_match_performance.MatchPerformance] = []
    cricketers = session.exec(select(model_cricketer.Cricketer)).all()
    random_cricketer_id = random.choice(cricketers).id
    match_date = datetime.strptime(fake.date(), "%Y-%m-%d").date()
    for _ in range(records):
        match_performance = model_match_performance.MatchPerformance(
            cricketer_id=random_cricketer_id,
            match_date=match_date,
            match_type=random.choice(["T20", "Test", "One day"]),
            runs=random.randint(0, 200),
            wickets=random.randint(0, 10),
            opponent_team=fake.unique.company(),
        )
        match_performances.append(match_performance)

    session.add_all(match_performances)
    session.commit()

    with open("dummy_data.txt", "a") as file:
        file.write("Match Performances:\n")
        for key in match_performances:
            session.refresh(key)
            file.write(f"{key.model_dump()}" "\n")

    return match_performances
