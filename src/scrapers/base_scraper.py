"""
Base scraper class with common functionality
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from loguru import logger
import time
from datetime import datetime
import feedparser


class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, config: Dict):
        """Initialize base scraper"""
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.url = config.get('url', '')
        self.rss_feed = config.get('rss_feed', None)
        self.enabled = config.get('enabled', True)
        self.max_articles = config.get('max_articles', 10)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.article_count = 0
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape articles from source - must be implemented by subclasses"""
        pass
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def fetch_rss(self, feed_url: Optional[str] = None) -> List[Dict]:
        """Fetch articles from RSS feed"""
        feed_url = feed_url or self.rss_feed
        if not feed_url:
            return []
        
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'summary': self._clean_text(entry.get('summary', '')),
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source': self.name,
                    'source_url': self.url,
                    'scraped_at': datetime.now().isoformat()
                }
                articles.append(article)
            
            self.article_count = len(articles)
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS from {feed_url}: {str(e)}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _extract_text_from_element(self, element, selector: str) -> str:
        """Safely extract text from element"""
        try:
            found = element.select_one(selector)
            if found:
                return self._clean_text(found.get_text())
        except Exception:
            pass
        return ""
    
    def rate_limit(self, delay: float = 1.0):
        """Rate limiting between requests"""
        time.sleep(delay)
