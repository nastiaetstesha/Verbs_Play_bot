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
from functools import partial

from telegram import Update, ForceReply, Bot
from gcloud import detect_intent_texts
from telegram_logs import TelegramLogsHandler


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


def handle_message(update, context, project_id):
    user_text = update.message.text
    telegram_user_id = update.effective_user.id
    session_id = f"tg-{telegram_user_id}"

    logging.info(f"📩 Новое сообщение от {telegram_user_id}: {user_text}")

    try:
        response_text = detect_intent_texts(
            project_id=project_id,
            session_id=session_id,
            text=user_text
        )
        update.message.reply_text(response_text)

    except Exception:
        logging.exception("❗ Ошибка при обработке сообщения")
        update.message.reply_text("Упс, что-то пошло не так.")


def main() -> None:
    """Start the bot."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    token = os.environ["TG_TOKEN"]
    admin_chat_id = os.environ["TG_ADMIN_CHAT_ID"]
    project_id = os.environ["GCLOUD_PROJECT_ID"]

    bot = Bot(token)

    updater = Updater(token)
    dispatcher = updater.dispatcher

    logger.addHandler(TelegramLogsHandler(bot, chat_id=admin_chat_id))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    wrapped_handler = partial(handle_message, project_id=project_id)

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, wrapped_handler)
        )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()