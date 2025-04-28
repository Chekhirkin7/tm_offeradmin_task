from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Прибрав Field(..., env=""), так як воно автоматом підтягується

    # For local
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    # For Docker development
    DB_NAME_DEV: str
    DB_USER_DEV: str
    DB_PASSWORD_DEV: str
    DB_HOST_DEV: str
    DB_PORT_DEV: int

    # SECRET_KEY: str = Field(..., env="SECRET_KEY") # Secret key використовується тільки Django

    # DEBUG flag to decide which DB to connect to
    DEBUG: bool  # Автоматично конвертує 1 в True та 0 в False

    class Config:
        # env_file = "../.env"
        extra = "ignore"  # ігноруємо невідомі параметри


settings = Settings()
