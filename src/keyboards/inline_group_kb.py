from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button1 = InlineKeyboardButton(text="МД-21-о", callback_data="Факультет искусств и физической культуры: МД-21-о")
button2 = InlineKeyboardButton(text="МД-22-о", callback_data="Факультет искусств и физической культуры: МД-22-о")
button3 = InlineKeyboardButton(text="МД-23-о", callback_data="Факультет искусств и физической культуры: МД-23-о")
button4 = InlineKeyboardButton(text="МД-24-о", callback_data="Факультет искусств и физической культуры: МД-24-о")

group_kb = InlineKeyboardMarkup(inline_keyboard=[
    [button1, button2],
    [button3, button4]
])













