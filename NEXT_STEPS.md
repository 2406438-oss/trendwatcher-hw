# 🎯 ЧТО ДАЛЬШЕ? Инструкция для вас

## ✅ Что уже готово

Я полностью адаптировал проект под новый стек:
- ✅ **Firebase Firestore** вместо Supabase
- ✅ **DeepSeek API** вместо OpenAI
- ✅ **Telegram Bot** для уведомлений
- ✅ **GitHub Pages** для публичной витрины

Все файлы созданы и настроены. Осталось только получить учётные данные и запустить!

---

## 📁 Структура проекта

```
trendwatcher-hw/
├── 📄 main.py                    # Главный скрипт (запускать этот)
├── 📄 scraper.py                 # Сбор событий
├── 📄 firebase_manager.py        # Работа с Firebase
├── 📄 ai_marker.py               # ИИ-разметка через DeepSeek
├── 📄 digest_builder.py          # Telegram сводки
├── 📄 config.py                  # Конфигурация
├── 📄 check_access.py            # Проверка безопасности
├── 📄 requirements.txt           # Зависимости Python
│
├── 📘 README.md                  # Полный отчёт (будет заполняться)
├── 📘 QUICKSTART.md              # Быстрый старт (30 минут)
├── 📘 SETUP_FIREBASE.md          # Подробная настройка Firebase
├── 📘 CHECKLIST.md               # Чек-лист выполнения задания
├── 📘 NEXT_STEPS.md              # Этот файл
│
├── 📋 .env.example               # Шаблон конфигурации
├── 📋 .gitignore                 # Исключения для Git
│
└── public/
    └── 📄 index.html             # Публичная витрина
```

---

## 🚀 Ваши следующие шаги

### 1️⃣ Получите учётные данные (15-20 минут)

#### Firebase (5 мин)
1. Перейдите: https://console.firebase.google.com/
2. Создайте проект `trendwatcher-hw`
3. Включите **Firestore Database**
4. Скачайте **Service Account** JSON
5. Сохраните как `firebase-credentials.json` в папку `trendwatcher-hw/`

**Подробно:** см. `SETUP_FIREBASE.md`

#### DeepSeek API (5 мин)
1. Перейдите: https://platform.deepseek.com/
2. Зарегистрируйтесь
3. Пополните баланс: **$5** (хватит на несколько месяцев!)
4. Создайте API ключ
5. Скопируйте ключ

