"""
Формирование и отправка сводок в Telegram
"""

from telegram import Bot
from telegram.constants import ParseMode
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, IMPORTANCE_THRESHOLD


class DigestBuilder:
    """Построитель сводок для Telegram"""
    
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.threshold = IMPORTANCE_THRESHOLD
    
    def format_event(self, event: Dict) -> str:
        """Форматирует одно событие для Telegram"""
        importance_stars = "⭐" * event['importance']
        
        text = f"{importance_stars} **{event['title']}**\n"
        text += f"📝 _{event['gist']}_\n"
        text += f"🔗 [Перейти к источнику]({event['url']})\n"
        
        if event.get('why'):
            text += f"💡 {event['why']}\n"
        
        return text
    
    def build_digest(self, events: List[Dict], 
                    start_date: str = None,
                    end_date: str = None) -> str:
        """
        Формирует сводку из событий
        
        Args:
            events: Список размеченных событий
            start_date: Начало периода (ISO format)
            end_date: Конец периода (ISO format)
        """
        # Фильтруем по важности
        important_events = [e for e in events if e.get('importance', 0) >= self.threshold]
        excluded_events = [e for e in events if e.get('importance', 0) < self.threshold]
        
        # Группируем по конкурентам
        by_competitor = defaultdict(list)
        for event in important_events:
            by_competitor[event['competitor']].append(event)
        
        # Сортируем внутри каждого конкурента по важности
        for competitor in by_competitor:
            by_competitor[competitor].sort(key=lambda x: x.get('importance', 0), reverse=True)
        
        # Формируем текст сводки
        period = ""
        if start_date and end_date:
            period = f" за период {start_date} - {end_date}"
        
        digest = f"📊 **СВОДКА ТРЕНДВОТЧЕРА**{period}\n"
        digest += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if not important_events:
            digest += "ℹ️ Нет важных событий за период\n"
            return digest
        
        # Добавляем события по конкурентам
        for competitor, comp_events in sorted(by_competitor.items()):
            digest += f"🏢 **{competitor}** ({len(comp_events)} событий)\n"
            digest += "─" * 40 + "\n\n"
            
            for event in comp_events:
                digest += self.format_event(event)
                digest += "\n"
            
            digest += "\n"
        
        # Статистика
        digest += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        digest += f"📈 **ИТОГО:**\n"
        digest += f"• Всего событий: {len(events)}\n"
        digest += f"• Важных (≥{self.threshold}): {len(important_events)}\n"
        digest += f"• Исключено (<{self.threshold}): {len(excluded_events)}\n"
        digest += f"• Конкурентов: {len(by_competitor)}\n"
        
        return digest
    
    def build_excluded_report(self, events: List[Dict]) -> str:
        """Формирует отчёт об исключённых событиях"""
        excluded = [e for e in events if e.get('importance', 0) < self.threshold]
        
        if not excluded:
            return "✅ Нет исключённых событий"
        
        report = f"📋 **ИСКЛЮЧЁННЫЕ СОБЫТИЯ** (важность <{self.threshold})\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        by_competitor = defaultdict(list)
        for event in excluded:
            by_competitor[event['competitor']].append(event)
        
        for competitor, comp_events in sorted(by_competitor.items()):
            report += f"🏢 **{competitor}** ({len(comp_events)})\n"
            
            for event in comp_events:
                imp = event.get('importance', 0)
                report += f"  • [{imp}/5] {event['title'][:60]}...\n"
                report += f"    _{event.get('gist', '')[:80]}..._\n"
            
            report += "\n"
        
        return report
    
    async def send_digest(self, digest_text: str):
        """Отправляет сводку в Telegram"""
        try:
            # Telegram ограничивает сообщения до 4096 символов
            max_length = 4000
            
            if len(digest_text) <= max_length:
                await self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=digest_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                print("✅ Сводка отправлена в Telegram")
            else:
                # Разбиваем на части
                parts = []
                current_part = ""
                
                for line in digest_text.split('\n'):
                    if len(current_part) + len(line) + 1 <= max_length:
                        current_part += line + '\n'
                    else:
                        parts.append(current_part)
                        current_part = line + '\n'
                
                if current_part:
                    parts.append(current_part)
                
                for i, part in enumerate(parts, 1):
                    await self.bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=f"[Часть {i}/{len(parts)}]\n\n{part}",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                
                print(f"✅ Сводка отправлена в Telegram ({len(parts)} частей)")
                
        except Exception as e:
            print(f"❌ Ошибка отправки в Telegram: {e}")


if __name__ == '__main__':
    # Тест форматирования
    builder = DigestBuilder()
    
    test_events = [
        {
            'competitor': 'Яндекс Практикум',
            'title': 'Новый курс по ML',
            'url': 'https://example.com/1',
            'gist': 'Запущен курс Machine Learning Engineer с гарантией трудоустройства',
            'why': 'Новое направление, высокая конкуренция за студентов',
            'importance': 5
        },
        {
            'competitor': 'Hexlet',
            'title': 'Статья о чистом коде',
            'url': 'https://example.com/2',
            'gist': 'Общая статья о принципах чистого кода',
            'why': 'Образовательный контент без привязки к продукту',
            'importance': 2
        },
    ]
    
    digest = builder.build_digest(test_events, '2026-11-01', '2026-11-10')
    print(digest)
    
    print("\n" + "="*80 + "\n")
    
    excluded = builder.build_excluded_report(test_events)
    print(excluded)
