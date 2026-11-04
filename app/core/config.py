from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://chronos:chronos@localhost:5432/chronosmatch"
    SECRET_KEY: str = "dev-only-change-me"
    ACCESS_TOKEN_MINUTES: int = 60

    @property
    def asyncpg_dsn(self) -> str:
        # raw asyncpg (used for LISTEN) doesn't understand the "+asyncpg" suffix
        return self.DATABASE_URL.replace("+asyncpg", "")


settings = Settings()
