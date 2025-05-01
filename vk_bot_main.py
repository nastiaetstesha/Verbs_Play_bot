import random
import logging
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


def echo(event, vk_api):
    message = event.text
    user_id = event.user_id
    logging.info(f"Новое сообщение от пользователя {user_id}: {message}")

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000000)
    )
    logging.info(f"Отправлено сообщение: {message}")


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("VK_API_KEY")

    try:
        logging.info("Запуск бота...")
        vk_session = vk.VkApi(token=token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)

    except Exception as e:
        logging.error("Произошла ошибка:", exc_info=e)
