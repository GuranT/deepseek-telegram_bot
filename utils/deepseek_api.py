import requests
import logging
from typing import List, Dict, Optional
from cachetools import TTLCache
from config import Config

logger = logging.getLogger(__name__)

class DeepSeekAPI:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_url = Config.API_URL
        self.model = Config.MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Кэш для хранения истории (TTL 1 час)
        self.user_cache = TTLCache(maxsize=1000, ttl=3600)
    
    def _build_messages(self, user_id: int, question: str) -> List[Dict]:
        """Построение списка сообщений с историей"""
        messages = [{"role": "system", "content": Config.SYSTEM_PROMPT}]
        
        # Добавляем историю из кэша
        history = self.user_cache.get(user_id, [])
        messages.extend(history[-Config.MAX_HISTORY_LENGTH:])
        
        # Добавляем текущий вопрос
        messages.append({"role": "user", "content": question})
        
        return messages
    
    def _update_history(self, user_id: int, question: str, answer: str):
        """Обновление истории диалога"""
        history = self.user_cache.get(user_id, [])
        history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ])
        # Ограничиваем размер истории
        self.user_cache[user_id] = history[-Config.MAX_HISTORY_LENGTH:]
    
    def ask_deepseek(self, user_id: int, question: str) -> str:
        """Основной метод для запроса к API"""
        if not self.api_key:
            raise ValueError("DeepSeek API ключ не установлен")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = self._build_messages(user_id, question)
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 429:
                return "⚠️ Слишком много запросов. Подождите немного."
            elif response.status_code == 401:
                return "❌ Ошибка авторизации API. Проверьте API ключ."
            elif response.status_code == 403:
                return "❌ Доступ запрещен. Проверьте права API ключа."
            
            response.raise_for_status()
            
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            # Обновляем историю
            self._update_history(user_id, question, answer)
            
            return answer
            
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout for user {user_id}")
            return "⏰ Таймаут запроса. Попробуйте позже."
        except requests.exceptions.ConnectionError:
            logger.error("Connection error to DeepSeek API")
            return "🔌 Ошибка соединения. Проверьте интернет."
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return f"❌ Ошибка API: {response.status_code}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "❌ Внутренняя ошибка. Попробуйте позже."
    
    def clear_history(self, user_id: int):
        """Очистка истории пользователя"""
        if user_id in self.user_cache:
            del self.user_cache[user_id]
