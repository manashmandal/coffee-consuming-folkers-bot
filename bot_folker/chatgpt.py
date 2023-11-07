from dataclasses import dataclass
from bot_folker.settings import Settings
from enum import StrEnum


class ChatGptPrompts(StrEnum):
    REPLY_SARCASTICALLY = "Reply sarcastically to the following text: "
    BRYLIEFY = "Reply to the following text as an english literature writer like shakespeare but not completely: "


@dataclass(frozen=True)
class ChatGpt:
    settings: Settings

    async def chat(
        self,
        messages: list[str],
        prompt_type: ChatGptPrompts,
        max_tokens: int | None = None,
        temperature: float | None = None,
        stream: bool = False,
    ) -> str | None:
        max_tokens = max_tokens or self.settings.chatgpt_max_tokens
        temperature = temperature or self.settings.chatgpt_temperature
        chatgpt_client = self.settings.async_open_ai_client
        prompt_messages = [{"role": "user", "content": prompt_type.value}] + [
            {"role": "user", "content": message} for message in messages
        ]

        response = await chatgpt_client.chat.completions.create(
            model=self.settings.chatgpt_model_version,
            messages=prompt_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )

        if not len(response.choices) > 0:
            return

        return response.choices[0].message.content
