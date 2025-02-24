from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button1 = InlineKeyboardButton(text="МД-21-о", callback_data="ФИФ: МД-21-о")
button2 = InlineKeyboardButton(text="МД-22-о", callback_data="ФИФ: МД-22-о")
button3 = InlineKeyboardButton(text="МД-23-о", callback_data="ФИФ: МД-23-о")
button4 = InlineKeyboardButton(text="МД-24-о", callback_data="ФИФ: МД-24-о")

group_kb = InlineKeyboardMarkup(inline_keyboard=[
    [button1, button2],
    [button3, button4],
])

test_button_1 = InlineKeyboardButton(text="Тест", callback_data="test")
test_button_2 = InlineKeyboardButton(text="Тест2", callback_data="test2")

test_kb = InlineKeyboardMarkup(inline_keyboard=[
    [test_button_1],
    [test_button_2],
])











