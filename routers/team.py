"""Routes for teams"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.session import get_session
from crud import team as crud
from schemas import team as schema

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/register", response_model=schema.TeamRead)
async def register_new_team(new_team: schema.TeamCreate, session: Annotated[Session, Depends(get_session)]):
    """Creates new team"""
    return crud.create_cricketer(session, new_team)


@router.get("/get_all", response_model=list[schema.TeamRead])
async def get_all_teams(session: Annotated[Session, Depends(get_session)]):
    """Display all teams"""
    return crud.get_cricketers(session)


@router.get("/by_id", response_model=schema.TeamRead)
async def get_team_by_id(id: int, session: Annotated[Session, Depends(get_session)]):
    """Finds team by id"""
    get_team_by_id = crud.get_cricketer_by_id(session, id)
    if not get_team_by_id:
        raise HTTPException(status_code=404, detail="Team not found.")
    return get_team_by_id


@router.delete("/delete", response_model=schema.TeamRead)
async def delete_team(id: int, session: Annotated[Session, Depends(get_session)]):
    """Deletes team by id"""
    delete_team_by_id = crud.get_cricketer_by_id(session, id)
    if not delete_team_by_id:
        raise HTTPException(status_code=404, detail="Team not found.")
    return crud.delete_cricketer
