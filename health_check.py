from flask import Flask, jsonify
import threading
import logging
from monitoring import MetricsCollector

app = Flask(__name__)
metrics_collector = MetricsCollector()

@app.route('/health')
def health_check():
    """Endpoint для проверки здоровья"""
    return jsonify({"status": "healthy", "service": "deepseek-bot"})

@app.route('/metrics')
def get_metrics():
    """Endpoint для метрик"""
    stats = metrics_collector.get_stats()
    return jsonify(stats)

@app.route('/')
def home():
    return "🤖 DeepSeek Telegram Bot is running!"

def run_health_server():
    """Запуск HTTP сервера для мониторинга"""
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        logging.error(f"Health server error: {e}")

# В main.py добавьте:
def main():
    # ... существующий код ...
    
    # Запуск health check сервера в отдельном потоке
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # ... остальной код ...
