from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Any

class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    TG_CHAT_ID: int

    HH_API_URL: str = "https://api.hh.ru/vacancies"
    USER_AGENT: str = "hh-telegram-bot/1.0"

    DB_DSN: str ="sqlite+aiosqlite:///./hh.db"

    KEYWORDS: List[str] = Field(default_factory=list)
    AREAS: List[str] = Field(default_factory=list)
    PROF_ROLES: List[str] = Field(default_factory=list)
    EXPERIENCE: List[str] = Field(default_factory=list)

    ONLY_WITH_SALARY: bool = False
    PER_PAGE: int = 100
    RUN_EVERY_MIN: int = 15 

    @field_validator("KEYWORDS", "AREAS", "PROF_ROLES", "EXPERIENCE", mode="before")
    @classmethod
    def split_csv(cls, v: Any):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v
    

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive= True,
        extra="ignore",
        enable_decoding=False,
        )

settings = Settings()

