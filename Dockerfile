FROM python:3.11-slim

# Создаем директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

# Запуск бота
CMD ["python", "bot.py"]
