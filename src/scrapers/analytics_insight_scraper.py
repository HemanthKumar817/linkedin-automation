"""Analytics Insight scraper"""
from typing import Dict, List
from src.scrapers.base_scraper import BaseScraper
from loguru import logger

class AnalyticsInsightScraper(BaseScraper):
    def scrape(self) -> List[Dict]:
        if self.rss_feed:
            return self.fetch_rss()
        return []
