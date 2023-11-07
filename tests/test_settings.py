from bot_folker.settings import Settings
from bot_folker.chatgpt import ChatGpt, ChatGptPrompts
import pytest


@pytest.fixture()
def settings() -> Settings:
    return Settings()


@pytest.fixture()
def chatgpt(settings: Settings) -> ChatGpt:
    return ChatGpt(settings=settings)


@pytest.mark.asyncio()
async def test_chatgpt(chatgpt: ChatGpt) -> None:
    response = await chatgpt.chat(
        prompt_type=ChatGptPrompts.REPLY_SARCASTICALLY, messages=["hello my friend"]
    )

    assert response is not None
