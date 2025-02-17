import requests
import json
from pathlib import Path
from constants import YANDEX_GPT_API_URL, SERVICE_ACCOUNT_API_KEY, FOLDER_ID, RESPONSES, BUCKET_NAME, BUCKET_INSTRUCTIONS_FILE_KEY

def handle_text_message(text):
    answer = get_answer_from_gpt(text)
    if not answer:
        return RESPONSES["answer_error"]
    else:
        return answer

def get_answer_from_gpt(text):
    headers = {
        "Content-Type": "application/json",
        "x-folder-id": FOLDER_ID,
        "Authorization": f"Api-Key {SERVICE_ACCOUNT_API_KEY}",
    }

    print(text)
    body = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
        "messages": [
            {
                "role": "system",
                "text": get_object_from_bucket(BUCKET_INSTRUCTIONS_FILE_KEY)
            },
            {
                "role": "user",
                "text": text
            },
        ],
    }

    try:
        response = requests.post(YANDEX_GPT_API_URL, headers=headers, json=body)
        print(response.text)
        response.raise_for_status()  # Raise exception for HTTP errors.
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Yandex GPT API: {e}")
        return None

    # Extract the final answer from the response.
    alternatives = response.json().get("result", {}).get("alternatives", [])
    for alt in alternatives:
        if alt.get("status") == "ALTERNATIVE_STATUS_FINAL":
            return alt["message"].get("text")
    return None

def get_object_from_bucket(object_key):
    try:
        with open(Path("/function/storage", BUCKET_NAME, object_key), "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("File not found in bucket", {"object_key": object_key})
        return ""