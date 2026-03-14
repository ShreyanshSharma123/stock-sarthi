"""
Sentiment Analyzer - Advanced sentiment analysis for financial news
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SentimentResult:
    """Data class for sentiment analysis results"""
    sentiment: str  # "positive", "negative", "neutral"
    score: float    # -1 to 1
    confidence: float
    aspects: Dict[str, str]


class SentimentAnalyzer:
    """
    Sentiment analyzer for financial text
    
    Methods:
    1. Rule-based (using financial lexicon)
    2. ML-based (using pre-trained models like FinBERT)
    """
    
    def __init__(self, method: str = "lexicon"):
        """
        Initialize sentiment analyzer
        
        Parameters:
            method: "lexicon" for rule-based, "finbert" for ML-based
        """
        self.method = method
        self._init_lexicons()
        
        if method == "finbert":
            self._init_finbert()
    
    def _init_lexicons(self):
        """
        Initialize financial sentiment lexicons
        """
        # Positive financial words
        self.positive_words = {
            # Performance
            'profit', 'growth', 'gains', 'surge', 'rally', 'rise', 'boost',
            'outperform', 'beat', 'exceed', 'record', 'strong', 'robust',
            
            # Momentum
            'bullish', 'uptrend', 'breakout', 'momentum', 'upgrade',
            
            # Business
            'acquisition', 'expansion', 'partnership', 'innovation',
            'dividend', 'buyback', 'launch', 'breakthrough',
            
            # Market
            'optimism', 'confidence', 'recovery', 'rebound', 'boom',
            
            # Ratings
            'buy', 'overweight', 'accumulate', 'positive', 'recommend'
        }
        
        # Negative financial words
        self.negative_words = {
            # Performance
            'loss', 'decline', 'drop', 'fall', 'crash', 'slump', 'plunge',
            'underperform', 'miss', 'weak', 'disappointing', 'poor',
            
            # Momentum
            'bearish', 'downtrend', 'breakdown', 'correction', 'downgrade',
            
            # Risk
            'risk', 'volatility', 'uncertainty', 'concern', 'fear', 'panic',
            'warning', 'crisis', 'recession', 'default', 'bankruptcy',
            
            # Issues
            'scandal', 'lawsuit', 'investigation', 'fraud', 'probe',
            
            # Ratings
            'sell', 'underweight', 'reduce', 'negative', 'avoid'
        }
        
        # Intensifiers (multiply sentiment score)
        self.intensifiers = {
            'very': 1.5, 'highly': 1.5, 'extremely': 2.0, 'significantly': 1.5,
            'major': 1.5, 'massive': 2.0, 'huge': 2.0, 'sharp': 1.5,
            'strong': 1.3, 'robust': 1.3
        }
        
        # Negators (flip sentiment)
        self.negators = {
            'not', 'no', 'never', 'neither', 'without', 'despite', 'fails', 'failed'
        }
        
        # Sector-specific terms
        self.sector_terms = {
            'banking': ['npa', 'credit growth', 'nii', 'nim', 'deposits'],
            'it': ['deal wins', 'attrition', 'digital', 'cloud', 'ai'],
            'pharma': ['fda', 'approval', 'patent', 'drug', 'clinical'],
            'auto': ['sales', 'ev', 'bookings', 'market share', 'production']
        }
    
    def _init_finbert(self):
        """
        Initialize FinBERT model for ML-based sentiment
        """
        try:
            from transformers import pipeline
            
            self.finbert = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert"
            )
            print("✅ FinBERT model loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load FinBERT: {e}")
            print("Falling back to lexicon-based method")
            self.method = "lexicon"
            self.finbert = None
    
    def analyze(self, text: str) -> SentimentResult:
        """
        Analyze sentiment of text
        
        Parameters:
            text: Text to analyze
            
        Returns:
            SentimentResult with sentiment, score, confidence, and aspects
        """
        if self.method == "finbert" and hasattr(self, 'finbert') and self.finbert:
            return self._analyze_finbert(text)
        else:
            return self._analyze_lexicon(text)
    
    def _analyze_lexicon(self, text: str) -> SentimentResult:
        """
        Lexicon-based sentiment analysis
        """
        # Preprocess text
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Initialize scores
        positive_score = 0
        negative_score = 0
        
        # Track found words for aspects
        positive_found = []
        negative_found = []
        
        # Check for negation context
        negation_active = False
        
        for i, word in enumerate(words):
            # Check for negators
            if word in self.negators:
                negation_active = True
                continue
            
            # Check for intensifiers
            multiplier = self.intensifiers.get(words[i-1], 1.0) if i > 0 else 1.0
            
            # Score positive words
            if word in self.positive_words:
                if negation_active:
                    negative_score += 1 * multiplier
                    negative_found.append(word)
                else:
                    positive_score += 1 * multiplier
                    positive_found.append(word)
                negation_active = False
            
            # Score negative words
            elif word in self.negative_words:
                if negation_active:
                    positive_score += 1 * multiplier
                    positive_found.append(word)
                else:
                    negative_score += 1 * multiplier
                    negative_found.append(word)
                negation_active = False
        
        # Calculate final score (-1 to 1)
        total_signals = positive_score + negative_score
        
        if total_signals == 0:
            raw_score = 0
            sentiment = "neutral"
            confidence = 0.5
        else:
            raw_score = (positive_score - negative_score) / total_signals
            
            if raw_score > 0.1:
                sentiment = "positive"
            elif raw_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Confidence based on number of signals
            confidence = min(0.5 + (total_signals * 0.05), 0.95)
        
        return SentimentResult(
            sentiment=sentiment,
            score=round(raw_score, 2),
            confidence=round(confidence, 2),
            aspects={
                "positive_keywords": ", ".join(positive_found[:5]),
                "negative_keywords": ", ".join(negative_found[:5]),
                "method": "lexicon"
            }
        )
    
    def _analyze_finbert(self, text: str) -> SentimentResult:
        """
        FinBERT-based sentiment analysis
        """
        try:
            # Truncate text if too long
            if len(text) > 512:
                text = text[:512]
            
            result = self.finbert(text)[0]
            
            label = result['label'].lower()
            score_value = result['score']
            
            # Map to standard format
            if label == 'positive':
                sentiment = "positive"
                score = score_value
            elif label == 'negative':
                sentiment = "negative"
                score = -score_value
            else:
                sentiment = "neutral"
                score = 0
            
            return SentimentResult(
                sentiment=sentiment,
                score=round(score, 2),
                confidence=round(score_value, 2),
                aspects={"method": "finbert", "raw_label": label}
            )
            
        except Exception as e:
            # Fallback to lexicon
            print(f"FinBERT error: {e}, falling back to lexicon")
            return self._analyze_lexicon(text)
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """
        Analyze sentiment for multiple texts
        """
        return [self.analyze(text) for text in texts]
    
    def analyze_news_article(self, title: str, content: Optional[str] = None) -> Dict:
        """
        Analyze a news article with title and optional content
        
        Gives more weight to title for headlines
        """
        title_result = self.analyze(title)
        
        if content:
            content_result = self.analyze(content)
            
            # Weighted average (title has higher weight)
            combined_score = (title_result.score * 0.6) + (content_result.score * 0.4)
            combined_confidence = (title_result.confidence * 0.6) + (content_result.confidence * 0.4)
            
            if combined_score > 0.1:
                combined_sentiment = "positive"
            elif combined_score < -0.1:
                combined_sentiment = "negative"
            else:
                combined_sentiment = "neutral"
            
            return {
                "sentiment": combined_sentiment,
                "score": round(combined_score, 2),
                "confidence": round(combined_confidence, 2),
                "title_sentiment": title_result.sentiment,
                "content_sentiment": content_result.sentiment
            }
        else:
            return {
                "sentiment": title_result.sentiment,
                "score": title_result.score,
                "confidence": title_result.confidence
            }
    
    def get_aggregate_sentiment(self, results: List[SentimentResult]) -> Dict:
        """
        Get aggregate sentiment from multiple results
        """
        if not results:
            return {"sentiment": "neutral", "score": 0, "confidence": 0}
        
        total_score = sum(r.score for r in results)
        avg_score = total_score / len(results)
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for r in results:
            sentiment_counts[r.sentiment] += 1
        
        if avg_score > 0.1:
            overall_sentiment = "positive"
        elif avg_score < -0.1:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        return {
            "overall_sentiment": overall_sentiment,
            "average_score": round(avg_score, 2),
            "average_confidence": round(avg_confidence, 2),
            "breakdown": sentiment_counts,
            "total_analyzed": len(results)
        }
    
    def extract_event_impact(self, text: str) -> Dict:
        """
        Extract potential market impact from text
        """
        text_lower = text.lower()
        
        # High impact indicators
        high_impact_words = ['crash', 'surge', 'plunge', 'soar', 'collapse', 
                            'breakthrough', 'crisis', 'record', 'historic']
        
        # Medium impact indicators
        medium_impact_words = ['rise', 'fall', 'increase', 'decrease', 'beat', 'miss']
        
        high_count = sum(1 for word in high_impact_words if word in text_lower)
        medium_count = sum(1 for word in medium_impact_words if word in text_lower)
        
        if high_count > 0:
            impact_level = "high"
            impact_score = min(0.5 + (high_count * 0.2), 1.0)
        elif medium_count > 0:
            impact_level = "medium"
            impact_score = min(0.3 + (medium_count * 0.1), 0.7)
        else:
            impact_level = "low"
            impact_score = 0.2
        
        return {
            "impact_level": impact_level,
            "impact_score": round(impact_score, 2),
            "high_impact_keywords": [w for w in high_impact_words if w in text_lower],
            "medium_impact_keywords": [w for w in medium_impact_words if w in text_lower]
        }


# Example usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer(method="lexicon")
    
    test_texts = [
        "Reliance Industries posts record profit, shares surge 5%",
        "Market crashes amid recession fears, investors panic",
        "TCS reports mixed results, IT sector shows uncertainty",
        "Government announces major infrastructure boost, banking stocks rally"
    ]
    
    print("Testing Sentiment Analyzer...")
    print("-" * 50)
    
    for text in test_texts:
        result = analyzer.analyze(text)
        impact = analyzer.extract_event_impact(text)
        
        print(f"\nText: {text[:50]}...")
        print(f"Sentiment: {result.sentiment} (score: {result.score})")
        print(f"Impact: {impact['impact_level']} (score: {impact['impact_score']})")
