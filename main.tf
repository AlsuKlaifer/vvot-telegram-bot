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
  service_account_id = var.SERVICE_ACCOUNT_ID
  memory = 128
  execution_timeout = 50

  environment = {
    "TELEGRAM_BOT_TOKEN" = var.TELEGRAM_BOT_TOKEN
    "FOLDER_ID" = var.FOLDER_ID
    "SERVICE_ACCOUNT_API_KEY" = yandex_iam_service_account_api_key.sa_api_key.secret_key
    "BUCKET_NAME" = var.BUCKET_NAME
    "BUCKET_INSTRUCTIONS_FILE_KEY" = var.BUCKET_INSTRUCTIONS_FILE_KEY
  }

  content {
    zip_filename = archive_file.zip.output_path
  }

  mounts {
    name = var.BUCKET_NAME
    mode = "ro"
    object_storage {
      bucket = yandex_storage_bucket.instructions_bucket.bucket
    }
  }
}

resource "archive_file" "zip" {
  type = "zip"
  output_path = "telegram_bot.zip"
  source_dir = "./src"
}

resource "yandex_iam_service_account_api_key" "sa_api_key" {
  service_account_id = var.SERVICE_ACCOUNT_ID
}

output "func_url" {
  value = "https://functions.yandexcloud.net/${yandex_function.func.id}"
}

resource "yandex_storage_bucket" "instructions_bucket" {
  bucket = var.BUCKET_NAME
}

resource "yandex_storage_object" "gpt_instructions" {
  bucket = yandex_storage_bucket.instructions_bucket.id
  key    = var.BUCKET_INSTRUCTIONS_FILE_KEY
  source = "./instructions/instructions.txt"
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

variable "BUCKET_NAME" {
  type        = string
  description = "Название бакета"
}

variable "BUCKET_INSTRUCTIONS_FILE_KEY" {
  type        = string
  description = "Название файла с инструкцией внутри бакета"
}