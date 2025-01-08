import base64
import requests
import json
from constants import SERVICE_ACCOUNT_API_KEY, FOLDER_ID, RESPONSES, TELEGRAM_API_URL, TELEGRAM_FILE_URL

def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile"
    try:
        response = requests.get(url, params={"file_id": file_id})
        response.raise_for_status()
        return response.json().get("result", {}).get("file_path")

    except requests.RequestException as e:
        print(f"Failed to get file path: {e}", {"file_id": file_id})
        return None

def get_photo(file_path):
    url = f"{TELEGRAM_FILE_URL}/{file_path}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    except requests.RequestException as e:
        print(f"Failed to download photo: {e}", {"file_path": file_path})
        return None

def encode_to_base64(bytes_content):
    return base64.b64encode(bytes_content).decode("utf-8")

def get_text_from_photo(photo_base64):
    body = {
        "mimeType": "JPEG",
        "languageCodes": ["*"],
        "model": "page",
        "content": photo_base64
    }

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers= {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {SERVICE_ACCOUNT_API_KEY}",
        "x-folder-id": FOLDER_ID
    }

    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(body))
        response.raise_for_status()  # Raise exception for HTTP errors.
        return response.json().get("result", {}).get("textAnnotation", {}).get("fullText")

    except requests.RequestException as e:
        print(f"OCR recognition failed: {e}")
        return RESPONSES["ocr_recognition_error"]

def handle_photo_message(file_id):
    file_path = get_file_path(file_id)
    photo = get_photo(file_path)
    photo_base64 = encode_to_base64(photo)
    text = get_text_from_photo(photo_base64)
    return text
