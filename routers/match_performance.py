"""Routes for match_performance"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlmodel import Session
from db.session import get_session
from utils.authentication import get_current_user
from crud import match_performance as crud
from schemas import match_performance as schema


router = APIRouter(prefix="/match_performance", tags=["Match Performance"])


@router.post("/create", response_model=schema.MatchPerformanceRead)
async def create_match_performance(
    new_match_performace: schema.MatchPerformanceCreate, session: Annotated[Session, Depends(get_session)]
):
    """Creates new match performance data"""
    return crud.create_match_perfomance(session, new_match_performace)


@router.get("/get_all", response_model=list[schema.MatchPerformanceRead])
async def get_all_match_performance(session: Annotated[Session, Depends(get_session)]):
    """Display all match perfomance data"""
    return crud.get_match_perfomance(session)


@router.get("/get_by_id", response_model=schema.MatchPerformanceRead)
async def get_match_performance_by_id(id: int, session: Annotated[Session, Depends(get_session)]):
    """Get match performance data by id"""
    match_performance_by_id = crud.get_match_perfomance_by_id(session, id)
    if not match_performance_by_id:
        raise HTTPException(status_code=404, detail="Match peformance not found.")
    return match_performance_by_id


@router.delete("/delete", response_model=schema.MatchPerformanceRead)
async def delete_match_perfomance_by_id(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Deletes match performance by id"""
    if current_user.get("role") not in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    delete_match_performanc_by_id = crud.delete_match_perfomance(session, id)
    if not delete_match_performanc_by_id:
        raise HTTPException(status_code=404, detail="Match peformance not found.")
    return crud.delete_match_perfomance(session, id)
