import asyncio
import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from .api_client import APIClient
from .database import Database
from .models import Parameter

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Основная функция парсера"""
    logger.info("Запуск парсера характеристик товаров")
    
    # Валидация конфигурации
    api_key = os.getenv('MARKETPLACE_API_KEY')
    category_id = os.getenv('CATEGORY_ID')
    
    if not api_key or api_key == 'your_api_key_here':
        logger.error("API ключ не настроен")
        return
    
    if not category_id:
        logger.error("CATEGORY_ID не указан")
        return
    
    try:
        category_id_int = int(category_id)
    except ValueError:
        logger.error(f"Неверный формат CATEGORY_ID: {category_id}")
        return
    
    # Получение данных из API
    api_client = APIClient()
    json_data = api_client.get_marketplace_data(category_id_int)
    
    if not json_data:
        logger.error("Не удалось получить данные из API")
        return
    
    # Парсинг данных
    parameters = []
    if 'result' in json_data and 'parameters' in json_data['result']:
        for item in json_data['result']['parameters']:
            try:
                param = Parameter.from_dict(item)
                param.category_id = category_id_int
                parameters.append(param)
            except Exception as e:
                logger.warning(f"Ошибка парсинга параметра: {e}")
    
    if not parameters:
        logger.warning("Нет параметров для сохранения")
        return
    
    # Сохранение в БД
    try:
        db = Database()
        await db.save_parameters(parameters)
        logger.info("Парсер успешно завершил работу")
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении в БД: {e}")

if __name__ == "__main__":
    asyncio.run(main())
