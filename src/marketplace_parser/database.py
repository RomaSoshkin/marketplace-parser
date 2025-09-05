import asyncpg
import os
import json
from typing import List, Optional
from .models import Parameter
import logging

logger = logging.getLogger(__name__)

class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self):
        self.db_config = {
            'user': os.getenv('DB_USER', 'db_user'),
            'password': os.getenv('DB_PASSWORD', 'secure_password_123'),
            'database': os.getenv('DB_NAME', 'marketplace_db'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432))
        }
    
    async def connect(self) -> asyncpg.Connection:
        """Установка соединения с БД"""
        return await asyncpg.connect(**self.db_config)
    
    async def save_parameters(self, parameters: List[Parameter]) -> None:
        """Сохранение параметров в базу данных"""
        if not parameters:
            logger.warning("Нет параметров для сохранения")
            return
        
        conn = None
        try:
            conn = await self.connect()
            
            query = """
                INSERT INTO marketplace_parameters 
                (param_id, name, description, required, values, category_id)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (param_id) DO NOTHING;
            """
            
            for param in parameters:
                values_json = json.dumps(param.values)
                await conn.execute(
                    query, 
                    param.param_id, 
                    param.name, 
                    param.description, 
                    param.required, 
                    values_json, 
                    param.category_id
                )
            
            logger.info(f"Успешно сохранено {len(parameters)} параметров")
            
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Ошибка базы данных: {e}")
            raise
        except Exception as e:
            logger.error(f"Общая ошибка: {e}")
            raise
        finally:
            if conn:
                await conn.close()
