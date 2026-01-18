from storage.memory.storage import new_db
from fastapi import APIRouter, Depends
from storage.interface import DB
from storage.models import User
from auth.auth import get_current_user

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/get_all_users")
async def get_all_users(db: DB = Depends(new_db)):
    return db.get_all_users()

@router.get("/get_all_records")
async def get_all_records(db: DB = Depends(new_db)):
    return db.get_all_records()

@router.delete("/delete_user")
async def delete_user(u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    db.delete_user(u)
