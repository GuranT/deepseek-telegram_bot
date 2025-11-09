import os
import logging
import telebot
import requests

# ===== КОНФИГУРАЦИЯ =====
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')

print("🔧 Проверка переменных...")
print(f"BOT_TOKEN: {'✅' if BOT_TOKEN else '❌'}")
print(f"DEEPSEEK_API_KEY: {'✅' if DEEPSEEK_API_KEY else '❌'}")

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    exit(1)

if not DEEPSEEK_API_KEY:
    print("❌ ОШИБКА: DEEPSEEK_API_KEY не установлен!")
    exit(1)

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🤖 *DeepSeek AI Assistant*

Бот успешно запущен! 🎉

Просто напишите ваш вопрос, и я помогу!
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['test'])
def test_command(message):
    """Тестовая команда для проверки работы"""
    bot.reply_to(message, "✅ Бот работает корректно!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        
        # Показываем индикатор набора
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Простой ответ для тестирования
        if user_text.lower() == 'привет':
            answer = "Привет! Я работаю! 🎉"
        else:
            answer = f"Вы написали: {user_text}\n\nБот работает, DeepSeek API будет подключено позже."
        
        bot.reply_to(message, answer)
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка, попробуйте еще раз")

if __name__ == '__main__':
    print("🚀 Бот запускается...")
    print("✅ Все зависимости загружены")
    print("📍 Ожидание сообщений...")
    bot.infinity_polling()
