from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



test_button_1 = InlineKeyboardButton(text="Тест", callback_data="test")
test_button_2 = InlineKeyboardButton(text="Тест2", callback_data="test2")

test_kb = InlineKeyboardMarkup(inline_keyboard=[
    [test_button_1],
    [test_button_2],
])
