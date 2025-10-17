"""
Post Generator - creates SEO-optimized LinkedIn posts using AI
"""
from typing import Dict, List
import os
from loguru import logger
import random
from datetime import datetime


class PostGenerator:
    """Generates LinkedIn posts from topics using AI"""
    
    def __init__(self, config: Dict):
        """Initialize post generator"""
        self.config = config
        self.content_config = config.get('content', {})
        self.seo_config = config.get('seo', {})
        
        # Determine AI provider
        self.ai_provider = os.getenv('AI_PROVIDER', 'gemini')
        
        if self.ai_provider == 'openai':
            self._init_openai()
        elif self.ai_provider == 'anthropic':
            self._init_anthropic()
        elif self.ai_provider == 'gemini':
            self._init_gemini()
        else:
            logger.warning(f"Unknown AI provider: {self.ai_provider}, using fallback")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
                self.model = os.getenv('AI_MODEL', 'gpt-4-turbo')
                logger.info("✅ OpenAI client initialized")
            else:
                logger.warning("OpenAI API key not found")
                self.client = None
        except ImportError:
            logger.warning("OpenAI package not installed")
            self.client = None
    
    def _init_anthropic(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = os.getenv('AI_MODEL', 'claude-3-sonnet-20240229')
                logger.info("✅ Anthropic client initialized")
            else:
                logger.warning("Anthropic API key not found")
                self.client = None
        except ImportError:
            logger.warning("Anthropic package not installed")
            self.client = None
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.model = os.getenv('AI_MODEL', 'gemini-1.5-pro')
                
                # Configure safety settings - allow most content for business/tech topics
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
                
                self.client = genai.GenerativeModel(
                    self.model,
                    safety_settings=safety_settings
                )
                logger.info(f"✅ Gemini client initialized with model: {self.model}")
            else:
                logger.warning("Gemini API key not found")
                self.client = None
        except ImportError:
            logger.warning("Google Generative AI package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing Gemini: {str(e)}")
            self.client = None
    
    def generate_post(self, topic: Dict) -> Dict:
        """Generate a complete LinkedIn post from a topic"""
        logger.info(f"✍️ Generating post for: {topic.get('title', 'Unknown')}")
        
        # Generate post content
        if self.client:
            content = self._generate_with_ai(topic)
        else:
            content = self._generate_fallback(topic)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(topic)
        
        # Determine posting time
        posting_time = self._suggest_posting_time()
        
        post = {
            'topic_title': topic.get('title', ''),
            'source_name': topic.get('source', ''),
            'source_url': topic.get('url', ''),
            'summary': topic.get('summary', ''),
            'content': content,
            'hashtags': ' '.join(hashtags),
            'suggested_posting_time': posting_time,
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        return post
    
    def _generate_with_ai(self, topic: Dict) -> str:
        """Generate post content using AI"""
        prompt = self._create_prompt(topic)
        
        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a professional LinkedIn content creator who writes engaging, SEO-optimized posts."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif self.ai_provider == 'anthropic':
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=300,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text.strip()
            
            elif self.ai_provider == 'gemini':
                response = self.client.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 300,
                    }
                )
                return response.text.strip()
        
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return self._generate_fallback(topic)
    
    def _create_prompt(self, topic: Dict) -> str:
        """Create prompt for AI generation"""
        post_length = self.content_config.get('post_length', {})
        min_length = post_length.get('min', 100)
        max_length = post_length.get('max', 150)
        
        prompt = f"""Create a professional LinkedIn post about this topic:

Title: {topic.get('title', '')}
Summary: {topic.get('summary', '')}
Source: {topic.get('source', '')}

Requirements:
- Length: {min_length}-{max_length} words
- Start with a catchy hook line
- Include key insights in plain language
- Professional, insightful, and slightly conversational tone
- End with a one-line call to action (question to engage readers)
- Naturally include SEO keywords
- Avoid clickbait or sensationalism
- Focus on value for professionals and creators

Write only the post content, no hashtags (those will be added separately)."""
        
        return prompt
    
    def _generate_fallback(self, topic: Dict) -> str:
        """Generate post without AI (fallback)"""
        title = topic.get('title', '')
        summary = topic.get('summary', '')
        
        hooks = [
            "Here's something you need to know:",
            "This is changing the game:",
            "Interesting development:",
            "Worth your attention:",
            "Big news in tech:"
        ]
        
        ctas = [
            "What are your thoughts on this?",
            "How is this impacting your work?",
            "Have you experienced this trend?",
            "What's your take on this?",
            "Are you seeing similar changes?"
        ]
        
        hook = random.choice(hooks)
        cta = random.choice(ctas)
        
        post = f"{hook}\n\n{title}\n\n{summary[:200]}...\n\n{cta}"
        
        return post
    
    def _generate_hashtags(self, topic: Dict) -> List[str]:
        """Generate relevant hashtags"""
        hashtag_config = self.content_config.get('hashtags', {})
        min_count = hashtag_config.get('min', 3)
        max_count = hashtag_config.get('max', 5)
        
        # Common trending hashtags
        trending = ['#AI', '#TechTrends', '#Innovation', '#FutureOfWork', '#Automation', 
                   '#DigitalTransformation', '#Technology', '#Business', '#Productivity']
        
        # Category-specific hashtags
        category_hashtags = {
            'ai_tools': ['#AITools', '#ChatGPT', '#AIAssistant', '#MachineLearning'],
            'job_market': ['#CareerGrowth', '#JobMarket', '#RemoteWork', '#Skills'],
            'ai_technology': ['#ArtificialIntelligence', '#DeepLearning', '#TechInnovation'],
            'tech_innovation': ['#TechNews', '#StartupLife', '#Innovation'],
            'viral_insights': ['#Leadership', '#ProfessionalGrowth', '#Insights']
        }
        
        # Get category-specific hashtags
        category = topic.get('category', 'general')
        specific_tags = category_hashtags.get(category, [])
        
        # Combine and select
        all_tags = list(set(trending + specific_tags))
        random.shuffle(all_tags)
        
        count = random.randint(min_count, max_count)
        return all_tags[:count]
    
    def _suggest_posting_time(self) -> str:
        """Suggest optimal posting time"""
        schedule_config = self.config.get('schedule', {})
        default_time = schedule_config.get('default_time', '21:00')
        priority_days = schedule_config.get('priority_days', [])
        
        now = datetime.now()
        day_name = now.strftime('%A')
        
        if day_name in priority_days:
            return f"{day_name} at {default_time} (High engagement day)"
        else:
            return f"{day_name} at {default_time}"
