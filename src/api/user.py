from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemes import user as user_schema
from services.user import User as UserCrud


user_router = APIRouter()


@user_router.get('/', response_model=list[user_schema.User])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await UserCrud.filter(session)
    return users


@user_router.get('/{user_id}', response_model=user_schema.User)
async def get_user(*, session: AsyncSession = Depends(get_session), user_id: int):
    user = await UserCrud.get(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@user_router.post('/', response_model=user_schema.User, status_code=HTTPStatus.CREATED)
async def create_user(*, session: AsyncSession = Depends(get_session), data: user_schema.UserCreate):
    user = await UserCrud.create(session, data=data)
    return user


@user_router.patch('/{user_id}', response_model=user_schema.User)
async def update_user(*, session: AsyncSession = Depends(get_session), user_id: int, data: user_schema.UserUpdate):
    user = await UserCrud.update(session, model_id=user_id, data=data)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@user_router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(*, session: AsyncSession = Depends(get_session), user_id: int):
    user = await UserCrud.delete(session, model_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
