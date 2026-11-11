#!/usr/bin/env python3
"""Генерация Telegram-сводки для отчёта"""
from firebase_manager import FirebaseManager
from digest_builder import DigestBuilder
from datetime import datetime

def main():
    fm = FirebaseManager()
    db = DigestBuilder()
    
    # Получаем события
    events = fm.get_events(limit=100)
    
    # Генерируем основную сводку
    date_str = datetime.now().strftime("%d.%m.%Y")
    digest = db.build_digest(events, start_date=date_str, end_date=date_str)
    
    print("=" * 80)
    print("📱 ПОЛНЫЙ ТЕКСТ TELEGRAM-СВОДКИ (для README секция 3)")
    print("=" * 80)
    print()
    print(digest)
    print()
    
    # Генерируем отчёт об исключённых
    excluded_report = db.build_excluded_report(events)
    print()
    print("=" * 80)
    print("📱 ОТЧЁТ ОБ ИСКЛЮЧЁННЫХ СОБЫТИЯХ")
    print("=" * 80)
    print()
    print(excluded_report)
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
