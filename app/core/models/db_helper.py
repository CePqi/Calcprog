from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.factory = async_sessionmaker(
            self.engine, expire_on_commit=False, autoflush=False, autocommit=False
        )

    async def get_async_session(self):
        async with self.factory() as session:
            yield session


db_helper = DataBaseHelper(settings.DB_URL, echo=settings.ECHO)
