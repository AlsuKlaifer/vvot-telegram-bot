import requests
import json
from constants import SERVICE_ACCOUNT_API_KEY, FOLDER_ID, RESPONSES, TELEGRAM_API_URL
from image_processing import handle_photo_message
from text_processing import handle_text_message

COMMANDS = ["/start", "/help"]

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    r = requests.post(url=url, data=data)
    return r

def delete_message(chat_id, message_id):
    url = f"{TELEGRAM_API_URL}/deleteMessage"
    data = {'chat_id': chat_id, 'message_id': message_id}
    r = requests.post(url, data=data)
    return r

def process_message(chat_id, text):
    response = send_message(chat_id, "Обрабатываю запрос...")
    answer = handle_text_message(text)

    message_id = response.json().get("result", {}).get("message_id")
    delete_message(chat_id, message_id)

    send_message(chat_id, answer)

def process_photo(chat_id, file_id):
    response = send_message(chat_id, "Распознаю текст с изображения...")
    text = handle_photo_message(file_id)

    message_id = response.json().get("result", {}).get("message_id")
    delete_message(chat_id, message_id)

    process_message(chat_id, text)

def handler(event, context):
    update = json.loads(event['body'])
    print(update)
    message = update["message"]
    message_id = message["message_id"]
    chat_id = message["chat"]["id"]

    if "photo" in message:
        if "media_group_id" in message:
            send_message(chat_id, RESPONSES["several_photo"])
        else:
            photo = message.get("photo")
            file_id = photo[-1]["file_id"]
            process_photo(chat_id, file_id)

    elif "text" in message:
        text = message["text"]
        if text[0] == "/":
            if text in COMMANDS:
                send_message(chat_id, RESPONSES["description"])
            else:
                send_message(chat_id, RESPONSES["no_command"])
        else:
            process_message(chat_id, text)

    else:
        send_message(chat_id, RESPONSES["rules"])

    return {"statusCode": 200, "body": "Message processed."}
