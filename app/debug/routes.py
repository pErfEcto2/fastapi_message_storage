from fastapi.responses import JSONResponse
from storage.memory.storage import new_db
from fastapi import APIRouter, Depends, status
from storage.interface import DB
from storage.models import User
from auth.auth import get_current_user

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/get_all_users")
async def get_all_users(db: DB = Depends(new_db)) -> JSONResponse:
    return JSONResponse(content=[user.model_dump() for user in db.get_all_users()],
                        status_code=status.HTTP_200_OK,
                        headers={"WWW-Authenticate": "Bearer"})

@router.get("/get_all_records")
async def get_all_records(db: DB = Depends(new_db)) -> JSONResponse:
    return JSONResponse(content=[r.model_dump() for r in db.get_all_records()],
                        status_code=status.HTTP_200_OK,
                        headers={"WWW-Authenticate": "Bearer"})

@router.delete("/delete_user")
async def delete_user(u: User = Depends(get_current_user), db: DB = Depends(new_db)) -> JSONResponse:
    db.delete_user(u)

    return JSONResponse(content={"message": "success"},
                        status_code=status.HTTP_204_NO_CONTENT,
                        headers={"WWW-Authenticate": "Bearer"})
