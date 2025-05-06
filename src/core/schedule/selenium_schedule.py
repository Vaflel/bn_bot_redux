import os
import asyncio
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



class SeleniumScheduleParser():
    def __init__(self, department_name: str, group_name: str):
        self.department_name = department_name
        self.group_name = group_name

    async def get_image(self):
        await self._get_shedule_screenshots()

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
        await asyncio.sleep(5)
        driver.execute_script("arguments[0].scrollBy(0, 560);", group_list)
        await asyncio.sleep(5)
        group_list_btn = driver.find_element(By.XPATH,
                                             value=f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div[2]/ul/li[text()='{self.group_name}']").click()
        await asyncio.sleep(5)
        #next_week = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[4]/button[2]").click()
        #await asyncio.sleep(5)
        week_schedule = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[5]/div")
        day_schedule: list = week_schedule.find_elements(By.TAG_NAME, 'div')
        screenshot_num = 0
        for day in day_schedule:
            driver.execute_script("arguments[0].scrollIntoView();", day)
            screenshot_num += 1
            day.screenshot("../data/" + str(screenshot_num) + self.group_name +".png")
            await asyncio.sleep(3)
        self._make_a_collage()  # Создаем картинку с расписанием
        driver.close()

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

if __name__ == "__main__":
    async def main():
        parser = SeleniumScheduleParser(department_name="Факультет искусств и физической культуры", group_name="МД-22-о")
        await parser._get_shedule_screenshots()

    asyncio.run(main())