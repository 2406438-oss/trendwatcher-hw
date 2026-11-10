"""
Главный скрипт трендвотчера
Запускает полный цикл: сбор -> разметка -> сводка -> отправка
"""

import asyncio
from datetime import datetime

from scraper import EventScraper
from firebase_manager import FirebaseManager
from ai_marker import AIMarker
from digest_builder import DigestBuilder


async def main():
    """Основной пайплайн трендвотчера"""
    
    print("=" * 80)
    print("🚀 ЗАПУСК ТРЕНДВОТЧЕРА")
    print("=" * 80)
    print(f"⏰ Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Инициализация компонентов
    scraper = EventScraper()
    db = FirebaseManager()
    marker = AIMarker()
    builder = DigestBuilder()
    
    # Этап 1: Сбор событий
    print("\n" + "=" * 80)
    print("📡 ЭТАП 1: СБОР СОБЫТИЙ")
    print("=" * 80)
    
    events = scraper.scrape_all()
    
    if not events:
        print("⚠️  Не найдено новых событий")
        return
    
    print(f"\n✅ Собрано событий: {len(events)}")
    
    # Этап 2: Сохранение в Firebase
    print("\n" + "=" * 80)
    print("💾 ЭТАП 2: СОХРАНЕНИЕ В FIREBASE")
    print("=" * 80)
    
    saved_count = db.save_events(events)
    
    if saved_count == 0:
        print("⚠️  Все события уже существуют в базе (дубликаты)")
    
    # Статистика до разметки
    stats_before = db.get_stats()
    print(f"\n📊 Статистика Firebase:")
    print(f"  Всего событий: {stats_before['total']}")
    print(f"  Размеченных: {stats_before['marked']}")
    print(f"  Неразмеченных: {stats_before['unmarked']}")
    
    # Этап 3: ИИ-разметка
    print("\n" + "=" * 80)
    print("🤖 ЭТАП 3: ИИ-РАЗМЕТКА СОБЫТИЙ")
    print("=" * 80)
    
    # Получаем неразмеченные события
    unmarked_events = db.get_events(only_unmarked=True, limit=50)
    
    if not unmarked_events:
        print("✅ Все события уже размечены")
    else:
        print(f"📝 Найдено неразмеченных событий: {len(unmarked_events)}")
        
        # Размечаем события
        marked_events = marker.mark_events_batch(unmarked_events)
        
        # Сохраняем разметку обратно в Firebase
        print(f"\n💾 Сохранение разметки в Firebase...")
        for event in marked_events:
            db.update_event_markup(
                event['id'],
                event['importance'],
                event['gist'],
                event['why']
            )
        
        print(f"✅ Разметка сохранена")
    
    # Статистика после разметки
    stats_after = db.get_stats()
    print(f"\n📊 Статистика после разметки:")
    print(f"  Всего событий: {stats_after['total']}")
    print(f"  Размеченных: {stats_after['marked']}")
    print(f"  Неразмеченных: {stats_after['unmarked']}")
    
    # Этап 4: Формирование сводки
    print("\n" + "=" * 80)
    print("📋 ЭТАП 4: ФОРМИРОВАНИЕ СВОДКИ")
    print("=" * 80)
    
    # Получаем все размеченные события за последние 7 дней
    all_events = db.get_events(limit=100)
    
    # Фильтруем размеченные
    marked_only = [e for e in all_events if e.get('importance') is not None]
    
    if not marked_only:
        print("⚠️  Нет размеченных событий для сводки")
        return
    
    print(f"📊 Размеченных событий для сводки: {len(marked_only)}")
    
    # Формируем сводку
    digest_text = builder.build_digest(
        marked_only,
        start_date=datetime.now().strftime('%Y-%m-%d'),
        end_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    print("\n" + "-" * 80)
    print("СВОДКА:")
    print("-" * 80)
    print(digest_text)
    
    # Отчёт об исключённых событиях
    excluded_report = builder.build_excluded_report(marked_only)
    print("\n" + "-" * 80)
    print("ИСКЛЮЧЁННЫЕ СОБЫТИЯ:")
    print("-" * 80)
    print(excluded_report)
    
    # Этап 5: Отправка в Telegram
    print("\n" + "=" * 80)
    print("📤 ЭТАП 5: ОТПРАВКА В TELEGRAM")
    print("=" * 80)
    
    # Отправляем сводку
    await builder.send_digest(digest_text)
    
    # Опционально: отправляем отчёт об исключённых
    # await builder.send_digest(excluded_report)
    
    # Финал
    print("\n" + "=" * 80)
    print("✅ ТРЕНДВОТЧЕР ЗАВЕРШИЛ РАБОТУ")
    print("=" * 80)
    print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    asyncio.run(main())
