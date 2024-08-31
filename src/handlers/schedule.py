from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from PIL import Image
from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import FSInputFile
from aiogram.handlers import MessageHandler
import asyncio

schedule_router = Router()


class ScheduleParser(MessageHandler):
    shedule_sheets = [
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[1]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[2]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[3]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[4]",
        "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[5]",
    ]
    def __init__(self, event: types.Message,  department_name, group_name):
        super().__init__(event)
        self.department_name = department_name
        self.group_name = group_name

    async def handle(self, bot: Bot, message: types.Message):
        await bot.send_message(message.from_user.id, "Делаю скриншоты, это займёт несколько минут")
        self._get_shedule_screenshots()

        document = FSInputFile(f"../data/{self.group_name}_schedule.png")
        await bot.send_document(message.from_user.id, document=document, caption="Расписание")

    async def _get_shedule_screenshots(self):
        options = Options()
        #options.add_argument("--headless")  # Включаем headless режим
        #options.add_argument("--disable-gpu")  # Отключаем использование GPU для ускорения
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get("https://sspi.ru/?alias=429")
        driver.set_window_size(1200, 1200)

        department_btn = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]").click()
        department_list_btn = driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[text()='{self.department_name}'']").click()
        await asyncio.sleep(5)
        group_btn = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]").click()
        await asyncio.sleep(5)
        group_list = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul")
        await asyncio.sleep(10)
        driver.execute_script("arguments[0].scrollBy(0, 560);", group_list)
        await asyncio.sleep(5)
        group_list_btn = driver.find_element(By.XPATH,
                                             f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul/li[text()='{self.group_name}']").click()
        await asyncio.sleep(5)
        next_week = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
        await asyncio.sleep(5)
        scr_num = 0
        for sheet in ScheduleParser.shedule_sheets:
            schedule = driver.find_element(By.XPATH, sheet)
            driver.execute_script("arguments[0].scrollIntoView();", schedule)
            scr_num += 1
            schedule.screenshot("../data/" + str(scr_num) + self.group_name +".png")
            await asyncio.sleep(3)
        self._make_a_collage()  # Создаем картинку с расписанием


    def _make_a_collage(self):
        image_files = [
            '../data/1schedule.png',
            '../data/2schedule.png',
            '../data/3schedule.png',
            '../data/4schedule.png',
            '../data/5schedule.png',
        ]

        images = [Image.open(image_file) for image_file in image_files]
        sizes = [image.size for image in images]
        total_height = sum(height for width, height in sizes)
        width = sizes[0][0]
        result_image = Image.new('RGB', (width, total_height))
        current_height = 0
        for image in images:
            result_image.paste(im=image, box=(0, current_height))
            current_height += image.size[1]
        result_image.save("../data/" + self.group_name + '_schedule.png')



    async def shedule_send_photo(self, message: types.Message, bot: Bot):
        document = FSInputFile('../data/full_schedule.png')
        await bot.send_document(message.from_user.id, document=document, caption="Расписание")



