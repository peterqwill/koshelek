# Используем официальный образ Python
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["gunicorn", "-b", "0.0.0.0:8080", "function:handler"]
