import os
from fastapi import FastAPI
import uvicorn
from storage.routes import router as storage_router
from auth.routes import router as auth_router
from debug.routes import router as debug_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(storage_router)
app.include_router(auth_router)
app.include_router(debug_router)




if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")))
