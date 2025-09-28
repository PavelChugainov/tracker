from __future__ import annotations
import logging
import os
from typing import Optional, AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool


logging.basicConfig(
    filename="./logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("Fastapi logger")


load_dotenv()

db_password = str(os.getenv("DATABASE_PASSWORD"))
db_name = str(os.getenv("DATABASE_NAME"))
db_port = int(str(os.getenv("DATABASE_PORT")))
db_user = str(os.getenv("DATABASE_USER", "postgres"))


class DataBase:
    def __init__(
        self,
        user: str = "postgres",
        password: str = "postgres",
        database: str = "database",
        host: str = "127.0.0.1",
        dialect: str = "postgresql",
        port: int = 5432,
    ):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.dialect = dialect
        self.url = f"{dialect}+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def init_db(self) -> None:
        """initialize the database engine and session factory"""
        self.engine = create_async_engine(
            self.url,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=True,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )
        logger.info("Database egine and session factory initialized")

    async def close(self) -> None:
        """Dispose of the database engine"""

        if self.engine:
            await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session with the correct schema set"""
        # await self.init_db()
        if not self.session_factory:
            logger.info("Database session factory is not initialized.")
            raise RuntimeError("Database session factory is not initialized.")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.info(f"Database session error: {e}")
                raise RuntimeError(f"Database session error: {e!r}")


# Global instances
sessionmanager = DataBase(
    user=db_user,
    database=db_name,
    password=db_password,
    port=db_port,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in sessionmanager.get_session():
        yield session
