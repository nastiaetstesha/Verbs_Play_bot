from dotenv import load_dotenv
from google.cloud import dialogflow
import os


load_dotenv()

tg_id = os.getenv("TG_ID")
session_id = tg_id
project_id = os.getenv("GCLOUD_PROJECT_ID")


def detect_intent_texts(
        project_id,
        session_id,
        text,
        language_code='ru',
        return_fallback=False
        ):
    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    fulfillment_text = response.query_result.fulfillment_text

    if return_fallback:
        is_fallback = response.query_result.intent.is_fallback
        return fulfillment_text, is_fallback

    return fulfillment_text

