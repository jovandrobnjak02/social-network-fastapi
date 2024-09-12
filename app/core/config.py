from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str 
    POSTGRES_DB: str 
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    REDIS_PORT: str
    REDIS_HOST: str
    API_VERSION: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()