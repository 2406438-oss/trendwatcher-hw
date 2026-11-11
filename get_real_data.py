#!/usr/bin/env python3
"""Скрипт для извлечения реальных данных для финальной доработки отчёта"""
import json
from firebase_manager import FirebaseManager
from collections import Counter

def main():
    fm = FirebaseManager()
    
    # Получаем все события
    events = fm.get_events(limit=100)
    
    print("=" * 80)
    print("📋 РЕАЛЬНЫЕ ДАННЫЕ ДЛЯ ОТЧЁТА")
    print("=" * 80)
    
    # 1. РЕАЛЬНЫЙ ПРИМЕР РАЗМЕЧЕННОГО СОБЫТИЯ
    print("\n1️⃣ РЕАЛЬНЫЙ ПРИМЕР РАЗМЕЧЕННОГО СОБЫТИЯ (для секции 2)")
    print("-" * 80)
    
    # Находим событие с важностью >= 3
    important_event = next((e for e in events if e.get('importance', 0) >= 3), None)
    
    if important_event:
        collected_at = important_event.get('collected_at')
        if hasattr(collected_at, 'isoformat'):
            collected_at = collected_at.isoformat()
        elif collected_at:
            collected_at = str(collected_at)
        
        example = {
            "competitor": important_event.get('competitor'),
            "title": important_event.get('title'),
            "url": important_event.get('url'),
            "importance": important_event.get('importance'),
            "gist": important_event.get('gist'),
            "why": important_event.get('why'),
            "collected_at": collected_at
        }
        print("\nJSON для вставки в README:")
        print("```json")
        print(json.dumps(example, ensure_ascii=False, indent=2))
        print("```")
    
    # 2. СТАТИСТИКА ДЛЯ TELEGRAM СВОДКИ
    print("\n\n2️⃣ ДАННЫЕ ДЛЯ TELEGRAM СВОДКИ (для секции 3)")
    print("-" * 80)
    
    important = [e for e in events if e.get('importance', 0) >= 3]
    excluded = [e for e in events if e.get('importance', 0) < 3]
    
    print(f"\nВажных событий (≥3): {len(important)}")
    print(f"Исключённых событий (<3): {len(excluded)}")
    
    if important:
        print("\n📊 ВАЖНЫЕ СОБЫТИЯ:")
        for e in important:
            print(f"\n🏢 {e.get('competitor')}")
            print(f"📌 {e.get('title')}")
            print(f"⭐ Важность: {e.get('importance')}/5")
            print(f"💡 {e.get('gist')}")
            print(f"🔗 {e.get('url')}")
    
    print("\n\n🚫 ИСКЛЮЧЁННЫЕ СОБЫТИЯ (примеры):")
    for i, e in enumerate(excluded[:3], 1):
        print(f"\n{i}. {e.get('competitor')} - {e.get('title')[:60]}...")
        print(f"   ⭐ Важность: {e.get('importance')}/5")
        print(f"   💡 {e.get('gist')}")
        print(f"   🔗 {e.get('url')}")
    
    # 3. ПОЛНАЯ СТАТИСТИКА
    print("\n\n3️⃣ ПОЛНАЯ СТАТИСТИКА")
    print("-" * 80)
    
    competitors = Counter(e.get('competitor') for e in events)
    importance_dist = Counter(e.get('importance', 0) for e in events)
    
    print(f"\nВсего событий: {len(events)}")
    print("\nПо конкурентам:")
    for comp, count in competitors.most_common():
        print(f"  • {comp}: {count}")
    
    print("\nПо важности:")
    for imp in sorted(importance_dist.keys(), reverse=True):
        count = importance_dist[imp]
        print(f"  • Важность {imp}: {count} событий")
    
    # 4. ИНФОРМАЦИЯ О ИСТОЧНИКАХ
    print("\n\n4️⃣ ИНФОРМАЦИЯ ОБ ИСТОЧНИКАХ")
    print("-" * 80)
    print("\nКонкуренты с собранными событиями:")
    for comp in competitors.keys():
        print(f"  ✅ {comp}")
    
    missing = ["Яндекс Практикум", "Skillfactory", "Hexlet"] 
    present = list(competitors.keys())
    for comp in missing:
        if comp not in present:
            print(f"  ⚠️ {comp} - события не найдены (возможно, источник временно недоступен)")

if __name__ == '__main__':
    main()
