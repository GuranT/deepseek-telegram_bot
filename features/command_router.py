import logging
from telegram import Update
from telegram.ext import ContextTypes
from typing import Dict, Callable, Any

logger = logging.getLogger(__name__)

class CommandRouter:
    """Маршрутизатор команд с плагинами"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self._register_default_commands()
    
    def _register_default_commands(self):
        """Регистрация стандартных команд"""
        self.commands.update({
            'start': self._start_command,
            'help': self._help_command,
            'clear': self._clear_command,
            'info': self._info_command,
            'stats': self._stats_command,
            'settings': self._settings_command,
            'feedback': self._feedback_command
        })
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return """
🤖 *DeepSeek AI Assistant*

Добро пожаловать! Я ваш умный помощник.

*Основные команды:*
/help - Справка по использованию
/clear - Очистить историю диалога  
/stats - Статистика использования
/settings - Настройки бота
/feedback - Оставить отзыв

Просто напишите ваш вопрос!
"""
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return """
🆘 *Справка по использованию*

*Как работать с ботом:*
1. Просто напишите вопрос
2. Используйте команды для управления
3. Бот запоминает контекст диалога

*Советы для лучших ответов:*
• Будьте конкретны в вопросах
• Для кода указывайте язык программирования
• Используйте /clear для очистки истории
"""
    
    async def _clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return "✅ История диалога очищена!"
    
    async def _info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return """
📊 *Информация о боте*

*Версия:* 4.0 (Professional)
*Модель:* DeepSeek Chat
*Статус:* ✅ Активен

*Особенности:*
• Умное управление контекстом
• Продвинутая безопасность
• Мониторинг производительности
• Автоматическое масштабирование
"""
    
    async def _stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return "📊 Статистика будет доступна в следующем обновлении"
    
    async def _settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return """
⚙️ *Настройки бота*

*Текущие настройки:*
• Длина контекста: 10 сообщений
• Макс. токены: 4000
• Температура: 0.7

Используйте /clear для сброса настроек.
"""
    
    async def _feedback_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        return """
💬 *Обратная связь*

Нашли ошибку? Есть предложения?
Отправьте сообщение с пометкой "Отзыв:" в начале.

Пример: "Отзыв: предложение по улучшению..."
"""
    
    def register_command(self, name: str, handler: Callable):
        """Регистрация новой команды"""
        self.commands[name] = handler
        logger.info(f"Registered new command: /{name}")
    
    async def execute_command(self, command: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Выполнение команды"""
        if command not in self.commands:
            return f"❌ Команда /{command} не найдена. Используйте /help для списка команд."
        
        try:
            return await self.commands[command](update, context)
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return "❌ Ошибка выполнения команды."
