from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'FastApi Shop'
    debug: bool = True
    database_url: str 
    test_database_url: str
    cors_origins: list = [
        'http://localhost:5500',
        'http://127.0.0.1:5500'
    ]
    static_dir: str = 'static'
    imgages_dir: str = 'static/images'
    secret_key: str
    algorithm: str = 'HS256'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()