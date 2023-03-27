import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from settings import test_settings
from main import app
from db import Base, get_session


class TestDB:
    def __init__(self):
        self.default_engine = create_async_engine(test_settings.DEFAULT_DSN, future=True, isolation_level="AUTOCOMMIT")
        self.active_engine = None
        self.sessionmaker = None

    async def create(self):
        async with self.default_engine.connect() as conn:
            await conn.execute(text(f" DROP DATABASE IF EXISTS {test_settings.DB_NAME}"))
            await conn.execute(text(f"DROP USER IF EXISTS {test_settings.DB_USER}"))
            await conn.execute(text(f"CREATE DATABASE {test_settings.DB_NAME}"))
            await conn.execute(text(f"CREATE USER {test_settings.DB_USER} WITH PASSWORD '{test_settings.DB_PASSWORD}'"))
            await conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE {test_settings.DB_NAME} TO {test_settings.DB_USER}"))

        self.active_engine = create_async_engine(test_settings.database_dsn, future=True)
        self.sessionmaker = async_sessionmaker(self.active_engine, expire_on_commit=False, class_=AsyncSession)
        async with self.active_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_test_session(self):
        async with self.sessionmaker() as session:
            yield session

    async def drop(self):
        async with self.active_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await self.active_engine.dispose()

        async with self.default_engine.connect() as conn:
            await conn.execute(text(f"DROP DATABASE {test_settings.DB_NAME}"))
            await conn.execute(text(f"DROP USER {test_settings.DB_USER}"))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db(event_loop):
    test_db = TestDB()
    await test_db.create()
    yield test_db
    await test_db.drop()


@pytest_asyncio.fixture(scope="function")
async def fastapi_app(db):
    app.dependency_overrides[get_session] = db.get_test_session
    yield app


@pytest_asyncio.fixture(scope="function")
async def client(fastapi_app):
    async with AsyncClient(app=fastapi_app, base_url=test_settings.server_address) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def session(db):
    async with db.sessionmaker() as session:
        yield session
