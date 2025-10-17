# LinkedIn Content Automation System

An intelligent automation system that scrapes trending tech news, generates SEO-optimized LinkedIn posts, and schedules them automatically to boost your professional presence.

## 🚀 Features

- **Multi-Source Scraping**: Collects content from 6 reliable tech sources daily
- **AI-Powered Content Generation**: Creates engaging, SEO-optimized LinkedIn posts
- **Smart Scheduling**: Auto-posts at optimal times (9 PM daily, prioritizes Tue-Thu)
- **Engagement Tracking**: Monitors post performance and adapts strategy
- **Professional Tone**: Maintains insightful, conversational, and credible content

## 📋 Content Sources

1. TechCrunch - Latest tech news
2. Analytics Insight - AI and data analytics trends
3. Business Insider AI - Business tech innovations
4. World Economic Forum - Future of work insights
5. Product Hunt - New product launches
6. Forbes AI - AI industry analysis

## 🎯 Topic Categories

- AI tools and their practical uses
- Job market and future of work trends
- Evolving AI technologies and breakthroughs
- Tech innovations and automation updates
- Viral insights for professionals and creators

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- LinkedIn Developer Account (for API access)
- OpenAI API key or Anthropic Claude API key

### Setup Steps

1. **Clone and navigate to the project**:
```powershell
cd "c:\Users\heman\OneDrive\Pictures\redmi note 11\New folder\Projects folder\webscraping"
```

2. **Create virtual environment**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Add your API keys and credentials

5. **Initialize database**:
```powershell
python -m src.database.init_db
```

## ⚙️ Configuration

Edit `config.yaml` to customize:

- **Posting schedule**: Default is 9 PM daily
- **Content preferences**: Adjust topic weights and filters
- **Engagement thresholds**: Set minimum performance metrics
- **Tone settings**: Fine-tune writing style

## 🏃 Usage

### Run Once (Manual Mode)
```powershell
python main.py --mode manual
```

### Run Daily Automation
```powershell
python main.py --mode auto
```

### Test Scraping Only
```powershell
python main.py --test-scrape
```

### Generate Sample Posts
```powershell
python main.py --generate-samples
```

## 🌐 Cloud Deployment

### Deploy to Render.com (FREE - No Credit Card!)

Deploy your automation to run 24/7:

```powershell
.\deploy_to_render.ps1
```

**Then follow the instructions to:**
1. Push to GitHub
2. Deploy on Render.com (5 minutes!)
3. Monitor logs at dashboard.render.com

**See full guide:** `RENDER_DEPLOY.md`

---

## 📊 Output Format

Each daily run generates:

```
Topic Title: [Trending Topic]
Source URL: [Original Article]
Summary: [6-10 line overview]
LinkedIn Post: [100-150 words, SEO-optimized]
Hashtags: #AI #FutureOfWork #TechTrends
Posting Time: 9:00 PM (Tue-Thu prioritized)
```

## 📈 Engagement Tracking

The system automatically:
- Logs post performance (likes, comments, shares)
- Analyzes which topics perform best
- Adjusts tone and hashtag strategy
- Provides weekly performance reports

## 🔒 Security

- All credentials stored in `.env` (never committed)
- API keys encrypted at rest
- LinkedIn OAuth 2.0 authentication
- Rate limiting to comply with platform policies

## 📁 Project Structure

```
webscraping/
├── .github/
│   └── copilot-instructions.md
├── src/
│   ├── scrapers/           # Web scraping modules
│   ├── analyzers/          # Content analysis
│   ├── generators/         # Post generation
│   ├── schedulers/         # Posting automation
│   ├── trackers/           # Engagement monitoring
│   └── database/           # Data persistence
├── data/                   # Scraped content & logs
├── config/                 # Configuration files
├── tests/                  # Unit and integration tests
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🛠️ Development

### Running Tests
```powershell
pytest tests/
```

### Code Formatting
```powershell
black src/
flake8 src/
```

### Adding New Sources

1. Create scraper in `src/scrapers/`
2. Register in `config/sources.yaml`
3. Test with `pytest tests/test_scrapers.py`

## 🤝 Contributing

This is a personal automation project. Feel free to fork and adapt for your needs.

## ⚠️ Disclaimer

- Follow LinkedIn's Terms of Service
- Respect posting limits and automation policies
- Verify all content before publishing
- Avoid spammy or misleading content

## 📝 License

MIT License - See LICENSE file for details

## 📧 Support

For issues or questions, check the troubleshooting guide in `docs/troubleshooting.md`

---

**Built with ❤️ to enhance your LinkedIn presence through intelligent automation**
