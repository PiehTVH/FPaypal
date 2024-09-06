from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    redis_url: str
    paypal_url: str
    
    class Config:
        env_file = "app/.env"

settings = Settings()