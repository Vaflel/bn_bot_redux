from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from PIL import Image
from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import FSInputFile
#from create_bot import bot
import asyncio

schedule_router = Router()

shedule_sheets = [
    "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[1]",
    "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[2]",
    "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[3]",
    "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[4]",
    "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div/div[5]",
]




@schedule_router.message(Command(commands=["Скриншот"]))
async def get_shedule_screenshots(message: types.Message, bot: Bot):
    await bot.send_message(message.from_user.id, text="Делаю скриншоты, это займёт несколько минут")

    options = Options()
    #options.add_argument("--headless")  # Включаем headless режим
    #options.add_argument("--disable-gpu")  # Отключаем использование GPU для ускорения
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://sspi.ru/?alias=429")
    driver.set_window_size(1200, 1200)

    department_btn = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]").click()
    department_list_btn = driver.find_element(By.XPATH,
                                              "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[7]").click()
    await asyncio.sleep(5)
    group_btn = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]").click()
    await asyncio.sleep(5)
    group_list = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul")
    await asyncio.sleep(10)
    driver.execute_script("arguments[0].scrollBy(0, 560);", group_list)
    await asyncio.sleep(5)
    group_list_btn = driver.find_element(By.XPATH,
                                         "/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul/li[9]").click()
    await asyncio.sleep(5)
    next_week = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
    await asyncio.sleep(5)
    scr_num = 0
    for sheet in shedule_sheets:
        schedule = driver.find_element(By.XPATH, sheet)
        driver.execute_script("arguments[0].scrollIntoView();", schedule)
        scr_num += 1
        schedule.screenshot("../data/" + str(scr_num) + "schedule.png")
        await asyncio.sleep(3)
    make_a_collage()  # Создаем картинку с расписанием
    await bot.send_message(message.from_user.id, text="Скриншоты готовы")


def make_a_collage():
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
    result_image.save("../data/" + 'full_schedule.png')


@schedule_router.message(Command(commands=["Расписание"]))
async def shedule_send_photo(message: types.Message, bot: Bot):
    document = FSInputFile('../data/full_schedule.png')
    await bot.send_document(message.from_user.id, document=document, caption="Расписание")



