from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Workshop Demo API"
    database_url: str = "sqlite+aiosqlite:///./demo.db"
    api_key: str = "demo-api-key-2024"
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    debug: bool = False

    model_config = {"env_prefix": "DEMO_"}


settings = Settings()
