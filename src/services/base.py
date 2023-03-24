from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

import sqlalchemy.exc
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base
from utils.exceptions import ObjectAlreadyExists


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def filter(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryInterface(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, session: AsyncSession, id: Union[int, UUID]) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        result = await session.execute(statement)
        await session.commit()
        return result.scalar_one_or_none()

    async def filter(self, session: AsyncSession, *, offset: int = 0,
                     limit: int = 100, **kwargs) -> List[ModelType]:
        statement = select(self._model).filter_by(**kwargs) \
                                       .offset(offset) \
                                       .limit(limit)
        # for key, value in kwargs.items():
        #     statement = statement.where(getattr(self._model, key) == value)
        result = await session.execute(statement)
        await session.commit()
        return result.scalars().all()

    async def create(self, session: AsyncSession, *, data: CreateSchemaType) -> ModelType:
        statement = insert(self._model).values(**data.dict()) \
                                       .returning(self._model)
        try:
            result = await session.execute(statement)
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
            raise ObjectAlreadyExists
        await session.commit()
        return result.scalar_one()

    async def update(self, session: AsyncSession, id: Union[int, UUID], *,
                     data: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        fields = data if isinstance(data, dict) else data.dict()
        statement = update(self._model).where(self._model.id == id) \
                                       .values(**fields) \
                                       .returning(self._model)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        await session.commit()
        return user

    async def delete(self, session: AsyncSession, *, id: Union[int, UUID]) -> None:
        statement = delete(self._model).where(self._model.id == id) \
                                       .returning(self._model)
        result = await session.execute(statement)
        user = result.scalar_one()
        await session.commit()
        return user