#### Telegram Bot (5 мин)
1. Откройте [@BotFather](https://t.me/botfather)
2. Отправьте `/newbot`
3. Получите токен
4. Отправьте боту любое сообщение
5. Получите chat ID: `https://api.telegram.org/bot<TOKEN>/getUpdates`

---

### 2️⃣ Создайте .env файл (2 минуты)

В папке `trendwatcher-hw/` создайте файл `.env`:

```env
# Firebase
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id-here

# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Settings
IMPORTANCE_THRESHOLD=3
```

---

### 3️⃣ Установите зависимости (2 минуты)

```bash
cd trendwatcher-hw
python -m venv .venv

# Активируйте виртуальное окружение:
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Установите пакеты:
pip install -r requirements.txt
```

---

### 4️⃣ Тестовый запуск (5 минут)

```bash
# Тест Firebase
python firebase_manager.py

# Тест DeepSeek
python ai_marker.py

# Если оба теста прошли успешно - переходите к следующему шагу!
```

---

### 5️⃣ ПЕРВЫЙ ЗАПУСК! (3-5 минут)

```bash
python main.py
```

**Что произойдёт:**
1. ⏳ Сбор событий из 5 конкурентов (~30-60 сек)
2. 💾 Сохранение в Firebase
3. 🤖 ИИ-разметка через DeepSeek (~1-2 мин)
4. 📋 Формирование сводки
5. 📤 Отправка в Telegram
6. ✅ Готово!

**ВАЖНО:** Запишите цифры из вывода:
- Собрано событий: _____
- Сохранено в Firebase: _____
- Стоимость разметки: $_____

---

### 6️⃣ Второй запуск (проверка дубликатов) (1 минута)

```bash
python main.py
```

**Должно вывести:**
```
⚠️  Все события уже существуют в базе (дубликаты)
Пропущено дубликатов: XX
```

Это подтверждает что механизм предотвращения дубликатов работает!

---

### 7️⃣ Настройте публичную страницу (5 минут)

1. Firebase Console → Project Settings → Your apps
2. Нажмите Web icon `</>`
3. Скопируйте `firebaseConfig`
4. Откройте `public/index.html`
5. Найдите строки 287-293:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_FIREBASE_API_KEY",          // Замените!
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

6. Замените на свои данные

---

### 8️⃣ Проверьте безопасность (1 минута)

```bash
python check_access.py
```

Все проверки должны пройти ✅

---

### 9️⃣ Задеплойте на GitHub Pages (5 минут)

```bash
# 1. Создайте репозиторий на GitHub
git init
git add .
git commit -m "Trendwatcher homework complete"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/trendwatcher-hw.git
git push -u origin main

# 2. На GitHub: Settings → Pages
#    Source: main
#    Folder: /public
#    Save

# 3. Подождите 1-2 минуты
# 4. Откройте: https://YOUR-USERNAME.github.io/trendwatcher-hw/
```

---

### 🔟 Заполните отчёт (10 минут)

Откройте `README.md` и заполните:

1. **Раздел 1:** Вставьте статистику из первого/второго запуска
2. **Раздел 3:** Скопируйте текст сводки из Telegram
3. **Раздел 4:** Скопируйте примеры исключённых событий
4. **Раздел 5:** Вставьте URL публичной страницы
5. **Раздел 6:** Скопируйте вывод `check_access.py`

---

## 📚 Полезные документы

- **QUICKSTART.md** - самый быстрый способ запустить (30 мин)
- **SETUP_FIREBASE.md** - подробная настройка Firebase с скриншотами
- **CHECKLIST.md** - пошаговый чек-лист выполнения задания
- **README.md** - финальный отчёт (заполняется в процессе)

---

## 🆘 Если что-то не работает

### Firebase ошибка
```
❌ Firebase credentials not found
```
**Решение:** Убедитесь что `firebase-credentials.json` в папке `trendwatcher-hw/`

### DeepSeek ошибка
```
❌ Rate limit exceeded
```
**Решение:** Пополните баланс на https://platform.deepseek.com/

### Telegram ошибка
```
❌ Unauthorized
```
**Решение:** Отправьте боту хотя бы одно сообщение перед запуском

### Публичная страница не загружает данные
**Решение:**
1. Проверьте `firebaseConfig` в `public/index.html`
2. Откройте DevTools (F12) → Console
3. Проверьте ошибки

---

## ✅ Критерии выполнения

Задание считается выполненным, когда:
- ✅ События собираются без дубликатов
- ✅ ИИ-разметка работает (importance, gist, why)
- ✅ Сводка приходит в Telegram
- ✅ Публичная страница работает
- ✅ check_access.py проходит все проверки
- ✅ README.md заполнен реальными данными

---

## 💰 Стоимость

- **Firebase Firestore:** Бесплатно (free tier хватит надолго)
- **DeepSeek API:** ~$0.15-0.30 в месяц
- **Telegram Bot:** Бесплатно
- **GitHub Pages:** Бесплатно

**Итого:** ~$0.15-0.30 в месяц

---

## ⏱️ Время выполнения

- Получение учётных данных: **15-20 мин**
- Настройка проекта: **5 мин**
- Первый запуск: **5 мин**
- Настройка публичной страницы: **5 мин**
- Деплой на GitHub Pages: **5 мин**
- Заполнение отчёта: **10 мин**

**ИТОГО: ~40-50 минут**

---

## 🎯 Следующие шаги

1. **Прямо сейчас:** Получите учётные данные (Firebase + DeepSeek + Telegram)
2. **Через 15 минут:** Создайте `.env` и запустите `python main.py`
3. **Через 20 минут:** Задеплойте на GitHub Pages
4. **Через 30 минут:** Заполните отчёт в README.md
5. **Через 40 минут:** ✅ Задание выполнено!

---

## 📞 Нужна помощь?

Смотрите:
- `QUICKSTART.md` - если торопитесь
- `SETUP_FIREBASE.md` - если нужны подробности
- `CHECKLIST.md` - если хотите пошаговый план

---

**Удачи! 🚀**

Если возникнут вопросы - все инструкции в файлах выше.
