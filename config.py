from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(slots=True)
class BotConfig:
    token: str
    web_app_url: str
    api_base_url: str

    @classmethod
    def from_env(cls) -> "BotConfig":
        token = os.getenv("BOT_TOKEN")
        if not token:
            raise RuntimeError("Environment variable BOT_TOKEN is required")

        web_app_url = os.getenv("WEB_APP_URL", "https://example.com")
        api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        return cls(token=token, web_app_url=web_app_url, api_base_url=api_base_url)
