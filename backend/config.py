from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'FastApi Shop'
    debug: bool = True
    database_url: str = 'postgresql+asyncpg://admin:admin123@localhost:1111/shop'
    cors_origins: list = [
        'http://localhost:5500',
        'http://127.0.0.1:5500'
    ]
    static_dir: str = 'static'
    imgages_dir: str = 'static/images'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()