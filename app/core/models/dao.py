from typing import TypeVar, Generic, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from app.core.models.user import User
import logging
from pydantic import BaseModel
from sqlalchemy import select

T = TypeVar("T", bound=Base)


class BaseDao(Generic[T]):
    model: Type[T]

    @classmethod
    async def add(cls, person, session: AsyncSession):
        logging.info("Добавление пользователя")
        try:
            session.add(cls.model(**person))
            await session.commit()
        except SQLAlchemyError as e:
            logging.error("Произошла ошибка", e)

    @classmethod
    async def find_one_or_none(cls, filters: BaseModel, session: AsyncSession):
        logging.info("Поиск по фильтрам")
        try:
            exm = select(cls.model).filter_by(**filters.model_dump(exclude_unset=True))
            result = await session.execute(exm)
            res = result.scalar_one_or_none()
            return res
        except SQLAlchemyError as e:
            logging.error("Ошибка при поиске по фильтрам")


class UserDao(BaseDao[User]):
    model = User

#class SearchHistoryDao(BaseDao[SearchHistory]):
   # model = SearchHistory
