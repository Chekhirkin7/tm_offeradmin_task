# Використовуємо базовий образ Python
FROM python:3.12-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо всі файли з вашої локальної машини в контейнер
COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./nginx /app/nginx

# Встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Вказуємо команду, яка запускає ваш застосунок
CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "main:app"]