import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    )

load_dotenv()

db_url = os.getenv("DATABASE_URL")
db_password = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

class 

class DataBase:
    def __init__(self,
                user: str = 'postgres',
                password: str = "postgres",
                database: str = "database",
                host: str = "127.0.0.1",
                type: str = "postgresql",
                db_name: str = "postgres"
                  ):
        self.user = user
        self.password = password
        self.database = database, 
        self.host = host
        self.type = type
        self.db_name = db_name
        self.engine = create_async_engine(
            url=f"{type}+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}",
            echo=True,
            )
        self.async_session = sessionmaker(
            class_=AsyncSession,
            expire_on_commit=False,
        )
    async def init_model(self, base):
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)
            await conn.run_sync(base.metadate.create_all)
    
    #Dependency
    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

