"""
Сборщик событий из источников конкурентов
Поддерживает RSS, Sitemap.xml и HTML-парсинг
"""

import requests
import feedparser
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib
import time

from config import COMPETITORS


class EventScraper:
    """Сборщик событий из различных источников"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.events = []
    
    def generate_event_id(self, url: str, title: str) -> str:
        """Генерирует уникальный ID события на основе URL и заголовка"""
        content = f"{url}_{title}".encode('utf-8')
        return hashlib.md5(content).hexdigest()
    
    def scrape_rss(self, url: str, competitor: str) -> List[Dict]:
        """Парсит RSS-ленту"""
        events = []
        try:
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:10]:  # Берём последние 10 записей
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    pub_date = datetime(*published[:6])
                else:
                    pub_date = datetime.now()
                
                # Берём события не старше 7 дней
                if (datetime.now() - pub_date).days <= 7:
                    event = {
                        'id': self.generate_event_id(entry.link, entry.title),
                        'competitor': competitor,
                        'title': entry.title,
                        'url': entry.link,
                        'description': entry.get('summary', '')[:500],
                        'published_at': pub_date.isoformat(),
                        'source_type': 'RSS',
                        'raw': entry.get('summary', ''),
                        'collected_at': datetime.now().isoformat()
                    }
                    events.append(event)
                    
        except Exception as e:
            print(f"❌ Ошибка парсинга RSS {url}: {e}")
        
        return events
    
    def scrape_sitemap(self, url: str, competitor: str) -> List[Dict]:
        """Парсит sitemap.xml и берёт свежие URL"""
        events = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            root = ET.fromstring(response.content)
            
            # Ищем URL в sitemap
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = root.findall('.//ns:url', namespace)
            
            for url_entry in urls[:20]:  # Берём первые 20 URL
                loc = url_entry.find('ns:loc', namespace)
                lastmod = url_entry.find('ns:lastmod', namespace)
                
                if loc is not None:
                    page_url = loc.text
                    
                    # Проверяем дату изменения
                    if lastmod is not None:
                        try:
                            mod_date = datetime.fromisoformat(lastmod.text.replace('Z', '+00:00'))
                            if (datetime.now() - mod_date.replace(tzinfo=None)).days > 7:
                                continue
                        except:
                            pass
                    
                    # Фильтруем только релевантные страницы (блог, новости, вакансии)
                    if any(keyword in page_url.lower() for keyword in ['blog', 'news', 'post', 'article', 'career', 'job']):
                        # Получаем заголовок страницы
                        try:
                            page_response = requests.get(page_url, headers=self.headers, timeout=5)
                            soup = BeautifulSoup(page_response.content, 'html.parser')
                            title = soup.find('title')
                            title_text = title.text.strip() if title else page_url
                            
                            event = {
                                'id': self.generate_event_id(page_url, title_text),
                                'competitor': competitor,
                                'title': title_text,
                                'url': page_url,
                                'description': '',
                                'published_at': lastmod.text if lastmod is not None else datetime.now().isoformat(),
                                'source_type': 'Sitemap',
                                'raw': '',
                                'collected_at': datetime.now().isoformat()
                            }
                            events.append(event)
                            
                        except Exception as e:
                            print(f"⚠️  Не удалось получить {page_url}: {e}")
                        
                        time.sleep(0.5)  # Задержка между запросами
                        
        except Exception as e:
            print(f"❌ Ошибка парсинга Sitemap {url}: {e}")
        
        return events
    
    def scrape_blog(self, url: str, competitor: str) -> List[Dict]:
        """Парсит HTML-страницу блога"""
        events = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ищем статьи (универсальный подход)
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['post', 'article', 'blog', 'card']
            ))[:10]
            
            for article in articles:
                # Ищем заголовок
                title_tag = article.find(['h1', 'h2', 'h3', 'a'])
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                
                # Ищем ссылку
                link_tag = article.find('a', href=True)
                if link_tag:
                    article_url = link_tag['href']
                    if not article_url.startswith('http'):
                        # Относительный URL
                        from urllib.parse import urljoin
                        article_url = urljoin(url, article_url)
                else:
                    continue
                
                # Ищем описание
                desc_tag = article.find(['p', 'div'], class_=lambda x: x and 'description' in str(x).lower())
                description = desc_tag.text.strip()[:500] if desc_tag else ''
                
                event = {
                    'id': self.generate_event_id(article_url, title),
                    'competitor': competitor,
                    'title': title,
                    'url': article_url,
                    'description': description,
                    'published_at': datetime.now().isoformat(),
                    'source_type': 'Blog',
                    'raw': description,
                    'collected_at': datetime.now().isoformat()
                }
                events.append(event)
                
        except Exception as e:
            print(f"❌ Ошибка парсинга Blog {url}: {e}")
        
        return events
    
    def scrape_all(self) -> List[Dict]:
        """Собирает события со всех источников"""
        all_events = []
        
        for competitor, sources in COMPETITORS.items():
            print(f"\n🔍 Сбор данных: {competitor}")
            
            for source_type, url in sources.items():
                print(f"  📡 {source_type}: {url}")
                
                if source_type == 'rss':
                    events = self.scrape_rss(url, competitor)
                elif source_type == 'sitemap':
                    events = self.scrape_sitemap(url, competitor)
                elif source_type == 'blog':
                    events = self.scrape_blog(url, competitor)
                else:
                    continue
                
                print(f"    ✓ Найдено событий: {len(events)}")
                all_events.extend(events)
                
                time.sleep(1)  # Задержка между источниками
        
        # Удаляем дубликаты по ID
        unique_events = {event['id']: event for event in all_events}
        
        print(f"\n📊 Всего собрано уникальных событий: {len(unique_events)}")
        return list(unique_events.values())


if __name__ == '__main__':
    scraper = EventScraper()
    events = scraper.scrape_all()
    
    print("\n" + "=" * 80)
    print("ПРИМЕРЫ СОБРАННЫХ СОБЫТИЙ:")
    print("=" * 80)
    
    for i, event in enumerate(events[:3], 1):
        print(f"\n{i}. {event['competitor']} - {event['title']}")
        print(f"   URL: {event['url']}")
        print(f"   Источник: {event['source_type']}")
