import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_db_exists(session):
    result = await session.execute(text('SELECT 1'))