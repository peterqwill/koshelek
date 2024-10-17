# Используем официальный образ Python в качестве базового
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы
COPY . .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Команда для запуска приложения
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
