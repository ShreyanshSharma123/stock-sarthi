# 📈 Stock Saarthi - AI-Powered Stock Analysis Platform

> An intelligent stock analysis platform that helps beginner investors make informed decisions using AI, ML predictions, and real-world event analysis.

---

## 🎯 Project Overview

**Stock Saarthi** is designed to democratize stock market analysis for beginners by:

- Simplifying stock selection and analysis
- Providing AI-powered price predictions
- Analyzing real-world events that impact stock prices
- Offering clear Buy/Hold/Sell signals

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              STOCK SAARTHI ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐ │
│  │   FRONTEND   │────▶│   BACKEND    │────▶│      EXTERNAL SERVICES       │ │
│  │   (React)    │     │   (FastAPI)  │     │                              │ │
│  │              │     │              │     │  • Yahoo Finance API         │ │
│  │  • Dashboard │     │  • REST API  │     │  • News APIs                 │ │
│  │  • Charts    │     │  • WebSocket │     │  • Sentiment Analysis        │ │
│  │  • Alerts    │     │  • Auth      │     │                              │ │
│  └──────────────┘     └──────────────┘     └──────────────────────────────┘ │
│         │                    │                          │                    │
│         │                    ▼                          │                    │
│         │            ┌──────────────┐                   │                    │
│         │            │   ML ENGINE  │◀──────────────────┘                    │
│         │            │              │                                        │
│         │            │  • SVM/SVR   │                                        │
│         │            │  • LSTM      │                                        │
│         │            │  • Sentiment │                                        │
│         │            └──────────────┘                                        │
│         │                    │                                               │
│         │                    ▼                                               │
│         │            ┌──────────────┐                                        │
│         └───────────▶│   DATABASE   │                                        │
│                      │  (PostgreSQL)│                                        │
│                      │   + Redis    │                                        │
│                      └──────────────┘                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  User Input │───▶│ Data Fetch  │───▶│ ML Process  │───▶│  Response   │
│  (Stock)    │    │ (API Calls) │    │ (Predict)   │    │ (Signals)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                         │                   │
                         ▼                   ▼
                  ┌─────────────┐    ┌─────────────┐
                  │ News/Events │───▶│  Sentiment  │
                  │   Fetch     │    │  Analysis   │
                  └─────────────┘    └─────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

| Technology              | Purpose      | Why?                                           |
| ----------------------- | ------------ | ---------------------------------------------- |
| **React.js**            | UI Framework | Component-based, easy to learn, huge community |
| **Chart.js / Recharts** | Stock Charts | Beautiful, interactive charts                  |
| **Tailwind CSS**        | Styling      | Utility-first, rapid development               |
| **Axios**               | API Calls    | Simple HTTP requests                           |

### Backend

| Technology         | Purpose        | Why?                             |
| ------------------ | -------------- | -------------------------------- |
| **Python FastAPI** | REST API       | Fast, modern, auto-documentation |
| **WebSocket**      | Real-time Data | Live stock updates               |
| **Celery**         | Task Queue     | Background jobs (data fetching)  |
| **Redis**          | Caching        | Fast data retrieval              |

### Machine Learning

| Technology                    | Purpose              | Why?                            |
| ----------------------------- | -------------------- | ------------------------------- |
| **scikit-learn**              | SVM/SVR Models       | Easy to use, well-documented    |
| **TensorFlow/Keras**          | Deep Learning (LSTM) | Time-series prediction          |
| **NLTK / TextBlob**           | Sentiment Analysis   | News sentiment scoring          |
| **Hugging Face Transformers** | Advanced NLP         | FinBERT for financial sentiment |

### Database

| Technology                 | Purpose          | Why?                               |
| -------------------------- | ---------------- | ---------------------------------- |
| **PostgreSQL**             | Primary Database | Reliable, supports complex queries |
| **Redis**                  | Cache & Sessions | Fast, in-memory storage            |
| **TimescaleDB (optional)** | Time-series Data | Optimized for stock data           |

### DevOps (Future)

| Technology         | Purpose          |
| ------------------ | ---------------- |
| **Docker**         | Containerization |
| **AWS / GCP**      | Cloud Hosting    |
| **GitHub Actions** | CI/CD            |

---

## 📊 Data Collection Guide

### 1. Stock Data Collection (Yahoo Finance)

```python
# Simple example using yfinance
import yfinance as yf

# Get stock data
stock = yf.Ticker("RELIANCE.NS")  # .NS for NSE stocks

# Historical data
hist = stock.history(period="1y")  # 1 year of data

# Live price
live_price = stock.info['regularMarketPrice']
```

**Data You Can Collect:**

- Open, High, Low, Close prices
- Volume
- Market Cap
- P/E Ratio
- 52-week high/low
- Dividend yield

### 2. News Data Collection

**Option A: NewsAPI (Free tier available)**

```python
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='YOUR_API_KEY')

# Get news about a company
news = newsapi.get_everything(
    q='Reliance Industries',
    language='en',
    sort_by='publishedAt',
    page_size=10
)
```

