terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  cloud_id = "b1g71e95h51okii30p25"
  folder_id = var.FOLDER_ID
  service_account_key_file = "./keys/key.json"
}

resource "yandex_function" "func" {
  name = "func-hw1-telegram-bot"
  user_hash = archive_file.zip.output_sha256
  runtime = "python312"
  entrypoint = "index.handler"
  memory = 128
  execution_timeout = 50

  environment = {
    "TELEGRAM_BOT_TOKEN" = var.TELEGRAM_BOT_TOKEN
    "FOLDER_ID" = var.FOLDER_ID
    "SERVICE_ACCOUNT_API_KEY" = yandex_iam_service_account_api_key.sa_api_key.secret_key
  }

  content {
    zip_filename = archive_file.zip.output_path
  }
}

resource "yandex_iam_service_account_api_key" "sa_api_key" {
  service_account_id = var.SERVICE_ACCOUNT_ID
}

output "func_url" {
  value = "https://functions.yandexcloud.net/${yandex_function.func.id}"
}

variable "TELEGRAM_BOT_TOKEN" {
  type = string
  description = "Ключ для бота в телеграме"
}

variable "SERVICE_ACCOUNT_ID" {
  type = string
  description = "Идентификатор сервисного аккаунта"
}

variable "FOLDER_ID" {
  type = string
  default = "Идентификатор папки"
}

resource "archive_file" "zip" {
  type = "zip"
  output_path = "telegram_bot.zip"
  source_dir = "./src"
}