from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SERVER_PORT: int = Field(8080, env='SERVER_PORT')
    SERVER_HOST: str = Field('localhost', env='SERVER_HOST')

    DB_HOST: str = Field('localhost', env='DB_HOST')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_NAME: str = Field('postgres', env='DB_NAME')
    DB_PASSWORD: str = Field('postgres', env='DB_PASSWORD')
    DB_USER: str = Field('postgres', env='DB_USER')
    
    @property
    def database_dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(
            db=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )

    @property
    def server_address(self) -> str:
        return f'http://{self.SERVER_HOST}:{self.SERVER_PORT}'
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
