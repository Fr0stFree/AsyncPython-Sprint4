from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_PORT: int = 8080
    SERVER_HOST: str = 'localhost'

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'async_sprint_4'
    DB_PASSWORD: str = 'async_password'
    DB_USER: str = 'async_user'

    DATABASE_DSN = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(
        db=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
