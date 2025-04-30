"""Routes for cricketers"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlmodel import Session
from db.session import get_session
from utils.authentication import get_current_user
from crud import cricketer as crud
from schemas import cricketer as schema

router = APIRouter(prefix="/cricketers", tags=["Cricketers"])


@router.post("/register", response_model=schema.CricketRead)
async def create_cricketer(
    new_cricketer: schema.CricketCreate,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Creates new cricketers"""
    return crud.create_cricketer(session, new_cricketer)


@router.get("/get_all", response_model=list[schema.CricketRead])
async def get_all_cricketers(session: Annotated[Session, Depends(get_session)]):
    """Reads all cricketers in database"""
    return crud.get_cricketers(session)


@router.get("/find_cricketer", response_model=schema.CricketRead)
async def find_cricketer_by_id(cricketer_id: int, session: Annotated[Session, Depends(get_session)]):
    """Finds cricketer by id"""
    cricketer_by_id = crud.get_cricketer_by_id(session, cricketer_id)
    if not cricketer_by_id:
        raise HTTPException(status_code=404, detail="Cricketer not found")
    return cricketer_by_id


@router.delete("/delete", response_model=schema.CricketRead)
async def delete_cricketer(
    cricketer_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Deletes a cricketer"""
    if current_user.get("role") not in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    cricketer_by_id = crud.get_cricketer_by_id(session, cricketer_id)
    if not cricketer_by_id:
        raise HTTPException(status_code=404, detail="Cricketer not found")
    return crud.delete_cricketer(session, cricketer_id)
