"""Routes for ranking"""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_session
from models.ranking import Ranking
from crud.ranking import show_rankings

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("/show_all", response_model=list[Ranking])
def show_all_ranks(session: Annotated[Session, Depends(get_session)]):
    """Shows all the ranks of cricketers based upon their performance"""
    return show_rankings(session)
