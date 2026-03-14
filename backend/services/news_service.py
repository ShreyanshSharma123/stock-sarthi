"""
News Service - Business logic for news and sentiment analysis
"""

import feedparser
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re


class NewsService:
    """
    Service class for fetching news and performing sentiment analysis
    """
    
    def __init__(self):
        # Simple sentiment word lists (basic approach)
        self.positive_words = {
            'growth', 'profit', 'surge', 'gain', 'rise', 'up', 'high', 'boost',
            'positive', 'strong', 'buy', 'bullish', 'outperform', 'beat', 'exceed',
            'upgrade', 'success', 'record', 'breakthrough', 'innovation', 'expand',
            'increase', 'improve', 'recovery', 'rally', 'optimistic', 'confident'
        }
        
        self.negative_words = {
            'loss', 'fall', 'decline', 'drop', 'down', 'low', 'weak', 'negative',
            'sell', 'bearish', 'underperform', 'miss', 'downgrade', 'concern',
            'risk', 'fear', 'crash', 'crisis', 'slump', 'plunge', 'warning',
            'decrease', 'struggle', 'volatile', 'uncertainty', 'lawsuit', 'scandal'
        }
        
        # Event keywords for classification
        self.event_keywords = {
            'budget': ['budget', 'fiscal', 'government spending', 'tax'],
            'election': ['election', 'vote', 'political', 'government'],
            'rbi_policy': ['rbi', 'reserve bank', 'interest rate', 'monetary policy', 'repo rate'],
            'earnings': ['earnings', 'quarterly results', 'profit', 'revenue', 'financial results'],
            'merger': ['merger', 'acquisition', 'takeover', 'deal'],
            'global': ['global', 'international', 'fed', 'us market', 'oil prices']
        }
    
    def get_latest_news(
        self, 
        limit: int = 20, 
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Get latest financial news from Google News RSS
        """
        try:
            # Build search query
            if category:
                query = f"India stock market {category}"
            else:
                query = "India stock market NSE BSE"
            
            query = query.replace(" ", "+")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
            
            feed = feedparser.parse(url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                # Analyze sentiment
                sentiment_result = self._analyze_sentiment(entry.title)
                
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "source": self._extract_source(entry.title),
                    "sentiment": sentiment_result["sentiment"],
                    "sentiment_score": sentiment_result["score"],
                    "event_type": self._classify_event(entry.title)
                })
            
            return news_items
            
        except Exception as e:
            # Return empty list on error
            return []
    
    def get_company_news(self, company_name: str, limit: int = 10) -> List[Dict]:
        """
        Get news for a specific company
        """
        try:
            query = f"{company_name} stock India".replace(" ", "+")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
            
            feed = feedparser.parse(url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                sentiment_result = self._analyze_sentiment(entry.title)
                
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "source": self._extract_source(entry.title),
                    "sentiment": sentiment_result["sentiment"],
                    "sentiment_score": sentiment_result["score"]
                })
            
            return news_items
            
        except Exception as e:
            return []
    
    def get_sentiment_analysis(self, symbol: str) -> Dict:
        """
        Get aggregated sentiment analysis for a stock
        """
        try:
            company_name = symbol.split(".")[0].title()
            news = self.get_company_news(company_name, limit=20)
            
            if not news:
                return {
                    "symbol": symbol,
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0,
                    "news_count": 0,
                    "breakdown": {"positive": 0, "neutral": 0, "negative": 0}
                }
            
            # Calculate aggregate sentiment
            total_score = 0
            breakdown = {"positive": 0, "neutral": 0, "negative": 0}
            
            for article in news:
                total_score += article["sentiment_score"]
                breakdown[article["sentiment"]] += 1
            
            avg_score = total_score / len(news)
            
            if avg_score > 0.1:
                overall = "positive"
            elif avg_score < -0.1:
                overall = "negative"
            else:
                overall = "neutral"
            
            return {
                "symbol": symbol,
                "overall_sentiment": overall,
                "sentiment_score": round(avg_score, 2),
                "news_count": len(news),
                "breakdown": breakdown,
                "recent_news": news[:5]
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing sentiment: {str(e)}")
    
    def get_upcoming_events(self, days: int = 30) -> List[Dict]:
        """
        Get upcoming economic events (simulated data)
        In production, this would fetch from an economic calendar API
        """
        # Sample events (in real app, fetch from economic calendar API)
        events = [
            {
                "id": 1,
                "title": "RBI Monetary Policy Meeting",
                "event_type": "rbi_policy",
                "date": (datetime.now() + timedelta(days=5)).isoformat(),
                "expected_impact": "high",
                "affected_sectors": ["Banking", "Finance", "Real Estate"],
                "description": "RBI to announce interest rate decision"
            },
            {
                "id": 2,
                "title": "Q3 Earnings Season",
                "event_type": "earnings",
                "date": (datetime.now() + timedelta(days=10)).isoformat(),
                "expected_impact": "high",
                "affected_sectors": ["All sectors"],
                "description": "Major companies will announce quarterly results"
            },
            {
                "id": 3,
                "title": "US Fed Meeting",
                "event_type": "global",
                "date": (datetime.now() + timedelta(days=15)).isoformat(),
                "expected_impact": "medium",
                "affected_sectors": ["IT", "Pharma", "Export-oriented"],
                "description": "Federal Reserve interest rate decision"
            },
            {
                "id": 4,
                "title": "Auto Sales Data Release",
                "event_type": "earnings",
                "date": (datetime.now() + timedelta(days=3)).isoformat(),
                "expected_impact": "medium",
                "affected_sectors": ["Auto", "Auto Ancillary"],
                "description": "Monthly auto sales figures"
            }
        ]
        
        return events
    
    def get_historical_event_impact(self, event_type: str) -> Dict:
        """
        Get historical impact of event types (simulated analysis)
        """
        # Historical analysis (simulated - in production, analyze real data)
        impact_analysis = {
            "budget": {
                "average_impact": 2.5,
                "typical_duration_days": 5,
                "most_affected_sectors": ["Banking", "Infrastructure", "Auto"],
                "historical_outcomes": [
                    {"year": 2024, "impact": "+2.8%", "sectors": "Banking rallied on tax benefits"},
                    {"year": 2023, "impact": "+1.5%", "sectors": "Infrastructure gained on capex focus"}
                ]
            },
            "election": {
                "average_impact": 4.0,
                "typical_duration_days": 30,
                "most_affected_sectors": ["All sectors"],
                "historical_outcomes": [
                    {"year": 2024, "impact": "+3.5%", "sectors": "Markets rallied on election results"},
                    {"year": 2019, "impact": "+4.2%", "sectors": "Strong mandate boosted confidence"}
                ]
            },
            "rbi_policy": {
                "average_impact": 1.5,
                "typical_duration_days": 3,
                "most_affected_sectors": ["Banking", "Finance", "Real Estate"],
                "historical_outcomes": [
                    {"year": 2024, "impact": "-0.8%", "sectors": "Rate hold disappointed some"},
                    {"year": 2023, "impact": "+1.2%", "sectors": "Rate pause supported banks"}
                ]
            },
            "earnings": {
                "average_impact": 5.0,
                "typical_duration_days": 7,
                "most_affected_sectors": ["Specific to company"],
                "historical_outcomes": [
                    {"note": "Earnings impact varies significantly by company performance"}
                ]
            }
        }
        
        return impact_analysis.get(event_type, {
            "average_impact": 0,
            "message": "No historical data for this event type"
        })
    
    def get_sector_news(self, sector: str, limit: int = 10) -> List[Dict]:
        """
        Get news for a specific sector
        """
        return self.get_latest_news(limit=limit, category=sector)
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of custom text
        """
        result = self._analyze_sentiment(text)
        
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "sentiment": result["sentiment"],
            "sentiment_score": result["score"],
            "positive_words_found": result.get("positive_words", []),
            "negative_words_found": result.get("negative_words", [])
        }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Simple rule-based sentiment analysis
        For production, use ML model like FinBERT
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        positive_found = words.intersection(self.positive_words)
        negative_found = words.intersection(self.negative_words)
        
        pos_count = len(positive_found)
        neg_count = len(negative_found)
        
        if pos_count > neg_count:
            sentiment = "positive"
            score = min((pos_count - neg_count) / 5, 1.0)
        elif neg_count > pos_count:
            sentiment = "negative"
            score = max((pos_count - neg_count) / 5, -1.0)
        else:
            sentiment = "neutral"
            score = 0
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "positive_words": list(positive_found),
            "negative_words": list(negative_found)
        }
    
    def _classify_event(self, text: str) -> Optional[str]:
        """
        Classify news into event type
        """
        text_lower = text.lower()
        
        for event_type, keywords in self.event_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return event_type
        
        return None
    
    def _extract_source(self, title: str) -> str:
        """
        Extract news source from Google News title
        Google News format: "Title - Source"
        """
        if " - " in title:
            return title.split(" - ")[-1]
        return "Unknown"
