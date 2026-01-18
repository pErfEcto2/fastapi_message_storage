from datetime import timedelta, datetime, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import random
import string

from storage.interface import DB
from storage.memory.storage import new_db
from storage.models import User
from .models import TokenData


load_dotenv()

__passwd_hash = PasswordHash.recommended()
__oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
__secret_key = os.getenv("JWT_SECRET_KEY")
__algorithm = os.getenv("JWT_ALGORITHM")

assert __secret_key is not None
assert __algorithm is not None

def verify_passwd(pwd: str, salt: str, hashed_pwd: str) -> bool:
    return __passwd_hash.verify(pwd + salt, hashed_pwd)

def hash_passwd(pwd: str, salt: str) -> str:
    return __passwd_hash.hash(pwd + salt)

def auth_user(name: str, passwd: str, db: DB) -> User | None:
    u = db.get_user_by_name(name)
    if u is None:
        return
    if not verify_passwd(passwd, u.salt, u.hashed_pwd):
        return

    return u

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, __secret_key, algorithm=__algorithm)
    return encoded_jwt

def create_salt_for_passwd(lenght: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=lenght))

def create_user_from_form(name: str, passwd: str) -> User:
    salt = create_salt_for_passwd()
    hashed_passwd = hash_passwd(passwd, salt)
    u = User(name=name, hashed_pwd=hashed_passwd, salt=salt)
    return u

async def get_current_user(token: Annotated[str, Depends(__oauth2_scheme)], db: DB = Depends(new_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, __secret_key, algorithms=[__algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(name=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = db.get_user_by_name(token_data.name)
    if user is None:
        raise credentials_exception
    return user

