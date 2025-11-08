import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Импорт наших модулей
from config import Config
from utils.helpers import setup_logging, send_large_message, get_user_info, safe_truncate
from utils.deepseek_api import DeepSeekAPI

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

# Инициализация API
deepseek_api = DeepSeekAPI()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_info = get_user_info
