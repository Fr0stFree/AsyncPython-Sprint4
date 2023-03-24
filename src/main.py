import uvicorn
from fastapi import FastAPI

from settings import settings
from api.routes import router


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                loop='asyncio',
                reload=True)
