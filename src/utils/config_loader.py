"""
Configuration loader utility
"""
import yaml
from pathlib import Path
from typing import Dict
from loguru import logger


def load_config(config_path: str = 'config/config.yaml') -> Dict:
    """Load configuration from YAML file"""
    try:
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return get_default_config()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Configuration loaded from {config_path}")
        return config
    
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return get_default_config()


def get_default_config() -> Dict:
    """Get default configuration"""
    return {
        'sources': {},
        'topic_categories': {},
        'schedule': {
            'default_time': '21:00',
            'timezone': 'America/New_York'
        },
        'content': {
            'post_length': {'min': 100, 'max': 150},
            'hashtags': {'min': 3, 'max': 5}
        },
        'engagement': {
            'enabled': True,
            'check_interval_hours': 6
        }
    }
