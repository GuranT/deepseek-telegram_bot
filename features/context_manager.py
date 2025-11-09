import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class ContextManager:
    """Управление контекстом диалогов с продвинутыми функциями"""
    
    def __init__(self):
        # Кэш для хранения контекста (24 часа TTL)
        self.context_cache = TTLCache(maxsize=5000, ttl=86400)
        # Кэш для топиков диалогов
        self.topic_cache = TTLCache(maxsize=5000, ttl=3600)
    
    def extract_topic(self, message: str) -> str:
        """Извлечение темы из сообщения"""
        topics = {
            'programming': ['код', 'программир', 'python', 'javascript', 'функция', 'алгоритм'],
            'learning': ['объясни', 'как работает', 'что такое', 'учиться'],
            'translation': ['переведи', 'translat', 'язык'],
            'creative': ['придумай', 'идея', 'создай', 'напиши текст'],
            'analysis': ['проанализируй', 'разбери', 'объясни сложно']
        }
        
        message_lower = message.lower()
        for topic, keywords in topics.items():
            if any(keyword in message_lower for keyword in keywords):
                return topic
        return 'general'
    
    def enhance_system_prompt(self, user_id: int, topic: str) -> str:
        """Улучшение системного промпта на основе темы"""
        base_prompt = "Ты полезный AI-ассистент. Отвечай на русском языке."
        
        topic_prompts = {
            'programming': "Ты опытный программист. Давай чистый, рабочий код с объяснениями.",
            'learning': "Ты терпеливый учитель. Объясняй сложные темы просто и понятно.",
            'translation': "Ты профессиональный переводчик. Сохраняй смысл и стиль текста.",
            'creative': "Ты креативный писатель. Будь оригинальным и вдохновляющим.",
            'analysis': "Ты аналитик. Будь точным, логичным и структурированным."
        }
        
        return f"{base_prompt} {topic_prompts.get(topic, '')}"
    
    def manage_context(self, user_id: int, new_message: str, assistant_response: str) -> List[Dict]:
        """Управление контекстом диалога"""
        current_context = self.context_cache.get(user_id, [])
        topic = self.extract_topic(new_message)
        
        # Добавляем новое сообщение и ответ
        current_context.extend([
            {"role": "user", "content": new_message, "topic": topic, "timestamp": datetime.now().isoformat()},
            {"role": "assistant", "content": assistant_response, "topic": topic, "timestamp": datetime.now().isoformat()}
        ])
        
        # Ограничиваем размер контекста
        if len(current_context) > 20:  # 10 пар сообщений
            current_context = current_context[-20:]
        
        # Сохраняем обновленный контекст
        self.context_cache[user_id] = current_context
        self.topic_cache[user_id] = topic
        
        return current_context
    
    def get_conversation_summary(self, user_id: int) -> Optional[str]:
        """Получение сводки диалога"""
        context = self.context_cache.get(user_id, [])
        if not context:
            return None
        
        topics = set(msg.get('topic', 'general') for msg in context)
        user_messages = [msg['content'] for msg in context if msg['role'] == 'user']
        
        return f"Темы: {', '.join(topics)}. Сообщений: {len(user_messages)}"
