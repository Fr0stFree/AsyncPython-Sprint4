from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from models import Url as UrlModel
from schemes.url import UrlCreate, UrlUpdate
from .base import RepositoryInterface


class UrlRepository(RepositoryInterface[UrlModel, UrlCreate, UrlUpdate]):
    
    async def get_redirect_url(self, session: AsyncSession, url_id: UUID) -> Optional[HttpUrl]:
        url = await super().get(session, url_id)
        if url is None:
            return None
        await super().update(session, url_id, data=dict(clicks=url.clicks + 1))
        return url.full_url


Url = UrlRepository(UrlModel)
