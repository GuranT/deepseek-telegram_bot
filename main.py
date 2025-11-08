import os
import logging
import telebot
import requests
import json

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

# Хранилище истории чата
user_histories = {}

def ask_deepseek(user_id, question):
    """Функция для запроса к DeepSeek API"""
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    # Получаем историю пользователя
    if user_id not in user_histories:
        user_histories[user_id] = []
    
    history = user_histories[user_id]
    
    # Формируем сообщения
    messages = [
        {"role": "system", "content": "Ты полезный AI-ассистент. Отвечай на русском языке."}
    ]
    
    # Добавляем историю
    messages.extend(history[-6:])  # Последние 3 пары сообщений
    
    # Добавляем текущий вопрос
    messages.append({"role": "user", "content": question})
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        # Обновляем историю
        user_histories[user_id].extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ])
        
        # Ограничиваем размер истории
        if len(user_histories[user_id]) > 10:
            user_histories[user_id] = user_histories[user_id][-10:]
        
        return answer
        
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🤖 *DeepSeek AI Assistant* 

Привет! Я AI-помощник на основе DeepSeek.

Просто напишите ваш вопрос, и я помогу!
    
/help - помощь
/clear - очистить историю
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
🆘 *Помощь*

• Просто напишите вопрос
• Бот запоминает контекст
• Используйте /clear чтобы очистить историю
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_history(message):
    user_id = message.from_user.id
    if user_id in user_histories:
        user_histories[user_id] = []
    bot.reply_to(message, "✅ История очищена!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id
        user_text = message.text
        
        # Показываем индикатор набора
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Получаем ответ от DeepSeek
        answer = ask_deepseek(user_id, user_text)
        
        # Отправляем ответ
        bot.reply_to(message, answer)
                
    except Exception as e:
        bot.reply_to(message, "❌ Ошибка, попробуйте еще раз")

if __name__ == '__main__':
    print("🚀 Бот запущен и готов к работе!")
    bot.infinity_polling()
