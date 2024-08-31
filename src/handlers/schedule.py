import os
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image

from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import FSInputFile

from keyboards.inline_group_kb import group_kb
from .departments_list import departments


schedule_router = Router()

@schedule_router.message(Command(commands=["Расписание"]))
async def send_group_keyboard(message: types.Message, bot: Bot):
    await message.answer(text="Выбери группу", reply_markup=group_kb)







@schedule_router.callback_query(lambda callback: callback.data.split(": ")[0] in departments)
async def process_callback(callback_query: types.CallbackQuery, bot: Bot):
    print("Поймал")
    # Получаем данные из callback_data
    department_name, group_name = callback_query.data.split(": ")

    await bot.answer_callback_query(callback_query.id, text=f'Вы выбрали группу: {group_name}')

    # Вызываем функцию для отправки расписания
    await send_schedule(callback_query.message, department_name, group_name)



async def send_schedule(message: types.Message, department_name: str, group_name: str, bot: Bot):
   #await message.answer(text="Выбери группу", reply_markup=None)  # Уберите клавиатуру, если она не нужна

    await bot.send_message(chat_id=message.from_user.id, text="Делаю скриншоты, это займёт несколько минут")

    # Используем переданные значения
    parser = ScheduleParser(department_name, group_name)
    await parser._get_shedule_screenshots()

    document = FSInputFile(f'../data/{group_name}_schedule.png')
    await bot.send_document(message.from_user.id, document=document, caption="Расписание")


class ScheduleParser():
    schedule_sheets = [
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[1]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[2]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[3]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[4]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[5]",
    ]

    def __init__(self, department_name, group_name):
        self.department_name = department_name
        self.group_name = group_name

    async def _get_shedule_screenshots(self):
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
        next_week = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
        await asyncio.sleep(5)
        scr_num = 0
        for sheet in ScheduleParser.schedule_sheets:
            schedule = driver.find_element(By.XPATH, sheet)
            driver.execute_script("arguments[0].scrollIntoView();", schedule)
            scr_num += 1
            schedule.screenshot("../data/" + str(scr_num) + self.group_name +".png")
            await asyncio.sleep(3)
        self._make_a_collage()  # Создаем картинку с расписанием

    def _make_a_collage(self):
        # Используем list comprehension для создания списка имен файлов
        image_files = [f'../data/{scr_num}{self.group_name}.png' for scr_num in range(1, 6)]

        # Открываем изображения
        images = [Image.open(image_file) for image_file in image_files]
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
            if os.path.exists(image_file):
                os.remove(image_file)




