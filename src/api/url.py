from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemes import url as url_schema
from services.url import Url
from utils.exceptions import ObjectAlreadyExists
from settings import settings


url_router = APIRouter()


@url_router.get('/{url_id}')
async def get_url(*, session: AsyncSession = Depends(get_session), url_id: UUID):
    full_url = await Url.get_redirect_url(session, url_id)
    if not full_url:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Url not found')
    return RedirectResponse(full_url)


@url_router.post('/')
async def create_url(*, session: AsyncSession = Depends(get_session), data: url_schema.UrlCreate):
    try:
        url = await Url.create(session, data=data)
    except ObjectAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Url already exists')
    return ORJSONResponse({'shorten_url': f'{settings.SERVER_ADDRESS}/{url.id}'},
                          status_code=HTTPStatus.CREATED)

