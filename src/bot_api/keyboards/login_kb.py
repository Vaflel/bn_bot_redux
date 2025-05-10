from aiogram.utils.keyboard import InlineKeyboardBuilder

departments_short_names = {
    "Аспирантура": "Аспирантура",
    "Гуманитарный факультет": "Гуманитарный",
    "Психолого-педагогический факультет": "Псих-пед",
    "Факультет дефектологии и естественно-научного образования": "Дефектологии",
    "Факультет дополнительных образовательных программ": "ДОП",
    "Факультет искусств и физической культуры": "Искусств",
    "Факультет среднего профессионального образования": "СПО",

}

login_keyboard = InlineKeyboardBuilder()
for full_name, short_name in departments_short_names.items():
    login_keyboard.button(text=short_name, callback_data=short_name)
login_keyboard.adjust(1)
login_keyboard = login_keyboard.as_markup()