**Option B: Google News RSS (Free)**

```python
import feedparser

def get_news(company_name):
    url = f"https://news.google.com/rss/search?q={company_name}&hl=en-IN"
    feed = feedparser.parse(url)
    return feed.entries
```

**Option C: Financial News APIs**

- Finnhub Stock API 
- News API

---

## 🧠 Machine Learning Pipeline

### Complete ML Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ML PIPELINE                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│  │  DATA   │──▶│ PREPROC │──▶│ FEATURE │──▶│  TRAIN  │──▶│ PREDICT │       │
│  │ COLLECT │   │  ESS    │   │   ENG   │   │  MODEL  │   │         │       │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘       │
│       │             │             │             │             │              │
│       ▼             ▼             ▼             ▼             ▼              │
│  • Stock API   • Clean NaN  • Moving Avg  • SVM/SVR    • Price Pred        │
│  • News API    • Normalize  • RSI, MACD   • LSTM       • Signal Gen        │
│  • Events      • Scale      • Sentiment   • Ensemble   • Confidence        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Feature Engineering for Stock Prediction

**Technical Indicators:**

```python
# Features we'll calculate
features = {
    'SMA_10': 'Simple Moving Average (10 days)',
    'SMA_50': 'Simple Moving Average (50 days)',
    'EMA_10': 'Exponential Moving Average',
    'RSI': 'Relative Strength Index',
    'MACD': 'Moving Average Convergence Divergence',
    'Bollinger_Upper': 'Bollinger Band Upper',
    'Bollinger_Lower': 'Bollinger Band Lower',
    'Volume_Change': 'Volume change percentage',
    'Daily_Return': 'Daily return percentage'
}
```

**Sentiment Features:**

```python
sentiment_features = {
    'news_sentiment': 'Average sentiment of recent news (-1 to 1)',
    'event_impact': 'Predicted impact of upcoming events',
    'social_sentiment': 'Social media sentiment score'
}
```

---

## 🎭 Event Sentiment Analysis Integration

### How Events Affect Stock Prices

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    EVENT IMPACT ANALYSIS                                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Event Type           │ Typical Impact      │ Sectors Affected           │
│  ─────────────────────┼─────────────────────┼─────────────────────────── │
│  Budget Announcement  │ High (±5-10%)       │ Banking, Infra, Auto       │
│  Elections            │ High (±3-8%)        │ All sectors                │
│  RBI Rate Decision    │ Medium (±2-5%)      │ Banking, Real Estate       │
│  Quarterly Results    │ Medium (±5-15%)     │ Specific company           │
│  Global Events        │ Variable            │ IT, Pharma, Export         │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Sentiment Analysis Pipeline

```python
# Step 1: Collect news about an event
news = get_news("Union Budget 2024")

# Step 2: Analyze sentiment
from transformers import pipeline

# Using FinBERT for financial sentiment
finbert = pipeline("sentiment-analysis",
                   model="ProsusAI/finbert")

sentiments = []
for article in news:
    result = finbert(article['title'])
    sentiments.append(result[0])

# Step 3: Calculate aggregate sentiment
avg_sentiment = calculate_average_sentiment(sentiments)

# Step 4: Integrate into prediction
prediction_with_sentiment = model.predict(
    technical_features + [avg_sentiment]
)
```

---

## 💾 Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐            │
│  │    USERS     │       │   STOCKS     │       │    NEWS      │            │
│  ├──────────────┤       ├──────────────┤       ├──────────────┤            │
│  │ id (PK)      │       │ symbol (PK)  │       │ id (PK)      │            │
│  │ email        │       │ name         │       │ title        │            │
│  │ password     │       │ sector       │       │ content      │            │
│  │ created_at   │       │ market_cap   │       │ sentiment    │            │
│  └──────────────┘       └──────────────┘       │ stock_symbol │            │
│         │                      │               │ published_at │            │
│         │                      │               └──────────────┘            │
│         ▼                      ▼                      │                     │
│  ┌──────────────┐       ┌──────────────┐              │                     │
│  │  WATCHLIST   │       │ STOCK_DATA   │              │                     │
│  ├──────────────┤       ├──────────────┤              │                     │
│  │ user_id (FK) │       │ id (PK)      │              │                     │
│  │ symbol (FK)  │       │ symbol (FK)  │◀─────────────┘                     │
│  │ created_at   │       │ date         │                                    │
│  └──────────────┘       │ open         │       ┌──────────────┐            │
│                         │ high         │       │ PREDICTIONS  │            │
│                         │ low          │       ├──────────────┤            │
│                         │ close        │       │ id (PK)      │            │
│                         │ volume       │       │ symbol (FK)  │            │
│                         └──────────────┘       │ predicted_at │            │
│                                                │ target_date  │            │
│                                                │ predicted_price │         │
│                                                │ signal        │            │
│                                                │ confidence    │            │
│                                                └──────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ UI Pages Required

