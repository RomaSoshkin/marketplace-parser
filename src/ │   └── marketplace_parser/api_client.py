import requests
import os
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Клиент для работы с API маркетплейса"""
    
    def __init__(self):
        self.api_key = os.getenv('MARKETPLACE_API_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'https://api.marketplace.example')
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', 30))
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('RETRY_DELAY', 5))
    
    def get_marketplace_data(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Получение данных о параметрах категории"""
        url = f"{self.base_url}/category/{category_id}/parameters"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, headers=headers, json={}, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Попытка {attempt + 1}/{self.max_retries} не удалась: {e}")
                if attempt < self.max_retries - 1:
                    sleep_time = self.retry_delay * (2 ** attempt)
                    logger.info(f"Повторная попытка через {sleep_time} секунд...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"Все {self.max_retries} попыток не удались")
                    return None
