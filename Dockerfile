# Используем официальный образ Python 3.12 на базе slim для уменьшения размера
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
# Добавляем --no-cache-dir для минимизации размера кэша
# Обновляем pip и устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
# .dockerignore исключит ненужные файлы, такие как .env, __pycache__ и т.д.
COPY . .

# Указываем команду для запуска бота
CMD ["python", "-m", "SMPBot"]