### Page Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              UI PAGES                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 🏠 Landing Page                                                         │
│     ├── Hero section with value proposition                                 │
│     ├── Features overview                                                   │
│     ├── How it works                                                        │
│     └── CTA to signup                                                       │
│                                                                              │
│  2. 🔐 Auth Pages                                                           │
│     ├── Login                                                               │
│     ├── Register                                                            │
│     └── Forgot Password                                                     │
│                                                                              │
│  3. 📊 Dashboard                                                            │
│     ├── Portfolio summary                                                   │
│     ├── Watchlist stocks                                                    │
│     ├── Market overview (Nifty, Sensex)                                     │
│     ├── Top gainers/losers                                                  │
│     └── Recent predictions                                                  │
│                                                                              │
│  4. 📈 Stock Analysis Page                                                  │
│     ├── Stock search/selector                                               │
│     ├── Price chart (candlestick)                                           │
│     ├── Technical indicators                                                │
│     ├── AI prediction with confidence                                       │
│     ├── Buy/Hold/Sell signal                                                │
│     ├── News sentiment                                                      │
│     └── Related events                                                      │
│                                                                              │
│  5. 📰 News & Events Page                                                   │
│     ├── Latest financial news                                               │
│     ├── Upcoming events calendar                                            │
│     ├── Event impact predictions                                            │
│     └── Sector-wise news filter                                             │
│                                                                              │
│  6. 🔮 Predictions Page                                                     │
│     ├── All stock predictions                                               │
│     ├── Accuracy history                                                    │
│     ├── Model explanation                                                   │
│     └── Comparison charts                                                   │
│                                                                              │
│  7. ⚙️ Settings Page                                                        │
│     ├── Profile settings                                                    │
│     ├── Notification preferences                                            │
│     └── Watchlist management                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Advanced AI Features (USP)

### 1. **Event Impact Predictor**

```
When a major event is announced, the AI predicts:
- Which stocks will be affected
- Expected price movement direction
- Confidence score
- Historical comparison with similar events
```

### 2. **Multi-Factor Sentiment Analysis**

```
Combines sentiment from:
- News articles
- Social media (Twitter/X)
- Analyst reports
- Company announcements
- Government policies
```

### 3. **Explainable AI (XAI)**

```
Instead of just showing predictions, explain WHY:
- "Price likely to increase because:
  - RSI indicates oversold condition
  - Positive earnings surprise
  - Sector showing upward trend
  - Recent government policy favorable"
```

### 4. **Pattern Recognition**

```
AI identifies chart patterns:
- Head and Shoulders
- Double Top/Bottom
- Cup and Handle
- Breakout patterns
```

### 5. **Smart Alerts**

```
Intelligent notifications:
- "Reliance approaching your target price"
- "Significant news detected for watched stocks"
- "Market conditions suggest portfolio review"
```

### 6. **What-If Analysis**

```
Scenario modeling:
- "What if RBI increases rates by 0.5%?"
- "What if crude oil prices rise 20%?"
- Show impact on portfolio
```

---

## 📁 Project Folder Structure

See the complete folder structure in the project files.

---

## 🎯 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis

### Quick Start

```bash
# 1. Clone and setup backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Setup database
# Create PostgreSQL database named 'stock_saarthi'

# 3. Run migrations
python -c "from database.models import Base, engine; Base.metadata.create_all(engine)"

# 4. Start backend
uvicorn main:app --reload

# 5. Setup frontend (new terminal)
cd frontend
npm install
npm start
```

---

## 📚 Learning Resources

### For Second-Year Students

**Python & ML:**

- [Python for Everybody - Coursera](https://www.coursera.org/specializations/python)
- [Machine Learning by Andrew Ng](https://www.coursera.org/learn/machine-learning)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)

**Web Development:**

- [React Official Tutorial](https://react.dev/learn)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

**Stock Market:**

- [Investopedia](https://www.investopedia.com/)
- [Zerodha Varsity](https://zerodha.com/varsity/)

---

##  Features 

- [ ] Real-time stock data updates
- [ ] AI predictions with confidence scores
- [ ] News sentiment analysis
- [ ] Event impact prediction
- [ ] Interactive charts
- [ ] User authentication
- [ ] Watchlist functionality
- [ ] Mobile-responsive design
- [ ] API documentation (auto-generated by FastAPI)

## 🚀 Startup-Level Features (Future Scope)

- [ ] Paper trading functionality
- [ ] Real broker integration (Zerodha, Groww APIs)
- [ ] Portfolio optimization suggestions
- [ ] Risk assessment tools
- [ ] Social features (follow traders)
- [ ] Premium subscription model
- [ ] Mobile app (React Native)
- [ ] Automated trading bots

---

## 👥 Contributing

This is a hackathon project. Feel free to fork and build upon it!

## 📄 License

MIT License - feel free to use for learning and building.

---

**Built with ❤️ by Team Stock Saarthi**
