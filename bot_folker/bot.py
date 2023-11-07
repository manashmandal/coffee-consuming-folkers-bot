from bot_folker.settings import Settings, BotCommands
import logging
import asyncio
from bot_folker.chatgpt import ChatGpt, ChatGptPrompts

from telegram import ForceReply, Update
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

    message: str | None = None

    if not update.message.text.startswith("@folker"):
        message = update.message.text.replace("@folker", "")

    response = await chatgpt.chat(
        prompt_type=ChatGptPrompts.REPLY_SARCASTICALLY, messages=[message]
    )

    await update.message.reply_text(response)


async def bryliefy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not (update.message and update.message.text):
        return

    response = await chatgpt.chat(
        prompt_type=ChatGptPrompts.BRYLIEFY,
        messages=[update.message.text],
    )

    await update.message.reply_text(response)


def main() -> None:
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler(BotCommands.BRYLIEFY, bryliefy))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ in ("__main__", "bot_folker.bot"):
    asyncio.run(main())  # type: ignore
