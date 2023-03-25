from fastapi import APIRouter

from .url import url_router
from .utils import utils_router


router = APIRouter()

router.include_router(utils_router)
router.include_router(url_router, tags=["url"])
