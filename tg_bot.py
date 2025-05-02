import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext
)
from telegram import Update, ForceReply
from google.cloud import dialogflow
from gcloud import detect_intent_texts

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
    user_id = os.getenv("TG_ID")
    response_text = detect_intent_texts(
        os.getenv("GCLOUD_PROJECT_ID"),
        user_id,
        user_text
    )
    update.message.reply_text(response_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()

    token = os.getenv("TG_TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
        )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()