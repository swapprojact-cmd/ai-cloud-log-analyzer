from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-luna"
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


settings = Settings()
