"""
Automation orchestrator - coordinates all automation components
"""
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import schedule
import time

from src.scrapers.scraper_manager import ScraperManager
from src.analyzers.topic_analyzer import TopicAnalyzer
from src.generators.post_generator import PostGenerator
from src.schedulers.post_scheduler import PostScheduler
from src.trackers.engagement_tracker import EngagementTracker
from src.database.db_manager import DatabaseManager


class AutomationOrchestrator:
    """Orchestrates the entire automation workflow"""
    
    def __init__(self, config: Dict, dry_run: bool = False):
        """Initialize orchestrator with configuration"""
        self.config = config
        self.dry_run = dry_run
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.scraper_manager = ScraperManager(config)
        self.topic_analyzer = TopicAnalyzer(config)
        self.post_generator = PostGenerator(config)
        self.post_scheduler = PostScheduler(config, dry_run=dry_run)
        self.engagement_tracker = EngagementTracker(config)
        
        logger.info("✅ Orchestrator initialized")
    
    def run_once(self) -> None:
        """Execute complete workflow once"""
        logger.info("🔄 Starting single execution cycle...")
        
        try:
            # Step 1: Scrape content
            logger.info("📰 Scraping content from sources...")
            articles = self.scraper_manager.scrape_all_sources()
            logger.info(f"✅ Scraped {len(articles)} articles")
            
            # Step 2: Analyze and identify trending topics
            logger.info("🔍 Analyzing topics...")
            trending_topics = self.topic_analyzer.identify_trending_topics(
                articles, 
                count=self.config.get('content', {}).get('daily_topics_count', 5)
            )
            logger.info(f"✅ Identified {len(trending_topics)} trending topics")
            
            # Step 3: Generate LinkedIn posts
            logger.info("✍️ Generating LinkedIn posts...")
            posts = []
            for topic in trending_topics:
                post = self.post_generator.generate_post(topic)
                posts.append(post)
                logger.info(f"  ✓ Generated post for: {topic['title']}")
            
            # Step 4: Save to database
            logger.info("💾 Saving posts to database...")
            for post in posts:
                self.db_manager.save_post(post)
            
            # Step 5: Schedule posts
            logger.info("📅 Scheduling posts...")
            scheduled_count = self.post_scheduler.schedule_posts(posts)
            logger.info(f"✅ Scheduled {scheduled_count} posts")
            
            # Step 6: Track previous posts engagement
            logger.info("📊 Tracking engagement on previous posts...")
            self.engagement_tracker.update_all_engagements()
            
            logger.info("✅ Execution cycle completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error in execution cycle: {str(e)}")
            raise
    
    def run_scheduled(self) -> None:
        """Run on schedule indefinitely"""
        logger.info("⏰ Setting up scheduled automation...")
        
        # Get schedule configuration
        schedule_config = self.config.get('schedule', {})
        default_time = schedule_config.get('default_time', '21:00')
        
        # Schedule daily run
        schedule.every().day.at(default_time).do(self.run_once)
        
        # Schedule engagement tracking every 6 hours
        schedule.every(6).hours.do(self.engagement_tracker.update_all_engagements)
        
        logger.info(f"✅ Scheduled daily run at {default_time}")
        logger.info("✅ Scheduled engagement tracking every 6 hours")
        logger.info("⏳ Waiting for scheduled time... (Press Ctrl+C to stop)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("⚠️ Scheduler stopped by user")
    
    def test_scraping(self) -> None:
        """Test scraping functionality"""
        logger.info("🧪 Testing scraping functionality...")
        
        articles = self.scraper_manager.scrape_all_sources()
        
        logger.info(f"\n📊 Scraping Results:")
        logger.info(f"Total articles: {len(articles)}")
        
        for source, count in self.scraper_manager.get_source_counts().items():
            logger.info(f"  • {source}: {count} articles")
        
        if articles:
            logger.info(f"\n📄 Sample article:")
            sample = articles[0]
            logger.info(f"  Title: {sample.get('title', 'N/A')}")
            logger.info(f"  Source: {sample.get('source', 'N/A')}")
            logger.info(f"  URL: {sample.get('url', 'N/A')}")
            logger.info(f"  Summary: {sample.get('summary', 'N/A')[:100]}...")
    
    def generate_sample_posts(self, count: int = 5) -> None:
        """Generate sample posts without scraping"""
        logger.info(f"✍️ Generating {count} sample posts...")
        
        # Use some sample topics
        sample_topics = [
            {
                'title': 'AI-Powered Coding Assistants Transform Development',
                'summary': 'New AI coding tools are helping developers write code faster and with fewer bugs.',
                'url': 'https://example.com/ai-coding',
                'source': 'TechCrunch',
                'category': 'ai_tools'
            },
            {
                'title': 'Remote Work Trends: What 2025 Holds',
                'summary': 'Companies are adopting hybrid models as remote work becomes permanent.',
                'url': 'https://example.com/remote-work',
                'source': 'World Economic Forum',
                'category': 'job_market'
            },
            {
                'title': 'Breakthrough in Natural Language Processing',
                'summary': 'New NLP models achieve human-level understanding in complex conversations.',
                'url': 'https://example.com/nlp-breakthrough',
                'source': 'Forbes AI',
                'category': 'ai_technology'
            },
            {
                'title': 'Automation Reaches New Industries',
                'summary': 'Manufacturing and healthcare see major automation adoption.',
                'url': 'https://example.com/automation',
                'source': 'Business Insider',
                'category': 'tech_innovation'
            },
            {
                'title': 'Top Productivity Hacks from Tech Leaders',
                'summary': 'CEOs share their secrets to staying productive in fast-paced environments.',
                'url': 'https://example.com/productivity',
                'source': 'Product Hunt',
                'category': 'viral_insights'
            }
        ]
        
        for i, topic in enumerate(sample_topics[:count], 1):
            logger.info(f"\n📝 Generating post {i}/{count}...")
            post = self.post_generator.generate_post(topic)
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Topic: {post['topic_title']}")
            logger.info(f"Source: {post['source_name']}")
            logger.info(f"URL: {post['source_url']}")
            logger.info(f"\nSummary:\n{post['summary']}")
            logger.info(f"\nLinkedIn Post:\n{post['content']}")
            logger.info(f"\nHashtags: {post['hashtags']}")
            logger.info(f"Posting Time: {post['suggested_posting_time']}")
            logger.info(f"{'='*60}")
