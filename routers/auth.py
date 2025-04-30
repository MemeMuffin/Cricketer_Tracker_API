"""Authentication and authorization routes"""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from db.session import get_session
from schemas.token import Token
from utils.authentication import login_for_access_token


router = APIRouter()


@router.post("/token", response_model= Token)
async def access_token_generation(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]
):
    """Generates JWT token for user authorization"""
    return await login_for_access_token(form_data, session)