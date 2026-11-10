#!/usr/bin/env python3
"""Скрипт для извлечения данных для README"""
import json
from firebase_manager import FirebaseManager
from collections import Counter

def main():
    fm = FirebaseManager()
    
    # Получаем все события
    events = fm.get_events(limit=100)
    
    print(f"=== СТАТИСТИКА СБОРА ===")
    print(f"Всего событий: {len(events)}")
    
    # Группируем по конкурентам
    competitors = Counter(e.get('competitor') for e in events)
    print("\nПо конкурентам:")
    for comp, count in competitors.most_common():
        print(f"  - {comp}: {count}")
    
    print(f"\n=== СТАТИСТИКА ВАЖНОСТИ ===")
    importance_dist = Counter(e.get('importance', 0) for e in events)
    print("Распределение важности:")
    for imp in sorted(importance_dist.keys(), reverse=True):
        count = importance_dist[imp]
        print(f"  - Важность {imp}: {count} событий")
    
    important = [e for e in events if e.get('importance', 0) >= 3]
    excluded = [e for e in events if e.get('importance', 0) < 3]
    
    print(f"\nВажных (≥3): {len(important)}")
    print(f"Исключённых (<3): {len(excluded)}")
    
    print(f"\n=== ВАЖНЫЕ СОБЫТИЯ (≥3) ===")
    for e in important:
        print(f"\n{e.get('competitor')} - {e.get('title')}")
        print(f"  Важность: {e.get('importance')}/5")
        print(f"  Суть: {e.get('gist')}")
        print(f"  Почему важно: {e.get('why')}")
        print(f"  URL: {e.get('url')}")
    
    print(f"\n=== ИСКЛЮЧЁННЫЕ СОБЫТИЯ (<3) - Примеры ===")
    for i, e in enumerate(excluded[:3], 1):
        print(f"\n{i}. {e.get('competitor')} - {e.get('title')}")
        print(f"   Важность: {e.get('importance')}/5")
        print(f"   Суть: {e.get('gist')}")
        print(f"   Почему исключён: {e.get('why')}")

if __name__ == '__main__':
    main()
