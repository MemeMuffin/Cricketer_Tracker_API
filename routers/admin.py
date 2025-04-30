"""Administrator routes"""

from typing import Annotated
from fastapi import APIRouter, Security, Depends, HTTPException
from sqlmodel import Session
from utils.authentication import get_current_user
from db.session import get_session
from crud import admin as crud
from schemas import admin as schemas

router = APIRouter(prefix="/administrator", tags=["Administrator"])


@router.post("/register", response_model=schemas.ReadAdministrator)
async def register_administrator(
    new_administrator: schemas.CreateAdministrator,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Registers new administrator"""
    if current_user.get("role") in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.create_administrator(session, new_administrator)


@router.get("/get_all", response_model=list[schemas.ReadAdministrator])
async def get_all(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Shows all administrator"""
    if current_user.get("role") in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.read_all(session)


@router.get("/get_by_id", response_model=schemas.ReadAdministrator)
async def get_by_id(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Shows administrator by given id"""
    if current_user.get("role") in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.read_by_id(session, id)


@router.patch("/update", response_model=schemas.ReadAdministrator)
async def update_administrator(
    id: int,
    update_admin: schemas.UpdateAdministrator,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Updates an administrator"""
    if current_user.get("role") in ("admin", "superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.update_administrator(session, id, update_admin)


@router.delete("/delete", response_model=schemas.ReadAdministrator)
async def delete_administrator(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Updates an administrator"""
    if current_user.get("role") != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.delete_by_id(session, id)
