from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from .models import User
from .interface import DB
from .memory.storage import new_db
from auth.auth import get_current_user

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/add_record")
async def add_data(payload: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    db.add_data(u, payload)

class __change_data_payload(BaseModel):
    id: str
    nd: str

@router.post("/change_record")
async def change_data(payload: __change_data_payload, u: User =Depends(get_current_user), db: DB = Depends(new_db)):
    if not db.user_has_data_by_id(u, payload.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant change data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db.change_data(payload.id, payload.nd)

@router.delete("/delete_record")
async def delete_record(data_id: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    if not db.user_has_data_by_id(u, data_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant delete data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db.delete_record(data_id)

@router.get("/get_record")
async def get_record(data_id: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    if not db.user_has_data_by_id(u, data_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant get data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    r = db.get_record(data_id)
    if r is not None:
        return r

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No such record",
        headers={"WWW-Authenticate": "Bearer"}
    )
