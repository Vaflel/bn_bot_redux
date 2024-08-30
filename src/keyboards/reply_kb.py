from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard = [
        [
            KeyboardButton(text = "/Скриншот"),
            KeyboardButton(text = "/Расписание"),
        ]
    ]
    )