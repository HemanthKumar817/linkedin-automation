"""
Topic Analyzer - identifies trending topics from scraped articles
"""
from typing import Dict, List
from collections import Counter
import re
from loguru import logger


class TopicAnalyzer:
    """Analyzes articles to identify trending topics"""
    
    def __init__(self, config: Dict):
        """Initialize topic analyzer"""
        self.config = config
        self.topic_categories = config.get('topic_categories', {})
    
    def identify_trending_topics(self, articles: List[Dict], count: int = 5) -> List[Dict]:
        """Identify top trending topics from articles"""
        logger.info(f"🔍 Analyzing {len(articles)} articles for trending topics...")
        
        if not articles:
            logger.warning("No articles to analyze")
            return []
        
        # Score articles based on keywords and categories
        scored_articles = []
        for article in articles:
            score = self._calculate_relevance_score(article)
            scored_articles.append({
                **article,
                'relevance_score': score
            })
        
        # Sort by relevance score
        scored_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Get top N diverse topics
        trending_topics = self._select_diverse_topics(scored_articles, count)
        
        logger.info(f"✅ Identified {len(trending_topics)} trending topics")
        return trending_topics
    
    def _calculate_relevance_score(self, article: Dict) -> float:
        """Calculate relevance score for an article"""
        score = 1.0
        
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        combined_text = f"{title} {summary}"
        
        # Check each category
        for category_key, category_data in self.topic_categories.items():
            keywords = category_data.get('keywords', [])
            weight = category_data.get('weight', 1.0)
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword.lower() in combined_text)
            
            if matches > 0:
                score += matches * weight
                article['category'] = category_key
        
        return score
    
    def _select_diverse_topics(self, scored_articles: List[Dict], count: int) -> List[Dict]:
        """Select diverse topics across different categories"""
        selected = []
        categories_used = set()
        
        # First pass: one from each category
        for article in scored_articles:
            category = article.get('category', 'general')
            if category not in categories_used:
                selected.append(article)
                categories_used.add(category)
                if len(selected) >= count:
                    break
        
        # Second pass: fill remaining slots with highest scores
        if len(selected) < count:
            for article in scored_articles:
                if article not in selected:
                    selected.append(article)
                    if len(selected) >= count:
                        break
        
        return selected[:count]
    
    def categorize_article(self, article: Dict) -> str:
        """Determine the category of an article"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        combined_text = f"{title} {summary}"
        
        best_category = 'general'
        best_score = 0
        
        for category_key, category_data in self.topic_categories.items():
            keywords = category_data.get('keywords', [])
            matches = sum(1 for keyword in keywords if keyword.lower() in combined_text)
            
            if matches > best_score:
                best_score = matches
                best_category = category_key
        
        return best_category
