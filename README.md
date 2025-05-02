# Verbs_play_bot
#### Python 3.12
`Verbs_play_bot` — это Telegram- и VK-боты, которые обрабатывают сообщения пользователей с помощью Dialogflow. Используются для помощи пользователям и получения обратной связи.

📌 Примеры:
- Telegram: [t.me/Verbs_Play_bot](https://t.me/Verbs_Play_bot)
- VK: [vk.com/club75514542](https://vk.com/club75514542)

---

## 🚀 Функциональность

- Обработка естественного языка через Dialogflow
- Ответы на часто задаваемые вопросы
- Поддержка Telegram и ВКонтакте
- Логирование ошибок и сообщений в Telegram

---

## 🛠️ Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/nastiaetstesha/Verbs_Play_bot.git
cd Verbs_play_bot
```
## Установка зависимостей
```bash

pip install -r requirements.txt
```

## Переменные окружения
Создайте .env файл в корне проекта со следующим содержимым:

```
VK_API_KEY=токен_группы_ВКонтакте
TELEGRAM_BOT_TOKEN=токен_Telegram_бота
TG_ADMIN_CHAT_ID=chat_id_для_получения_логов
GCLOUD_PROJECT_ID=ваш_dialogflow_project_id
GOOGLE_APPLICATION_CREDENTIALS=application_default_credentials.json
```

### 📁 Структура проекта
```
Verbs_play_bot/
├── create_intent_from_file.py     # Автоматическое создание интентов из JSON
├── gcloud.py                      # Взаимодействие с Dialogflow
├── questions.json                 # Часто задаваемые вопросы и ответы
├── tg_bot.py                      # Логика Telegram-бота
├── vk_bot.py                      # Логика VK-бота
├── requirements.txt               # Зависимости проекта
├── .env                           # Переменные окружения
├── README.md                      # Описание проекта
├── telegram_logs.py
```

## 🔧 Запуск
Telegram бот

`python tg_bot.py`

ВКонтакте бот

`python vk_bot.py`

## 📡 Логирование
Все ошибки и важные события отправляются в Telegram-чат, указанный в TG_ADMIN_CHAT_ID.

```
from telegram import Bot
from telegram_logs import TelegramLogsHandler

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
logger.addHandler(TelegramLogsHandler(bot, chat_id=os.getenv("TG_ADMIN_CHAT_ID")))
```

## 📌 Основные зависимости
`python-telegram-bot` — Telegram API

`vk_api` — для работы с ВКонтакте

`google-cloud-dialogflow `— интеграция с Dialogflow

`python-dotenv` — загрузка .env файла

`logging` — логирование