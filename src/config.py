from pydantic_settings import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_NAME: str
    DB_PORT: str

    class Config:
        extra = Extra.ignore
        env_file = "./.env"


settings = Settings()
