from bot_folker.settings import Settings, BotCommands, REPLY_IF_CONTAINS
import logging
import asyncio
from bot_folker.chatgpt import ChatGpt, ChatGptPrompts
from typing import Callable, Coroutine, Any, TypedDict

from telegram import ForceReply, Update, Message
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)
settings = Settings()
chatgpt = ChatGpt(settings=settings)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if not (user and update.message):
        return

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not (update.message and update.message.text):
        return

    if not update.message.text.startswith(REPLY_IF_CONTAINS):
        return

    message = update.message.text.replace(REPLY_IF_CONTAINS, "")

    response = await chatgpt.chat(
        prompt_type=ChatGptPrompts.REPLY_SARCASTICALLY, messages=[message]
    )

    await update.message.reply_text(response)


def generic_command_handler(command: BotCommands):
    prompt_mapper = {
        BotCommands.BRYLIEFY: ChatGptPrompts.BRYLIEFY,
        BotCommands.FLUTELIFY: ChatGptPrompts.FLUTELIFY,
        BotCommands.REBRYLIEFY: ChatGptPrompts.REBRYLIEFY,
        BotCommands.UNBRYLIEFY: ChatGptPrompts.UNBRYLIEFY,
    }

    async def handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> Coroutine[Any, Any, Message]:
        if not (update.message and update.message.text):
            return

        response = await chatgpt.chat(
            prompt_type=prompt_mapper[BotCommands(command)],
            messages=[update.message.text],
        )

        await update.message.reply_text(response)

    return handler


def main() -> None:
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    for command in BotCommands.__members__.values():
        application.add_handler(
            CommandHandler(command, generic_command_handler(command))
        )

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ in ("__main__", "bot_folker.bot"):
    asyncio.run(main())  # type: ignore
