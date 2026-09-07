from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'FastApi Shop'
    debug: bool = True
    database_url: str = 'postgresql+asyncpg://admin:admin123@localhost:1111/shop'
    cors_origins: list = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5173',
        'http://127.0.0.1:5173'
    ]
    static_dir: str = 'static'
    imgages_dir: str = 'static/images'

    class Config:
        env_file = '.env'

settings = Settings()