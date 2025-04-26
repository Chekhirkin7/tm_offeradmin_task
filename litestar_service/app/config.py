from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # For local
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_PORT: int = Field(..., env="DB_PORT")

    # For Docker development
    DB_NAME_DEV: str = Field(..., env="DB_NAME_DEV")
    DB_USER_DEV: str = Field(..., env="DB_USER_DEV")
    DB_PASSWORD_DEV: str = Field(..., env="DB_PASSWORD_DEV")
    DB_HOST_DEV: str = Field(..., env="DB_HOST_DEV")
    DB_PORT_DEV: int = Field(..., env="DB_PORT_DEV")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")

    # DEBUG flag to decide which DB to connect to
    DEBUG: int = Field(..., env="DEBUG")

    class Config:
        env_file = ".env"


settings = Settings()
