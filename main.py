import os
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Импорт наших модулей
from config import Config
from utils.helpers import setup_logging, send_large_message, get_user_info, safe_truncate
from utils.deepseek_api import DeepSeekAPI
from security import SecurityManager
from monitoring import MetricsCollector

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

# Инициализация компонентов
deepseek_api = DeepSeekAPI()
security_manager = SecurityManager()
metrics_collector = MetricsCollector()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_info = get_user_info(update)
    logger.info(f"User {user_info} started the bot")
    
    welcome_text = """
🤖 *DeepSeek AI Assistant*

Добро пожаловать! Я ваш умный помощник на основе AI.

*Что я умею:*
• 💬 Отвечать на любые вопросы
• 💻 Помогать с программированием
• 📚 Объяснять сложные темы
• 🌐 Переводить тексты
• 💡 Генерировать идеи

*Команды:*
/start - Запуск бота
/help - Помощь и инструкции
/clear - Очистить историю диалога
/info - Информация о боте
/stats - Статистика использования

Просто напишите ваш вопрос!
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    stats = metrics_collector.get_stats()
    
    if not stats:
        await update.message.reply_text("📊 Статистика пока недоступна")
        return
    
    stats_text = f"""
📊 *Статистика бота*

*Общая статистика:*
• Всего запросов: {stats['total_requests']}
• Успешных: {stats['successful_requests']}
• Ошибок: {stats['failed_requests']}
• Успешность: {stats['success_rate']:.1f}%

*Производительность:*
• Среднее время ответа: {stats['avg_processing_time']:.2f}с
• Время работы: {stats['uptime_minutes']:.1f} минут

*Ваш ID:* {update.effective_user.id}
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    user_id = update.effective_user.id
    user_info = get_user_info(update)
    
    start_time = time.time()
    success = False
    
    try:
        # Проверка безопасности
        if not security_manager.check_rate_limit(user_id):
            await update.message.reply_text("⚠️ Слишком много запросов. Подождите минуту.")
            return
        
        if security_manager.contains_malicious_content(user_message):
            await update.message.reply_text("❌ Сообщение содержит подозрительный контент.")
            logger.warning(f"Malicious content detected from {user_info}")
            return
        
        # Очистка входных данных
        sanitized_message = security_manager.sanitize_input(user_message)
        
        logger.info(f"Message from {user_info}: {safe_truncate(sanitized_message)}")
        
        # Показываем индикатор набора
        await update.message.chat.send_action(action="typing")
        
        # Получаем ответ от DeepSeek
        answer = deepseek_api.ask_deepseek(user_id, sanitized_message)
        success = True
        
        # Отправляем ответ
        await send_large_message(context, update.effective_chat.id, answer)
        
        logger.info(f"Response sent to {user_info}")
        
    except Exception as e:
        logger.error(f"Error processing message from {user_info}: {e}")
        error_text = "❌ Произошла непредвиденная ошибка. Попробуйте позже."
        await update.message.reply_text(error_text)
    finally:
        # Записываем метрики
        processing_time = time.time() - start_time
        metrics_collector.record_request(user_id, processing_time, success)

# Добавьте новый обработчик в main()
def main():
    """Основная функция запуска бота"""
    # ... существующий код ...
    
    # Добавьте новый обработчик команд
    application.add_handler(CommandHandler("stats", stats_command))
    
    # ... остальной код ...
