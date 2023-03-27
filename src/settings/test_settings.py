from pydantic import Field

from .base_settings import Settings


class TestSettings(Settings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'test_db'
    DB_PASSWORD: str = 'test_password'
    DB_USER: str = 'test_user'