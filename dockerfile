FROM python:3.12-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libfontconfig1

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копирование кода приложения
COPY . /app/src
WORKDIR /app

# Запуск приложения
CMD ["python", "main.py"]


