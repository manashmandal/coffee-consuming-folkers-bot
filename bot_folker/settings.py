from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    telegram_bot_token: str = Field(default="<TOKEN>", alias="TELEGRAM_BOT_TOKEN")
    telegram_baseurl: str = Field(default="<TG_BASEURL>", alias="TELEGRAM_BASEURL")
    openapi_token: str = Field(default="CHATGPT_TOKEN", alias="OPENAPI_TOKEN")
    openapi_baseurl: str = Field(default="OPENAPI_BASEURL", alias="OPENAPI_BASEURL")
    bot_name: str = Field(default="Coffee consuming folkers bot", alias="BOT_NAME")

    model_config = SettingsConfigDict(env_file=(".env.example", ".env"))
