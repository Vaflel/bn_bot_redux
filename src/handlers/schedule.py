import os
import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image

from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import FSInputFile

from keyboards.inline_group_kb import group_kb, test_kb
from .departments_list import departments, departments_short_names


schedule_router = Router()


@schedule_router.message(Command(commands=["Расписание"]))
async def send_department_keyboard(message: types.Message):
    # Создаем клавиатуру с выбором факультетов
    kb = InlineKeyboardBuilder()
    for full_name, short_name in departments_short_names.items():
        kb.button(text=short_name, callback_data=short_name)
    await message.answer("Выберите факультет:", reply_markup=kb.adjust(1).as_markup())

@schedule_router.callback_query(lambda c: c.data in departments_short_names.values())
async def send_group_keyboard(callback_query: types.CallbackQuery):
    short_name = callback_query.data  # Получаем краткое название факультета
    full_name = next(key for key, value in departments_short_names.items() if value == short_name)  # Получаем полное название факультета
    groups = departments[short_name]  # Получаем группы для выбранного факультета
    # Создаем клавиатуру с группами с использованием InlineKeyboardBuilder
    kb = InlineKeyboardBuilder()
    for group in groups:
        kb.button(text=f"{group}", callback_data=f"{short_name}_{group}")
    await callback_query.message.answer(f"Выберите группу для факультета {full_name}:", reply_markup=kb.adjust(2).as_markup())

# Обработчик для коллбэков групп
@schedule_router.callback_query(lambda c: '_' in c.data)
async def handle_group_selection(callback_query: types.CallbackQuery):
    short_name, group_name = callback_query.data.split('_')  # Разделяем данные коллбэка
    # Получаем полное название факультета
    department_name = next(key for key, value in departments_short_names.items() if value == short_name)
    await callback_query.answer(f"Вы выбрали группу: {group_name} факультета {department_name}, делаю скриншоты")
    # Используем переданные значения
    parser = ScheduleParser(department_name, group_name)
    await parser.get_shedule_screenshots()
    document = FSInputFile(f'../data/{group_name}_schedule.png')
    await callback_query.message.answer_document(document=document, caption="Расписание")

