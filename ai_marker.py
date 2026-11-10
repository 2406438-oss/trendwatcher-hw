"""
ИИ-разметка событий через DeepSeek API
Определяет важность, краткую суть и обоснование
"""

from openai import OpenAI
from typing import Dict, List
import json

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL


class AIMarker:
    """ИИ-разметчик событий на базе DeepSeek"""
    
    def __init__(self):
        # DeepSeek использует OpenAI-совместимый API
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.model = "deepseek-chat"
        
        self.system_prompt = """
Ты - аналитик трендвотчера для компании в сфере IT-образования.

Твоя задача - оценить важность события от конкурента и дать краткую выжимку.

**Критерии важности (1-5):**

5 - Критическое:
- Запуск нового продукта/направления
- Крупная сделка, партнёрство, инвестиции
- Громкие новости в СМИ
- Радикальные изменения в бизнес-модели

4 - Высокая важность:
- Существенное обновление продукта
- Новые маркетинговые кампании
- Значимые вакансии (топ-менеджмент)
- Изменения в ценообразовании

3 - Средняя важность:
- Обычные статьи в блоге о продукте
- Стандартные вакансии
- Анонсы вебинаров
- Обновления курсов

2 - Низкая важность:
- Общие статьи без привязки к продукту
- Новости отрасли (не о компании)
- Технические посты

1 - Минимальная:
- Офтоп, развлекательный контент
- Старые новости (переопубликация)
- Технический контент без бизнес-значения

**Формат ответа (строго JSON):**
{
  "importance": 3,
  "gist": "Краткая суть события в 1-2 предложениях",
  "why": "Обоснование оценки важности"
}
"""
    
    def mark_event(self, event: Dict) -> Dict:
        """
        Размечает одно событие
        
        Returns:
            {'importance': int, 'gist': str, 'why': str, 'cost': float}
        """
        user_message = f"""
Конкурент: {event['competitor']}
Заголовок: {event['title']}
URL: {event['url']}
Описание: {event.get('description', 'Нет описания')}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Добавляем стоимость запроса
            usage = response.usage
            # Цены DeepSeek (на ноябрь 2024):
            # Input: $0.14 per 1M tokens, Output: $0.28 per 1M tokens
            input_cost = usage.prompt_tokens * 0.14 / 1_000_000
            output_cost = usage.completion_tokens * 0.28 / 1_000_000
            total_cost = input_cost + output_cost
            
            result['cost'] = round(total_cost, 6)
            result['tokens'] = usage.total_tokens
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка разметки события: {e}")
            return {
                'importance': 3,
                'gist': 'Ошибка разметки',
                'why': str(e),
                'cost': 0
            }
    
    def mark_events_batch(self, events: List[Dict]) -> List[Dict]:
        """
        Размечает пакет событий
        
        Returns:
            List of marked events with added fields: importance, gist, why
        """
        marked_events = []
        total_cost = 0
        
        print(f"\n🤖 Начинаю разметку {len(events)} событий через DeepSeek API...")
        
        for i, event in enumerate(events, 1):
            print(f"  [{i}/{len(events)}] {event['competitor']}: {event['title'][:60]}...")
            
            markup = self.mark_event(event)
            
            event_with_markup = {
                **event,
                'importance': markup['importance'],
                'gist': markup['gist'],
                'why': markup['why']
            }
            
            marked_events.append(event_with_markup)
            total_cost += markup['cost']
            
            print(f"    ⭐ Важность: {markup['importance']}/5")
            print(f"    📝 Суть: {markup['gist'][:80]}...")
            print(f"    💰 Стоимость: ${markup['cost']:.6f}")
        
        print(f"\n💰 Общая стоимость разметки: ${total_cost:.4f}")
        print(f"📊 Средняя стоимость на событие: ${total_cost/len(events):.6f}")
        
        # Оценка стоимости на месяц (при ежедневном запуске)
        monthly_cost = total_cost * 30
        print(f"📅 Оценка стоимости на месяц: ${monthly_cost:.2f}")
        
        return marked_events


if __name__ == '__main__':
    # Тест разметки
    marker = AIMarker()
    
    test_event = {
        'competitor': 'Яндекс Практикум',
        'title': 'Запускаем новое направление: Machine Learning Engineer',
        'url': 'https://example.com',
        'description': 'Мы рады анонсировать запуск нового курса для ML-инженеров с трудоустройством'
    }
    
    result = marker.mark_event(test_event)
    print(f"\n✅ Результат разметки:")
    print(f"  Важность: {result['importance']}/5")
    print(f"  Суть: {result['gist']}")
    print(f"  Почему: {result['why']}")
    print(f"  Стоимость: ${result['cost']:.6f}")
