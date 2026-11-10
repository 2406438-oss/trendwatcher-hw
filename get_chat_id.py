"""
Скрипт для получения Chat ID из Telegram бота
"""
import requests
import sys

TOKEN = "8572618880:AAHelep4QE9G4ZBNjTBwTkV3dqv3eFvUKhk"

def get_chat_id():
    """Получает Chat ID из последних сообщений бота"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    
    try:
        print("🔍 Запрашиваю обновления от бота...")
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ Ошибка API: {data.get('description', 'Неизвестная ошибка')}")
            return
        
        results = data.get("result", [])
        
        if not results:
            print("\n⚠️  Сообщений не найдено!")
            print("\n📝 Инструкция:")
            print("1. Найдите вашего бота в Telegram")
            print("2. Отправьте ему любое сообщение (например: /start)")
            print("3. Запустите этот скрипт снова")
            return
        
        print(f"\n✅ Найдено сообщений: {len(results)}")
        print("\n" + "="*60)
        
        chat_ids = set()
        for update in results:
            if "message" in update:
                msg = update["message"]
                chat = msg.get("chat", {})
                chat_id = chat.get("id")
                username = chat.get("username", "нет username")
                first_name = chat.get("first_name", "")
                last_name = chat.get("last_name", "")
                
                if chat_id:
                    chat_ids.add(chat_id)
                    print(f"\n💬 Сообщение от: {first_name} {last_name} (@{username})")
                    print(f"   Chat ID: {chat_id}")
                    print(f"   Текст: {msg.get('text', 'нет текста')}")
        
        print("\n" + "="*60)
        
        if chat_ids:
            if len(chat_ids) == 1:
                chat_id = list(chat_ids)[0]
                print(f"\n✅ ВАШ CHAT ID: {chat_id}")
                print(f"\nДобавьте в .env файл:")
                print(f"TELEGRAM_CHAT_ID={chat_id}")
            else:
                print(f"\n⚠️  Найдено несколько Chat ID: {chat_ids}")
                print("Используйте ID того чата, куда нужно отправлять сообщения")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    get_chat_id()
