from telegrambot.bot import TestBot, TelegramBot
from typing import Union


def validate_file(name: str, verify: bool) -> None:
    pass


def get_bot(name: str, is_token: bool, file: str) -> Union[TestBot, TelegramBot]:
    pass


def get_chat_id(name: str, is_id: bool, file: str) -> str:
    pass


def send_message(
        bot: str,
        is_token: bool,
        bot_file: str,
        chat: str,
        is_id: bool,
        chat_file: str,
        message: str,
) -> None:
    validate_file(bot_file, is_token)
    validate_file(chat_file, is_id)

    telegram_bot = get_bot(bot, is_token, bot_file)
    chat_id = get_chat_id(chat, is_id, chat_file)
    success, status_code, message = telegram_bot.send_message(message, chat_id)
    if not success:
        print(f"Failed to send message. Status code {status_code}")
        return
    print(f"Message send successfully: {message}")


def send_photo(
        bot: str,
        is_token: bool,
        bot_file: str,
        chat: str,
        is_id: bool,
        chat_file: str,
        photo_path: str,
        caption: str = ""
) -> None:
    validate_file(bot_file, is_token)
    validate_file(chat_file, is_id)
    validate_file(photo_path, True)

    telegram_bot = get_bot(bot, is_token, bot_file)
    chat_id = get_chat_id(chat, is_id, chat_file)
    success, status_code = telegram_bot.send_photo(photo_path, chat_id, caption)
    if not success:
        print(f"Failed to send photo. Status code {status_code}")
        return
    print(f"Photo send successfully: {photo_path}")


def get_updates(
        bot: str,
        is_token: bool,
        bot_file: str,
) -> None:
    telegram_bot = get_bot(bot, is_token, bot_file)
    success, status_code, updates = telegram_bot.get_updates()
    if not success:
        print(f"Failed to get updates. Status code {status_code}")
        return
    print(f"Bot updates: {updates}")
