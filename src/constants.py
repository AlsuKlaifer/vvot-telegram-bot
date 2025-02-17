import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

YANDEX_GPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

SERVICE_ACCOUNT_API_KEY = os.getenv("SERVICE_ACCOUNT_API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_INSTRUCTIONS_FILE_KEY = os.getenv("BUCKET_INSTRUCTIONS_FILE_KEY")

RESPONSES = {
    "description": (
        "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине \"Операционные системы\".\n"
        "Пришлите мне фотографию с вопросом или наберите его текстом."
    ),
    "several_photo": "Я могу обработать только одну фотографию.",
    "rules": "Я могу обработать только текстовое сообщение или фотографию.",
    "no_command": "Я не знаю такой команды. Попробуйте /start или /help.",
    "ocr_recognition_error": "Я не могу обработать эту фотографию.",
    "answer_error": "Я не смог подготовить ответ на ваш запрос."
}