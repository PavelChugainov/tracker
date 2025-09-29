from fastapi import FastAPI
from src.routers.users import router
from contextlib import asynccontextmanager
from src.database.db_helper import sessionmanager
from src.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    await sessionmanager.init_db()
    yield
    await sessionmanager.close()


app = FastAPI(lifespan=lifespan)


app.include_router(router)
