"""
Скрипт для обновления существующих событий: добавление importance=0
"""
from firebase_manager import FirebaseManager

def fix_existing_events():
    """Добавляет importance=0 к существующим событиям без разметки"""
    db = FirebaseManager()
    
    try:
        # Получаем все события
        collection_ref = db.db.collection(db.collection_name)
        docs = collection_ref.stream()
        
        updated_count = 0
        
        for doc in docs:
            event_data = doc.to_dict()
            
            # Проверяем, нужно ли обновить
            needs_update = False
            update_data = {}
            
            if 'importance' not in event_data or event_data.get('importance') is None:
                update_data['importance'] = 0
                needs_update = True
            
            if 'gist' not in event_data or event_data.get('gist') is None:
                update_data['gist'] = ''
                needs_update = True
            
            if 'why' not in event_data or event_data.get('why') is None:
                update_data['why'] = ''
                needs_update = True
            
            if needs_update:
                doc.reference.update(update_data)
                updated_count += 1
                print(f"✅ Обновлено: {event_data.get('title', 'без названия')[:50]}")
        
        print(f"\n✅ Обновлено событий: {updated_count}")
        
        # Проверяем статистику
        stats = db.get_stats()
        print(f"\n📊 Статистика после обновления:")
        print(f"  Всего событий: {stats['total']}")
        print(f"  Размеченных: {stats['marked']}")
        print(f"  Неразмеченных: {stats['unmarked']}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_existing_events()
