from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from openai import AsyncOpenAI
from enum import StrEnum
from typing import Final

REPLY_IF_CONTAINS: Final = "@folker"


class BotCommands(StrEnum):
    BRYLIEFY = "bryliefy"
    FLUTELIFY = "flutelify"
    REBRYLIEFY = "rebryliefy"


class Settings(BaseSettings):
    telegram_bot_token: str = Field(default="<TOKEN>", alias="TELEGRAM_BOT_TOKEN")
    openai_token: str = Field(default="CHATGPT_TOKEN", alias="OPENAI_TOKEN")
    bot_name: str = Field(default="Coffee consuming folkers bot", alias="BOT_NAME")

    chatgpt_model_version: str = Field(default="gpt-4", alias="CHATGPT_MODEL_VERSION")
    chatgpt_temperature: float = Field(default=0.5, alias="CHATGPT_TEMPERATURE")
    chatgpt_max_tokens: int = Field(default=512, alias="CHATGPT_MAX_TOKENS")

    model_config = SettingsConfigDict(env_file=(".env.example", ".env"))

    @property
    def async_open_ai_client(self) -> AsyncOpenAI:
        return AsyncOpenAI(api_key=self.openai_token)
