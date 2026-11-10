# 🚀 Быстрый старт Трендвотчера

## Шаг 1: Получите учётные данные (15 минут)

### 1.1 Firebase (5 минут)
1. Перейдите на https://console.firebase.google.com/
2. Создайте проект `trendwatcher-hw`
3. Включите Firestore Database (Production mode, europe-west3)
4. Скачайте Service Account JSON: Settings → Service accounts → Generate new private key
5. Сохраните как `firebase-credentials.json` в корень проекта

**Firestore Rules:**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /events/{eventId} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

### 1.2 DeepSeek API (5 минут)
1. Перейдите на https://platform.deepseek.com/
2. Зарегистрируйтесь
3. Пополните баланс ($5 минимум, хватит на несколько месяцев)
4. Создайте API ключ
5. Скопируйте ключ

### 1.3 Telegram Bot (5 минут)
1. Откройте [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Назовите бота (например, `Trendwatcher Bot`)
4. Укажите username (например, `trendwatcher_hw_bot`)
5. Скопируйте токен бота
6. Отправьте боту любое сообщение
7. Откройте `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
8. Найдите `"chat":{"id": 123456}` и скопируйте chat ID

---

## Шаг 2: Настройте проект (5 минут)

### 2.1 Установите зависимости
```bash
cd trendwatcher-hw
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2.2 Создайте .env файл
```bash
# Создайте файл .env со следующим содержимым:

# Firebase
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id

# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Settings
IMPORTANCE_THRESHOLD=3
```

### 2.3 Получите Firebase Web конфигурацию
1. Firebase Console → Project Settings → General → Your apps
2. Нажмите Web icon (</>) → Add app
3. Скопируйте `firebaseConfig`
4. Откройте `public/index.html`
5. Замените:
```javascript
const firebaseConfig = {
    apiKey: "AIza...",          // Ваш API key
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456:web:abc123"
};
```

---

## Шаг 3: Запустите трендвотчер (2 минуты)

### 3.1 Тест подключений
```bash
# Проверка Firebase
python firebase_manager.py

# Проверка DeepSeek API
python ai_marker.py
```

### 3.2 Первый запуск
```bash
python main.py
```

Что произойдёт:
1. ⏳ Сбор событий из 5 конкурентов (~30-60 сек)
2. 💾 Сохранение в Firebase
3. 🤖 ИИ-разметка через DeepSeek (~1-2 мин)
4. 📋 Формирование сводки
5. 📤 Отправка в Telegram
6. ✅ Готово!

### 3.3 Второй запуск (проверка дубликатов)
```bash
python main.py
```

Должно вывести:
```
⚠️  Все события уже существуют в базе (дубликаты)
Пропущено дубликатов: XX
```

---

## Шаг 4: Проверка безопасности (2 минуты)

```bash
python check_access.py
```

Проверяет:
- ✅ Чтение событий работает
- ✅ Обязательные поля присутствуют
- ✅ Запись заблокирована для публики
- ✅ Публичная страница готова

---

## Шаг 5: Деплой публичной страницы (5 минут)

### 5.1 Создайте GitHub репозиторий
```bash
git init
git add .
git commit -m "Initial commit: Trendwatcher homework"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/trendwatcher-hw.git
git push -u origin main
```

### 5.2 Включите GitHub Pages
1. Откройте Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, Folder: `/public`
4. Нажмите Save
5. Подождите 1-2 минуты

### 5.3 Проверьте публичную страницу
Откройте: `https://YOUR-USERNAME.github.io/trendwatcher-hw/`

---

## Шаг 6: Заполните отчёт (5 минут)

Откройте `README.md` и заполните плейсхолдеры:

1. **Раздел 1 (Сбор данных):**
   - Замените `XX` на реальные цифры из первого/второго запуска

2. **Раздел 3 (Telegram):**
   - Вставьте реальный текст сводки из Telegram

3. **Раздел 4 (Исключённые события):**
   - Скопируйте примеры исключённых событий (importance < 3)

4. **Раздел 5 (Публичная витрина):**
   - Вставьте URL: `https://YOUR-USERNAME.github.io/trendwatcher-hw/`
   - Добавьте скриншот (опционально)

5. **Раздел 6 (Проверка доступа):**
   - Скопируйте вывод `python check_access.py`

---

## ✅ Готово!

Теперь у вас есть:
- 🤖 Рабочий трендвотчер с ИИ-разметкой
- 📊 База событий в Firebase
- 📱 Telegram сводки
- 🌐 Публичная витрина на GitHub Pages
- 📄 Полный отчёт в README.md

---

## 🔧 Устранение неполадок

### Ошибка: "Firebase credentials not found"
- Убедитесь что файл `firebase-credentials.json` в корне проекта
- Проверьте путь в `.env`: `FIREBASE_CREDENTIALS_PATH=firebase-credentials.json`

### Ошибка: "DeepSeek API rate limit"
- Пополните баланс на https://platform.deepseek.com/
- Проверьте API ключ в `.env`

### Ошибка: "Telegram bot unauthorized"
- Проверьте токен бота в `.env`
- Убедитесь что отправили боту хотя бы одно сообщение

### Публичная страница не загружает данные
- Проверьте `firebaseConfig` в `public/index.html`
- Откройте Developer Console (F12) и проверьте ошибки
- Убедитесь что Firestore Rules разрешают чтение

### События не собираются
- Проверьте интернет соединение
- Некоторые сайты могут блокировать скрапинг
- Попробуйте запустить `python scraper.py` отдельно для отладки

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи в консоли
2. Запустите `python check_access.py`
3. Проверьте `.env` файл
4. Убедитесь что все ключи валидны

**Документация:**
- Firebase: https://firebase.google.com/docs/firestore
- DeepSeek API: https://platform.deepseek.com/docs
- Telegram Bot API: https://core.telegram.org/bots/api

---

**Время на полную настройку:** ~30-40 минут  
**Стоимость в месяц:** ~$0.15-0.30 (только DeepSeek API)  
**Сложность:** Средняя 🟡
