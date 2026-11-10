"""
Конфигурация трендвотчера
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Firebase
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Настройки
IMPORTANCE_THRESHOLD = int(os.getenv('IMPORTANCE_THRESHOLD', '3'))

# Конкуренты и их источники
COMPETITORS = {
    'Яндекс Практикум': {
        'sitemap': 'https://practicum.yandex.ru/sitemap.xml',
        'blog': 'https://practicum.yandex.ru/blog/',
    },
    'Skillfactory': {
        'sitemap': 'https://skillfactory.ru/sitemap.xml',
        'blog': 'https://blog.skillfactory.ru/',
    },
    'Hexlet': {
        'blog': 'https://ru.hexlet.io/blog',
    },
    'Netology': {
        'sitemap': 'https://netology.ru/sitemap.xml',
        'blog': 'https://netology.ru/blog',
    },
    'GeekBrains': {
        'sitemap': 'https://geekbrains.ru/sitemap.xml',
        'blog': 'https://geekbrains.ru/posts',
    },
}
