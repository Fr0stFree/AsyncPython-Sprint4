import asyncio
import uuid
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from settings import settings
from main import app
from schemes import url as url_schema
from models import Url, UrlClick


Base: DeclarativeMeta = declarative_base()
metadata = Base.metadata





class TestDB:
    engine = create_async_engine(url=settings.database_dsn, echo=True, future=True)
    async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    
    def __init__(self):
        self.port = 5432
        self.host = 'localhost'
        self.user = 'postgres'
        self.password = 'postgres'
        self.db_name = 'postgres'
        self.engine = self.create_engine()
        self.async_session = self.create_sessionmaker(self.engine)
    
    def create_engine(self):
        engine = create_async_engine(
            url=f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}',
            echo=True,
            future=True,
            isolation_level='AUTOCOMMIT'
        )
        return engine

    def create_sessionmaker(self, engine):
        return sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

        
    async def create_test_db(self):
        async with self.async_session() as session:
            await session.execute(text('CREATE DATABASE test_db'))
            await session.execute(text('CREATE USER test_user WITH PASSWORD \'test_password\''))
            await session.execute(text('GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user'))
            self.db_name = 'test_db'
            self.password = 'test_password'
            self.user = 'test_user'

    async def drop_test_db(self):
        async with self.get_session() as session:
            await session.execute(text('DROP DATABASE test_db'))
            await session.execute(text('DROP USER test_user'))
            self.db_name = 'postgres'
            self.password = 'postgres'
            self.user = 'postgres'

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
            
    

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
    
    
@pytest_asyncio.fixture(scope="session")
async def test_db():
    db = TestDB()
    await db.create_test_db()
    await db.create_tables()
    yield db
    await db.drop_test_db()


@pytest_asyncio.fixture(scope="function")
async def session(test_db):
    async with test_db.get_session() as session:
        yield session
    