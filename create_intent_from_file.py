import json
import os
from google.cloud import dialogflow


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts
        ):
    
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for phrase in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def create_all_intents_from_json(json_path, project_id):
    with open(json_path, 'r', encoding='utf-8') as file:
        intents_data = json.load(file)

    for intent_title, data in intents_data.items():
        questions = data.get("questions", [])
        answer = data.get("answer", "")
        create_intent(project_id, intent_title, questions, [answer])


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    project_id = os.getenv("GCLOUD_PROJECT_ID")
    json_path = "questions.json"

    create_all_intents_from_json(json_path, project_id)
