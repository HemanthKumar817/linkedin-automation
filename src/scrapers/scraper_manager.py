"""
Scraper Manager - coordinates all web scraping operations
"""
from typing import Dict, List
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml

from src.scrapers.techcrunch_scraper import TechCrunchScraper
from src.scrapers.analytics_insight_scraper import AnalyticsInsightScraper
from src.scrapers.business_insider_scraper import BusinessInsiderScraper
from src.scrapers.weforum_scraper import WeForumScraper
from src.scrapers.producthunt_scraper import ProductHuntScraper
from src.scrapers.forbes_scraper import ForbesScraper


class ScraperManager:
    """Manages all scrapers and aggregates results"""
    
    def __init__(self, config: Dict):
        """Initialize scraper manager with configuration"""
        self.config = config
        self.sources_config = config.get('sources', {})
        
        # Initialize scrapers
        self.scrapers = {
            'techcrunch': TechCrunchScraper(self.sources_config.get('techcrunch', {})),
            'analytics_insight': AnalyticsInsightScraper(self.sources_config.get('analytics_insight', {})),
            'business_insider': BusinessInsiderScraper(self.sources_config.get('business_insider', {})),
            'weforum': WeForumScraper(self.sources_config.get('weforum', {})),
            'producthunt': ProductHuntScraper(self.sources_config.get('producthunt', {})),
            'forbes': ForbesScraper(self.sources_config.get('forbes', {}))
        }
        
        logger.info(f"✅ Initialized {len(self.scrapers)} scrapers")
    
    def scrape_all_sources(self, max_workers: int = 3) -> List[Dict]:
        """Scrape all enabled sources in parallel"""
        all_articles = []
        
        # Filter enabled scrapers
        enabled_scrapers = {
            name: scraper for name, scraper in self.scrapers.items()
            if self.sources_config.get(name, {}).get('enabled', True)
        }
        
        logger.info(f"📰 Scraping {len(enabled_scrapers)} sources...")
        
        # Scrape in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_source = {
                executor.submit(scraper.scrape): name
                for name, scraper in enabled_scrapers.items()
            }
            
            for future in as_completed(future_to_source):
                source_name = future_to_source[future]
                try:
                    articles = future.result()
                    all_articles.extend(articles)
                    logger.info(f"  ✓ {source_name}: {len(articles)} articles")
                except Exception as e:
                    logger.error(f"  ✗ {source_name}: Failed - {str(e)}")
        
        return all_articles
    
    def scrape_source(self, source_name: str) -> List[Dict]:
        """Scrape a specific source"""
        if source_name not in self.scrapers:
            raise ValueError(f"Unknown source: {source_name}")
        
        scraper = self.scrapers[source_name]
        return scraper.scrape()
    
    def get_source_counts(self) -> Dict[str, int]:
        """Get article count per source"""
        counts = {}
        for name, scraper in self.scrapers.items():
            if hasattr(scraper, 'article_count'):
                counts[name] = scraper.article_count
            else:
                counts[name] = 0
        return counts
