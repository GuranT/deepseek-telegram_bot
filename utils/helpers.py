import logging
from typing import List
from telegram import Update
from telegram.ext import ContextTypes
from config import Config

logger = logging.getLogger(__name__)

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )

def split_message(text: str, max_length: int = None) -> List[str]:
    """Разделение длинного сообщения на части"""
    if max_length is None:
        max_length = Config.MAX_MESSAGE_LENGTH
    
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        
        # Ищем место для разделения
        split_pos = text.rfind('\n\n', 0, max_length)
        if split_pos == -1:
            split_pos = text.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = text.rfind('. ', 0, max_length)
        if split_pos == -1:
            split_pos = text.rfind(' ', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
            
        parts.append(text[:split_pos].strip())
        text = text[split_pos:].strip()
        
    return parts

async def send_large_message(context: ContextTypes.DEFAULT_TYPE, 
                           chat_id: int, 
                           text: str):
    """Отправка длинного сообщения частями"""
    parts = split_message(text)
    for i, part in enumerate(parts):
        # Добавляем индикатор продолжения для частей кроме первой
        if i > 0:
            part = f"📄 *[Продолжение {i+1}/{len(parts)}]*\n\n{part}"
        await context.bot.send_message(
            chat_id=chat_id, 
            text=part,
            parse_mode='Markdown'
        )

def get_user_info(update: Update) -> str:
    """Получение информации о пользователе"""
    user = update.effective_user
    return f"{user.first_name} {user.last_name or ''} (@{user.username or 'no_username'})"

def safe_truncate(text: str, max_length: int = 100) -> str:
    """Безопасное обрезание текста для логов"""
    return text[:max_length] + "..." if len(text) > max_length else text
