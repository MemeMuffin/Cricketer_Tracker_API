"""Administrator routes"""

from typing import Annotated
from fastapi import APIRouter, Security, Depends, HTTPException
from sqlmodel import Session
from utils.authentication import get_current_user
from db.session import get_session
from crud import superuser as crud
from schemas import superuser as schemas


router = APIRouter(prefix="/superuser", tags=["Superusers"])


@router.post("/register", response_model=schemas.ReadSuperuser)
async def register_superuser(
    new_superuser: schemas.CreateSuperuser,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Registers new superuser"""
    if current_user["role"] != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.create_superuser(session, new_superuser)


@router.get("/get_all", response_model=list[schemas.ReadSuperuser])
async def get_all_superuser(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Shows all superusers"""
    if current_user["role"] != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.read_all(session)


@router.get("/get_by_id", response_model=schemas.ReadSuperuser)
async def get_by_id_superuser(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Shows user by id"""
    if current_user["role"] != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.read_by_id(session, id)


@router.patch("/update", response_model=schemas.ReadSuperuser)
async def update_superuser(
    id: int,
    update_superuser: schemas.UpdateSuperuser,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Updates superuser by id"""
    if current_user["role"] != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.update_superuser(session, update_superuser, id)


@router.delete("/delete", response_model=schemas.ReadSuperuser)
async def delete_superuser(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Security(get_current_user)],
):
    """Deletes superusers"""
    if current_user["role"] != "superuser":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return crud.delete_superuser(session, id)
