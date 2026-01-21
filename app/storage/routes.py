from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status

from .models import User
from .interface import DB
from .memory.storage import new_db
from auth.auth import get_current_user

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/add_record")
async def add_data(data: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    db.add_data(u, data)

    return JSONResponse(content={"message": "success"},
                        status_code=status.HTTP_201_CREATED,
                        headers={"WWW-Authenticate": "Bearer"})


class __change_data_payload(BaseModel):
    id: str
    new_data: str

@router.post("/change_record")
async def change_data(payload: __change_data_payload, u: User =Depends(get_current_user), db: DB = Depends(new_db)):
    if not db.user_has_data_by_id(u, payload.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant change data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db.change_data(payload.id, payload.new_data)

    return JSONResponse(content={"message": "success"},
                        status_code=status.HTTP_200_OK,
                        headers={"WWW-Authenticate": "Bearer"})

@router.delete("/delete_record")
async def delete_record(data_id: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)):
    if not db.user_has_data_by_id(u, data_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant delete data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db.delete_record(data_id)

    return JSONResponse(content={"message": "success"},
                        status_code=status.HTTP_204_NO_CONTENT,
                        headers={"WWW-Authenticate": "Bearer"})

@router.get("/get_record")
async def get_record(data_id: str, u: User = Depends(get_current_user), db: DB = Depends(new_db)) -> JSONResponse:
    if not db.user_has_data_by_id(u, data_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cant get data",
            headers={"WWW-Authenticate": "Bearer"}
        )

    r = db.get_record(data_id)
    if r is not None:
        return JSONResponse(content=r.model_dump(),
                            status_code=status.HTTP_200_OK,
                            headers={"WWW-Authenticate": "Bearer"})

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No such record",
        headers={"WWW-Authenticate": "Bearer"}
    )
