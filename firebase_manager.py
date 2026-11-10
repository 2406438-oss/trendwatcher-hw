"""
Модуль для работы с Firebase Firestore
Сохранение и получение событий
"""

import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Optional
from datetime import datetime
import os

from config import FIREBASE_CREDENTIALS_PATH, FIREBASE_PROJECT_ID


class FirebaseManager:
    """Менеджер для работы с Firebase Firestore"""
    
    def __init__(self):
        # Инициализация Firebase
        if not firebase_admin._apps:
            if os.path.exists(FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
            else:
                # Инициализация без credentials файла (используя переменные окружения)
                firebase_admin.initialize_app(options={
                    'projectId': FIREBASE_PROJECT_ID,
                })
        
        self.db = firestore.client()
        self.collection_name = 'events'
    
    def save_events(self, events: List[Dict]) -> int:
        """
        Сохраняет события в Firestore
        Использует event ID для предотвращения дубликатов
        
        Returns:
            Количество сохранённых событий (новых)
        """
        if not events:
            print("⚠️  Нет событий для сохранения")
            return 0
        
        try:
            collection_ref = self.db.collection(self.collection_name)
            saved_count = 0
            duplicate_count = 0
            
            for event in events:
                event_id = event['id']
                doc_ref = collection_ref.document(event_id)
                
                # Проверяем существование документа
                if doc_ref.get().exists:
                    duplicate_count += 1
                    continue
                
                # Добавляем timestamp для Firestore и инициализируем importance
                event_data = {**event}
                if 'collected_at' in event_data and isinstance(event_data['collected_at'], str):
                    event_data['collected_at'] = firestore.SERVER_TIMESTAMP
                
                # Инициализируем поля разметки, если их нет
                if 'importance' not in event_data:
                    event_data['importance'] = 0
                if 'gist' not in event_data:
                    event_data['gist'] = ''
                if 'why' not in event_data:
                    event_data['why'] = ''
                
                doc_ref.set(event_data)
                saved_count += 1
            
            print(f"✅ Сохранено новых событий в Firebase: {saved_count}")
            if duplicate_count > 0:
                print(f"⏭️  Пропущено дубликатов: {duplicate_count}")
            
            return saved_count
            
        except Exception as e:
            print(f"❌ Ошибка сохранения в Firebase: {e}")
            return 0
    
    def get_events(self, 
                   competitor: Optional[str] = None,
                   limit: int = 100,
                   only_unmarked: bool = False) -> List[Dict]:
        """
        Получает события из Firestore
        
        Args:
            competitor: Фильтр по конкуренту
            limit: Максимальное количество
            only_unmarked: Только неразмеченные события
        """
        try:
            query = self.db.collection(self.collection_name)
            
            if competitor:
                query = query.where('competitor', '==', competitor)
            
            if only_unmarked:
                # В Firestore фильтруем по отсутствию поля importance
                query = query.where('importance', '==', 0)
            
            query = query.order_by('collected_at', direction=firestore.Query.DESCENDING).limit(limit)
            
            docs = query.stream()
            events = []
            
            for doc in docs:
                event_data = doc.to_dict()
                event_data['id'] = doc.id
                events.append(event_data)
            
            return events
            
        except Exception as e:
            print(f"❌ Ошибка получения из Firebase: {e}")
            return []
    
    def update_event_markup(self, event_id: str, 
                           importance: int, 
                           gist: str, 
                           why: str) -> bool:
        """Обновляет разметку события"""
        try:
            doc_ref = self.db.collection(self.collection_name).document(event_id)
            doc_ref.update({
                'importance': importance,
                'gist': gist,
                'why': why,
                'marked_at': firestore.SERVER_TIMESTAMP
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления разметки: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Получает статистику по событиям"""
        try:
            collection_ref = self.db.collection(self.collection_name)
            
            # Всего событий
            all_docs = list(collection_ref.stream())
            total = len(all_docs)
            
            # Размеченные события (importance > 0)
            marked = sum(1 for doc in all_docs if doc.to_dict().get('importance', 0) > 0)
            
            return {
                'total': total,
                'marked': marked,
                'unmarked': total - marked
            }
            
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            return {'total': 0, 'marked': 0, 'unmarked': 0}


if __name__ == '__main__':
    # Тест подключения
    manager = FirebaseManager()
    stats = manager.get_stats()
    print("📊 Статистика Firebase:")
    print(f"  Всего событий: {stats['total']}")
    print(f"  Размеченных: {stats['marked']}")
    print(f"  Неразмеченных: {stats['unmarked']}")
