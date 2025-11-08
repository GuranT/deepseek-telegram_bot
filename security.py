import re
import logging
from typing import Set
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class SecurityManager:
    def __init__(self):
        # Кэш для ограничения запросов
        self.rate_limit_cache = TTLCache(maxsize=10000, ttl=60)  # 60 секунд
        self.max_requests_per_minute = 10
        
        # Запрещенные паттерны
        self.malicious_patterns = [
            r"(?i)(password|token|key|secret).*[\"': ]*[a-zA-Z0-9]{10,}",
            r"(?i)(drop|delete|update|insert).*(table|database|user)",
            r"(?i)(http|https|ftp)://[^\s]+",
        ]
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Проверка ограничения запросов"""
        current = self.rate_limit_cache.get(user_id, 0)
        if current >= self.max_requests_per_minute:
            return False
        self.rate_limit_cache[user_id] = current + 1
        return True
    
    def sanitize_input(self, text: str) -> str:
        """Очистка входных данных"""
        # Удаляем потенциально опасные символы
        sanitized = re.sub(r'[<>{}`]', '', text)
        # Обрезаем длину
        return sanitized[:2000]
    
    def contains_malicious_content(self, text: str) -> bool:
        """Проверка на вредоносный контент"""
        for pattern in self.malicious_patterns:
            if re.search(pattern, text):
                return True
        return False