class ScheduleParser():
    schedule_sheets = [
        f"/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[{i}]"
        for i in range(1, 6)
    ]

    def __init__(self, department_name: str, group_name: str):
        self.department_name = department_name
        self.group_name = group_name

    async def get_shedule_screenshots(self):
        options = Options()
        #options.add_argument("--headless")  # Включаем headless режим
        #options.add_argument("--disable-gpu")  # Отключаем использование GPU для ускорения
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get("https://sspi.ru/?alias=429")
        driver.set_window_size(width=1200, height=1200)

        department_btn = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]").click()
        department_list_btn = driver.find_element(By.XPATH, value=f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[text()='{self.department_name}']").click()
        await asyncio.sleep(5)
        group_btn = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]").click()
        await asyncio.sleep(5)
        group_list = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul")
        await asyncio.sleep(10)
        driver.execute_script("arguments[0].scrollBy(0, 560);", group_list)
        await asyncio.sleep(5)
        group_list_btn = driver.find_element(By.XPATH,
                                             value=f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul/li[text()='{self.group_name}']").click()
        await asyncio.sleep(5)
        # next_week = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
        # await asyncio.sleep(5)
        week_schedule = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div")
        day_schedule: list = week_schedule.find_elements(By.TAG_NAME, 'div')
        screenshot_num = 0
        for day in day_schedule:
            driver.execute_script("arguments[0].scrollIntoView();", day)
            screenshot_num += 1
            day.screenshot("../data/" + str(screenshot_num) + self.group_name +".png")
            await asyncio.sleep(3)
        self._make_a_collage()  # Создаем картинку с расписанием

    def _make_a_collage(self):
        # Используем list comprehension для создания списка имен файлов
        #image_files = [f'../data/{scr_num}{self.group_name}.png' for scr_num in range(1, 6)]
        image_files = [f for f in os.listdir("../data/") if f.endswith(f'{self.group_name}.png')]
        # Если нужно, можно отсортировать файлы по номеру
        image_files.sort(key=lambda x: int(x.split(self.group_name)[0]))
        # Открываем изображения
        images = [Image.open(os.path.join("../data/", image_file)) for image_file in image_files]
        sizes = [image.size for image in images]
        total_height = sum(height for width, height in sizes)
        width = sizes[0][0]

        # Создаем новое изображение для коллажа
        result_image = Image.new('RGB', (width, total_height))
        current_height = 0

        # Пастим каждое изображение в коллаж
        for image in images:
            result_image.paste(im=image, box=(0, current_height))
            current_height += image.size[1]

        # Сохраняем итоговое изображение
        result_image.save(f"../data/{self.group_name}_schedule.png")

        # Удаляем промежуточные изображения
        for image_file in image_files:
            full_path = os.path.join("../data/", image_file)  # Создаем полный путь к файлу
            if os.path.exists(full_path):
                os.remove(full_path)


# class ScheduleParser():
#     schedule_sheets = [
#         f"/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[{i}]"
#         for i in range(1, 6)
#     ]
#
#     def __init__(self, department_name: str, group_name: str):
#         self.department_name = department_name
#         self.group_name = group_name
#
#     async def _get_shedule_screenshots(self):
#         options = Options()
#         #options.add_argument("--headless")  # Включаем headless режим
#         #options.add_argument("--disable-gpu")  # Отключаем использование GPU для ускорения
#         options.add_argument("--no-sandbox")
#
#         driver = webdriver.Chrome(options=options)
#         driver.get("https://sspi.ru/?alias=429")
#         driver.set_window_size(width=1200, height=1200)
#
#         department_btn = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]").click()
#         department_list_btn = driver.find_element(By.XPATH, value=f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[text()='{self.department_name}']").click()
#         await asyncio.sleep(5)
#         group_btn = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]").click()
#         await asyncio.sleep(5)
#         group_list = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul")
#         await asyncio.sleep(10)
#         driver.execute_script("arguments[0].scrollBy(0, 560);", group_list)
#         await asyncio.sleep(5)
#         group_list_btn = driver.find_element(By.XPATH,
#                                              value=f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul/li[text()='{self.group_name}']").click()
#         await asyncio.sleep(5)
#         # next_week = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
#         # await asyncio.sleep(5)
#         scr_num = 0
#         for sheet in ScheduleParser.schedule_sheets:
#             schedule = driver.find_element(By.XPATH, sheet)
#             driver.execute_script("arguments[0].scrollIntoView();", schedule)
#             scr_num += 1
#             schedule.screenshot("../data/" + str(scr_num) + self.group_name +".png")
#             await asyncio.sleep(3)
#         self._make_a_collage()  # Создаем картинку с расписанием
#
#     def _make_a_collage(self):
#         # Используем list comprehension для создания списка имен файлов
#         image_files = [f'../data/{scr_num}{self.group_name}.png' for scr_num in range(1, 6)]
#
#         # Открываем изображения
#         images = [Image.open(image_file) for image_file in image_files]
#         sizes = [image.size for image in images]
#         total_height = sum(height for width, height in sizes)
#         width = sizes[0][0]
#
#         # Создаем новое изображение для коллажа
#         result_image = Image.new('RGB', (width, total_height))
#         current_height = 0
#
#         # Пастим каждое изображение в коллаж
#         for image in images:
#             result_image.paste(im=image, box=(0, current_height))
#             current_height += image.size[1]
#
#         # Сохраняем итоговое изображение
#         result_image.save(f"../data/{self.group_name}_schedule.png")
#
#         # Удаляем промежуточные изображения
#         for image_file in image_files:
#             if os.path.exists(image_file):
#                 os.remove(image_file)

