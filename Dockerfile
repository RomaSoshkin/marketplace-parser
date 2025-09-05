FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY scripts/ ./scripts/

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

CMD ["python", "-m", "src.marketplace_parser.main"]
