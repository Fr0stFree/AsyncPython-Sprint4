from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemes import url as url_schema
from services.url import Url as UrlCrud


url_router = APIRouter()

@url_router.get('/{url_key}', response_model=url_schema.Url)
async def get_url(*, session: AsyncSession = Depends(get_session), url_key: UUID):
    url = await UrlCrud.get(session, id=url_key)
    if not url:
        raise HTTPException(status_code=404, detail='Url not found')
    return url


@url_router.post('/', response_model=url_schema.Url, status_code=HTTPStatus.CREATED)
async def create_url(*, session: AsyncSession = Depends(get_session), data: url_schema.UrlCreate):
    url = await UrlCrud.create(session, data=data)
    if not url:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Url already exists')
    return url

