"""
TechCrunch scraper implementation
"""
from typing import Dict, List
from src.scrapers.base_scraper import BaseScraper
from loguru import logger


class TechCrunchScraper(BaseScraper):
    """Scraper for TechCrunch"""
    
    def scrape(self) -> List[Dict]:
        """Scrape articles from TechCrunch"""
        logger.info(f"📰 Scraping {self.name}...")
        
        # TechCrunch has RSS feed
        if self.rss_feed:
            articles = self.fetch_rss()
            if articles:
                return articles
        
        # Fallback to web scraping
        return self._scrape_web()
    
    def _scrape_web(self) -> List[Dict]:
        """Scrape TechCrunch website directly"""
        articles = []
        
        try:
            soup = self.fetch_page(self.url)
            if not soup:
                return articles
            
            # Find article elements (adjust selectors based on actual site structure)
            article_elements = soup.select('article.post-block')[:self.max_articles]
            
            for element in article_elements:
                try:
                    title_elem = element.select_one('h2.post-block__title a')
                    if not title_elem:
                        continue
                    
                    article = {
                        'title': self._clean_text(title_elem.get_text()),
                        'url': title_elem.get('href', ''),
                        'summary': self._extract_text_from_element(element, 'div.post-block__content'),
                        'source': self.name,
                        'source_url': self.url,
                    }
                    
                    if article['title'] and article['url']:
                        articles.append(article)
                    
                    self.rate_limit(0.5)
                    
                except Exception as e:
                    logger.debug(f"Error parsing article: {str(e)}")
                    continue
            
            self.article_count = len(articles)
            
        except Exception as e:
            logger.error(f"Error scraping {self.name}: {str(e)}")
        
        return articles
