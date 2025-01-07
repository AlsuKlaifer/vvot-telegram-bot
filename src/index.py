import requests
import os
import json

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

COMMANDS = ["/start", "/help"]

RESPONSES = {
    "description": (
        "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине \"Операционные системы\".\n"
        "Пришлите мне фотографию с вопросом или наберите его текстом."
    ),
    "several_photo": "Я могу обработать только одну фотографию.",
    "rules": "Я могу обработать только текстовое сообщение или фотографию.",
    "no_command": "Я не знаю такой команды. Попробуйте /start или /help."
}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    r = requests.post(url=url, data=data)
    return r

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
            send_message(chat_id, "Получил фото.")

    elif "text" in message:
        text = message["text"]
        if text[0] == "/":
            if text in COMMANDS:
                send_message(chat_id, RESPONSES["description"])
            else:
                send_message(chat_id, RESPONSES["no_command"])
        else:
            send_message(chat_id, text)

    else:
        send_message(chat_id, RESPONSES["rules"])

    return {"statusCode": 200, "body": "Message processed."}
