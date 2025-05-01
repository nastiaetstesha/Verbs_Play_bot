from dotenv import load_dotenv
from google.cloud import dialogflow
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
import logging
import os
import json


load_dotenv()

tg_id = os.getenv("TG_ID")
session_id = tg_id
project_id = os.getenv("GCLOUD_PROJECT_ID")


def detect_intent_texts(project_id, session_id, text, language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def handle_message(update, context):
    user_text = update.message.text
    user_id = os.getenv("TG_ID")
    response_text = detect_intent_texts(
        os.getenv("GCLOUD_PROJECT_ID"),
        user_id,
        user_text
    )
    update.message.reply_text(response_text)