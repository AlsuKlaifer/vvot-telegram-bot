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
  folder_id = "b1gb87u00c1covc5ttqv"
  service_account_key_file = "./keys/key.json"
}

resource "yandex_function" "func" {
  name = "func-hw1-telegram-bot"
  user_hash = archive_file.zip.output_sha256
  runtime = "python312"
  entrypoint = "index.handler"
  memory = 128

  environment = {
    "TELEGRAM_BOT_TOKEN" = var.TELEGRAM_BOT_TOKEN
  }

  content {
    zip_filename = archive_file.zip.output_path
  }
}

output "func_url" {
  value = "https://functions.yandexcloud.net/${yandex_function.func.id}"
}

variable "TELEGRAM_BOT_TOKEN" {
  type = string
  description = "Ключ для бота в телеграме"
}

resource "archive_file" "zip" {
  type = "zip"
  output_path = "telegram_bot.zip"
  source_dir = "./src"
}