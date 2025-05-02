import random
import logging
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
from gcloud import detect_intent_texts
from telegram import Bot
from telegram_logs import TelegramLogsHandler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


def handle_event(event):
    user_id = event.user_id
    user_text = event.text

    logging.info(f"Сообщение от пользователя {user_id}: {user_text}")

    try:
        reply, is_fallback = detect_intent_texts(
            project_id=project_id,
            session_id=str(user_id),
            text=user_text,
            return_fallback=True
        )

        if is_fallback:
            logging.info(
                "❗ Не удалось распознать намерение. Ответ не отправлен."
                )
            return

    except Exception as e:
        logging.error("Ошибка при обращении к Dialogflow", exc_info=e)
        reply = "Упс! Что-то пошло не так, попробуй ещё раз позже."

    vk_api.messages.send(
        user_id=user_id,
        message=reply,
        random_id=random.randint(1, 1_000_000)
    )
    logging.info(f"Ответ пользователю {user_id}: {reply}")


if __name__ == "__main__":
    load_dotenv()
    
    token = os.getenv("VK_API_KEY")
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    admin_chat_id = os.getenv("TG_ADMIN_CHAT_ID")
    telegram_token = os.getenv("TG_TOKEN")

    bot = Bot(token=telegram_token)
    logger = logging.getLogger()
    logger.addHandler(TelegramLogsHandler(bot, chat_id=admin_chat_id))

    try:
        logging.info("Запуск бота...")
        vk_session = vk.VkApi(token=token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_event(event)

    except Exception as e:
        logging.error("Произошла ошибка:", exc_info=e)
