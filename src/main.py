import uvicorn
from fastapi import FastAPI

from settings import settings
from api.routes import router
from utils import exceptions as exc


app = FastAPI()
app.include_router(router)
app.add_exception_handler(exc.ObjectAlreadyExists, exc.obj_already_exists_handler)
app.add_exception_handler(exc.ObjectDoesNotExist, exc.obj_does_not_exist_handler)
app.add_exception_handler(exc.UrlIsBanned, exc.url_is_banned_handler)


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                loop='asyncio',
                reload=True)
