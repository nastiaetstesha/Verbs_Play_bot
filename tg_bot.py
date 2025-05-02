import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from telegram import Update, ForceReply, Bot
from gcloud import detect_intent_texts
from telegram_logs import TelegramLogsHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Доброго времени суток, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def handle_message(update, context):
    user_text = update.message.text
    user_id = update.effective_user.id

    logging.info(f"📩 Новое сообщение от {user_id}: {user_text}")

    try:
        response_text = detect_intent_texts(
            os.getenv("GCLOUD_PROJECT_ID"),
            str(user_id),
            user_text
        )
        update.message.reply_text(response_text)
    except Exception as e:
        logging.exception("❗ Ошибка при обработке сообщения")
        update.message.reply_text("Упс, что-то пошло не так.")


def main() -> None:
    """Start the bot."""
    load_dotenv()

    token = os.getenv("TG_TOKEN")
    admin_chat_id = os.getenv("TG_ADMIN_CHAT_ID")
    bot = Bot(token)

    updater = Updater(token)
    dispatcher = updater.dispatcher

    logger.addHandler(TelegramLogsHandler(bot, chat_id=admin_chat_id))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
        )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()