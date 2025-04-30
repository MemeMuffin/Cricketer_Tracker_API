"""Utilities for authentication and authorization"""

import secrets, os
from datetime import timedelta, datetime, timezone
from typing import Annotated
import jwt
from jwt import PyJWTError
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db.session import get_session
from models.admin import Administrator
from models.superuser import Superuser
from schemas.token import TokenData, Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# "write": "Write access", "admin": "Above admin access", "delete": "Delete access"

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# role_based_scopes = {"superuser": ["admin", "write", "delete"], "admin": ["write", "delete"]}


def verify_password(plain_password, hashed_password):
    """Verifies password"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password):
    """Hashes a given password"""
    return pwd_context.hash(plain_password)


def get_user(session: Session, username: str):
    """Return user"""
    user_administrator = session.exec(select(Administrator).where(Administrator.username == username)).first()
    user_superuser = session.exec(select(Superuser).where(Superuser.username == username)).first()
    if user_administrator and user_superuser:
        return {"user": user_administrator, "role": "superuser"}
    elif user_superuser:
        return {"user": user_superuser, "role": "superuser"}
    elif user_administrator:
        return {"user": user_administrator, "role": "admin"}

    return None


def create_access_token(data: dict, expires_delta: timedelta | None):
    """Creates access token"""
    to_encode = data.copy()
    to_encode.update({"sub": data.get("sub"), "role": data.get("role")})
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(session: Session, name: str, password: str):
    """Authenticates user"""
    user_data = get_user(session, name)
    print(user_data)
    if not user_data:
        raise HTTPException(status_code=404, detail="Credentials not found.")
    user = user_data["user"]
    if verify_password(password, user.password):
        return user_data
    raise HTTPException(status_code=404, detail="Credentials not found.")


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: str = Depends(oauth_scheme),
):
    """Returns current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        name = payload.get("sub")
        role = payload.get("role")
        token_data = TokenData(username=name, role=role)
    except PyJWTError:
        raise credentials_exception

    user = get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active(current_user: dict = Depends(get_current_user)):
    """Returns current active user"""
    if current_user["role"] == "admin" or current_user["role"] == "superuser":
        return current_user
    raise HTTPException(status_code=404, detail="No such administrator or superuser available.")


# Token Creation function
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]
):
    """Generates JWT token for user authorization"""
    user_data = authenticate_user(session, form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"www-Authenticate": "Bearer"},
        )
    user = user_data["user"]
    user_role = user_data.get("role")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user_role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")
