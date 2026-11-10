# Настройка Firebase для Трендвотчера

## 1. Создание Firebase проекта

1. Перейдите на https://console.firebase.google.com/
2. Нажмите "Добавить проект" (Add project)
3. Введите название проекта (например, `trendwatcher-hw`)
4. Отключите Google Analytics (не требуется для этого проекта)
5. Нажмите "Создать проект"

## 2. Настройка Firestore Database

1. В боковом меню выберите **Firestore Database**
2. Нажмите "Создать базу данных" (Create database)
3. Выберите режим **Production mode**
4. Выберите регион (например, `europe-west3` для Европы)
5. Нажмите "Включить" (Enable)

### Настройка правил безопасности

В разделе **Rules** замените правила на следующие:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Публичный доступ на чтение событий
    match /events/{eventId} {
      allow read: if true;  // Открытый доступ на чтение
      allow write: if false;  // Запись только через Admin SDK
    }
  }
}
```

## 3. Получение учётных данных для сервера

### Service Account (для Python скрипта)

1. Перейдите в **Project Settings** (⚙️ → Project settings)
2. Откройте вкладку **Service accounts**
3. Нажмите "Generate new private key"
4. Сохраните JSON файл как `firebase-credentials.json` в корень проекта
5. **ВАЖНО:** Добавьте этот файл в `.gitignore`!

```bash
# В файле .gitignore
firebase-credentials.json
```

## 4. Получение конфигурации для публичной страницы

1. В **Project Settings** → **General**
2. Прокрутите до раздела "Your apps"
3. Нажмите на иконку Web (</>) "Add app"
4. Введите название приложения (например, `trendwatcher-public`)
5. **НЕ** включайте Firebase Hosting
6. Скопируйте объект `firebaseConfig`

Пример:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

## 5. Настройка .env файла

Создайте файл `.env` в корне проекта:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id

# DeepSeek API (получите на https://platform.deepseek.com/)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Settings
IMPORTANCE_THRESHOLD=3
```

## 6. Обновление public/index.html

Откройте `public/index.html` и замените:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_FIREBASE_API_KEY",          // Замените
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",  // Замените
    projectId: "YOUR_PROJECT_ID",             // Замените
    storageBucket: "YOUR_PROJECT_ID.appspot.com",   // Замените
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",  // Замените
    appId: "YOUR_APP_ID"                      // Замените
};
```

## 7. Создание Telegram бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Введите название бота (например, `Trendwatcher Bot`)
4. Введите username (должен заканчиваться на `bot`, например `trendwatcher_hw_bot`)
5. Скопируйте **токен бота** в `.env` → `TELEGRAM_BOT_TOKEN`

### Получение Chat ID

1. Отправьте боту любое сообщение
2. Откройте в браузере: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Найдите `"chat":{"id": 123456789}` и скопируйте ID
4. Добавьте в `.env` → `TELEGRAM_CHAT_ID`

## 8. Получение DeepSeek API ключа

1. Перейдите на https://platform.deepseek.com/
2. Зарегистрируйтесь или войдите
3. Пополните баланс (минимум $5)
4. Перейдите в раздел API Keys
5. Создайте новый ключ
6. Скопируйте в `.env` → `DEEPSEEK_API_KEY`

## 9. Установка зависимостей

```bash
cd trendwatcher-hw
pip install -r requirements.txt
```

## 10. Проверка подключения

Тест Firebase:
```bash
python firebase_manager.py
```

Тест DeepSeek API:
```bash
python ai_marker.py
```

## Готово! 🎉

Теперь можно запускать полный цикл:
```bash
python main.py
```
