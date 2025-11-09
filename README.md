# 🤖 DeepSeek Telegram Bot

Профессиональный Telegram бот с интеграцией DeepSeek AI.

## 🚀 Быстрый старт

1. Клонируйте репозиторий
2. Настройте переменные окружения в `render.yaml`
3. Deploy на Render.com

## ⚙️ Настройка

### Переменные окружения:
- `BOT_TOKEN` - Токен Telegram бота от @BotFather
- `DEEPSEEK_API_KEY` - API ключ от platform.deepseek.com
- `LOG_LEVEL` - Уровень логирования (INFO, DEBUG, ERROR)

### Команды:
- `/start` - Запуск бота
- `/help` - Справка
- `/clear` - Очистить историю
- `/stats` - Статистика
- `/settings` - Настройки

## 🛠 Разработка

### Локальная разработка:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
