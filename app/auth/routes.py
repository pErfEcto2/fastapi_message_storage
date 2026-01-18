from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from .models import Token
from storage.interface import DB
from storage.memory.storage import new_db
from .auth import auth_user, create_access_token, create_user_from_form
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(prefix="/auth", tags=["auth"])

__access_token_expires_m = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_M")
assert __access_token_expires_m is not None
__access_token_expires_m = float(__access_token_expires_m)

class __signup_form(BaseModel):
    name: str
    passwd: str

@router.post("/signup")
async def signup(form_data: __signup_form, db: DB = Depends(new_db)):
    if db.user_exists_by_name(form_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    u = create_user_from_form(form_data.name, form_data.passwd)
    db.add_user(u)

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB = Depends(new_db)) -> Token:
    u = auth_user(form_data.username, form_data.password, db)
    if u is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": u.name}, expires_delta=timedelta(minutes=__access_token_expires_m)
    )
    return Token(access_token=access_token, token_type="bearer")
