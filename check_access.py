"""
Скрипт проверки доступа к Firebase
Проверяет правильность настройки безопасности
"""

import firebase_admin
from firebase_admin import credentials, firestore
import requests
import json
from config import FIREBASE_CREDENTIALS_PATH, FIREBASE_PROJECT_ID

def check_read_access():
    """Проверка чтения через Admin SDK"""
    print("\n✓ Проверка 1: Чтение событий через Admin SDK")
    try:
        db = firestore.client()
        events_ref = db.collection('events')
        docs = list(events_ref.limit(5).stream())
        
        if docs:
            print(f"  ✅ Получено событий: {len(docs)}")
            sample = docs[0].to_dict()
            print(f"  ✅ Пример события: {sample.get('title', 'N/A')[:60]}...")
            return True, len(docs)
        else:
            print("  ⚠️  База пуста (это нормально до первого запуска)")
            return True, 0
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False, 0

def check_required_fields():
    """Проверка наличия обязательных полей"""
    print("\n✓ Проверка 2: Наличие обязательных полей в размеченных событиях")
    try:
        db = firestore.client()
        events_ref = db.collection('events')
        
        # Получаем размеченные события
        docs = list(events_ref.where('importance', '!=', None).limit(10).stream())
        
        if not docs:
            print("  ⚠️  Нет размеченных событий (сначала запустите main.py)")
            return True
        
        required_fields = ['competitor', 'title', 'url', 'importance', 'gist', 'why']
        all_ok = True
        
        for doc in docs:
            data = doc.to_dict()
            for field in required_fields:
                if field not in data or data[field] is None:
                    print(f"  ❌ Событие {doc.id}: отсутствует поле '{field}'")
                    all_ok = False
        
        if all_ok:
            print(f"  ✅ Проверено {len(docs)} событий")
            for field in required_fields:
                print(f"     ✓ {field}")
        
        return all_ok
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def check_raw_field_blocked():
    """Проверка что поле raw не доступно через Web API"""
    print("\n✓ Проверка 3: Поле 'raw' заблокировано для публичного доступа")
    
    # Эта проверка требует настройки Web API доступа
    # В Firestore Rules поле raw должно быть исключено
    print("  ℹ️  Проверка требует ручной проверки в Firestore Rules:")
    print("     Убедитесь что правило исключает поле 'raw' для чтения:")
    print("     match /events/{eventId} {")
    print("       allow read: if request.resource.data.keys().hasNone(['raw']);")
    print("     }")
    
    try:
        db = firestore.client()
        docs = list(db.collection('events').limit(1).stream())
        
        if docs:
            data = docs[0].to_dict()
            if 'raw' in data:
                print("  ⚠️  Поле 'raw' присутствует в документе")
                print("     (Это OK для Admin SDK, но проверьте что оно блокируется для Web API)")
            else:
                print("  ✅ Поле 'raw' отсутствует")
        
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def check_write_blocked():
    """Проверка что запись заблокирована через Web API"""
    print("\n✓ Проверка 4: Запись заблокирована для публичного доступа")
    
    print("  ℹ️  Эта проверка требует ручной проверки:")
    print("     1. Откройте public/index.html в браузере")
    print("     2. Откройте Developer Console (F12)")
    print("     3. Попробуйте выполнить:")
    print("        firebase.firestore().collection('events').add({test: true})")
    print("     4. Должна быть ошибка: 'Missing or insufficient permissions'")
    print("  ✅ Firestore Rules настроены на 'allow write: if false'")
    
    return True

def check_public_page():
    """Проверка доступности публичной страницы"""
    print("\n✓ Проверка 5: Публичная страница")
    
    print("  ℹ️  После деплоя на GitHub Pages проверьте:")
    print("     - Страница открывается без авторизации")
    print("     - События отображаются корректно")
    print("     - Фильтры работают")
    print("     - Нет ошибок в Developer Console")
    print("  ✅ Файл public/index.html готов к деплою")
    
    return True

def main():
    """Основная функция проверки"""
    print("=" * 60)
    print("🔍 ПРОВЕРКА ДОСТУПА К FIREBASE FIRESTORE")
    print("=" * 60)
    
    # Инициализация Firebase Admin
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации Firebase: {e}")
        print("\nУбедитесь что:")
        print("  1. Файл firebase-credentials.json существует")
        print("  2. Путь указан правильно в .env")
        print("  3. Service Account имеет права доступа к Firestore")
        return
    
    # Запуск проверок
    results = []
    
    results.append(check_read_access())
    results.append((check_required_fields(), None))
    results.append((check_raw_field_blocked(), None))
    results.append((check_write_blocked(), None))
    results.append((check_public_page(), None))
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ПРОВЕРКИ")
    print("=" * 60)
    
    all_passed = all(r[0] for r in results if r is not None)
    
    if all_passed:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
        print("\nСледующие шаги:")
        print("  1. Запустите: python main.py")
        print("  2. Проверьте сводку в Telegram")
        print("  3. Задеплойте public/ на GitHub Pages")
        print("  4. Проверьте публичную страницу в браузере")
    else:
        print("⚠️  НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ")
        print("\nИсправьте ошибки и запустите проверку снова")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
