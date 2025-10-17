"""
Main entry point for LinkedIn Content Automation System
"""
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.automation import AutomationOrchestrator
from src.utils.config_loader import load_config
from src.database.init_db import initialize_database


def setup_logging(log_level: str = "INFO"):
    """Configure logging"""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
        level=log_level
    )
    logger.add(
        "data/logs/automation_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level=log_level
    )


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="LinkedIn Content Automation System"
    )
    parser.add_argument(
        "--mode",
        choices=["manual", "auto"],
        default="auto",
        help="Run mode: manual (one-time) or auto (scheduled)"
    )
    parser.add_argument(
        "--test-scrape",
        action="store_true",
        help="Test scraping functionality only"
    )
    parser.add_argument(
        "--generate-samples",
        action="store_true",
        help="Generate sample posts without scraping"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without actually posting to LinkedIn"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging(args.log_level)
    
    logger.info("🚀 Starting LinkedIn Content Automation System")
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        initialize_database()
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        # Create orchestrator
        orchestrator = AutomationOrchestrator(
            config=config,
            dry_run=args.dry_run
        )
        
        # Execute based on mode
        if args.test_scrape:
            logger.info("🔍 Testing scraping functionality...")
            orchestrator.test_scraping()
            
        elif args.generate_samples:
            logger.info("✍️ Generating sample posts...")
            orchestrator.generate_sample_posts()
            
        elif args.mode == "manual":
            logger.info("🔄 Running manual execution...")
            orchestrator.run_once()
            
        else:  # auto mode
            logger.info("⏰ Starting automated scheduler...")
            orchestrator.run_scheduled()
        
        logger.info("✅ Execution completed successfully")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
