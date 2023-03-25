import time

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from .url import url_router

router = APIRouter()


@router.get("/ping")
async def ping(session: AsyncSession = Depends(get_session)):
    start_time: float = time.time()
    try:
        await session.execute(text("SELECT 1"))
        total_time: float = round(time.time() - start_time, 2) * 1000
        return ORJSONResponse({"status": "OK", "ping": f'{total_time}ms'})
    except OperationalError:
        return ORJSONResponse({"status": "ERROR", "ping": "Database error"})


router.include_router(url_router, tags=["url"])