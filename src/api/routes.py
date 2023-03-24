from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from .url import url_router


router = APIRouter()
router.include_router(url_router, tags=["url"])

