#!/bin/bash

echo "🚀 Starting deployment process..."

# Проверка переменных окружения
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ ERROR: BOT_TOKEN is not set"
    exit 1
fi

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "❌ ERROR: DEEPSEEK_API_KEY is not set" 
    exit 1
fi

echo "✅ Environment variables check passed"

# Установка зависимостей
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Проверка синтаксиса Python
echo "🔍 Checking Python syntax..."
python -m py_compile main.py config.py utils/*.py features/*.py

if [ $? -ne 0 ]; then
    echo "❌ Python syntax check failed"
    exit 1
fi

echo "✅ Python syntax check passed"

# Запуск тестов (если есть)
if [ -f "test_bot.py" ]; then
    echo "🧪 Running tests..."
    python test_bot.py
fi

echo "🎉 Deployment preparation completed!"
echo "📊 Starting bot application..."
