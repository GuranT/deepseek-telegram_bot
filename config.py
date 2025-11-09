import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env файла

class Config:
    # API ключи
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    
    # Настройки приложения
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    MAX_REQUESTS_PER_MINUTE = int(os.environ.get('MAX_REQUESTS_PER_MINUTE', '10'))
    
    # Настройки DeepSeek
    API_URL = "https://api.deepseek.com/chat/completions"
    MODEL = "deepseek-chat"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
    # Настройки бота
    MAX_HISTORY_LENGTH = 8
    REQUEST_TIMEOUT = 30
    MAX_MESSAGE_LENGTH = 4096
    
    # Системный промпт
    SYSTEM_PROMPT = """Ты полезный AI-ассистент в Telegram. Отвечай на русском языке.
Будь кратким, информативным и полезным. Форматируй ответы с помощью Markdown."""
    
    @classmethod
    def validate_config(cls):
        """Проверка конфигурации"""
        errors = []
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN не установлен")
        if not cls.DEEPSEEK_API_KEY:
            errors.append("DEEPSEEK_API_KEY не установлен")
        
        # Логируем конфигурацию (без секретов)
        logger.info(f"Config validated: LOG_LEVEL={cls.LOG_LEVEL}, REQUESTS_PER_MINUTE={cls.MAX_REQUESTS_PER_MINUTE}")
        return errors
