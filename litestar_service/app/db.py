from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from .config import settings
import logging

logging.basicConfig(level=logging.INFO)


class DataBaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine = create_async_engine(url, echo=True)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(f"Error: {err}")
            await session.rollback()
        finally:
            await session.close()


if settings.DEBUG == 1:
    logging.info("Using dev database")
    sessionmanager = DataBaseSessionManager(
        f"postgresql+asyncpg://{settings.DB_USER_DEV}:{settings.DB_PASSWORD_DEV}@{settings.DB_HOST_DEV}:{settings.DB_PORT_DEV}/{settings.DB_NAME_DEV}"
    )
else:
    logging.info("Using standard database")
    sessionmanager = DataBaseSessionManager(
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


# async def get_db():
#     async with sessionmanager.session() as session:
#         yield session
