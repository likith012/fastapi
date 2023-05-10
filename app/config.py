from pydantic import BaseSettings


class Settings(BaseSettings):
    # DATABASE
    DATABASE_TYPE: str
    DATABASE_DRIVER: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    
    # JWT   
    SECRET_KEY: str
    ALGORITHM: str
    ACEESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')