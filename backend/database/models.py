"""
Database Models for Stock Saarthi
Using SQLAlchemy ORM with PostgreSQL
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv()

# Database URL - Change this based on your setup
# For development, you can use SQLite for simplicity
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./stock_saarthi.db"  # SQLite for development
    # "postgresql://username:password@localhost/stock_saarthi"  # PostgreSQL for production
)

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Enums
class SignalType(enum.Enum):
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"


class SentimentType(enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


# ============== USER MODEL ==============
class User(Base):
    """
    User model for storing user information
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    watchlist = relationship("Watchlist", back_populates="user")


# ============== STOCK MODEL ==============
class Stock(Base):
    """
    Stock model for storing stock information
    """
    __tablename__ = "stocks"

    symbol = Column(String(20), primary_key=True, index=True)  # e.g., "RELIANCE.NS"
    name = Column(String(255), nullable=False)  # e.g., "Reliance Industries Limited"
    sector = Column(String(100))  # e.g., "Energy"
    industry = Column(String(100))  # e.g., "Oil & Gas"
    market_cap = Column(Float)  # Market capitalization
    currency = Column(String(10), default="INR")
    exchange = Column(String(20), default="NSE")  # NSE or BSE
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    stock_data = relationship("StockData", back_populates="stock")
    predictions = relationship("Prediction", back_populates="stock")
    news_articles = relationship("NewsArticle", back_populates="stock")


# ============== STOCK DATA MODEL ==============
class StockData(Base):
    """
    Historical and live stock price data
    """
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    
    # OHLCV Data
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    
    # Technical indicators (pre-calculated)
    sma_10 = Column(Float)  # Simple Moving Average (10 days)
    sma_50 = Column(Float)  # Simple Moving Average (50 days)
    ema_10 = Column(Float)  # Exponential Moving Average
    rsi = Column(Float)     # Relative Strength Index
    macd = Column(Float)    # MACD value
    macd_signal = Column(Float)  # MACD signal line
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    stock = relationship("Stock", back_populates="stock_data")


# ============== PREDICTION MODEL ==============
class Prediction(Base):
    """
    AI predictions for stocks
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    
    # Prediction details
    predicted_at = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=False)  # Date for which prediction is made
    
    current_price = Column(Float)
    predicted_price = Column(Float)
    price_change_percent = Column(Float)
    
    signal = Column(String(10))  # "buy", "hold", "sell"
    confidence = Column(Float)  # 0 to 1
    
    # Model information
    model_name = Column(String(50))  # e.g., "SVR", "LSTM"
    model_version = Column(String(20))
    
    # Factors considered
    technical_score = Column(Float)  # Technical analysis score
    sentiment_score = Column(Float)  # News sentiment score
    event_impact_score = Column(Float)  # Event impact score
    
    # Explanation
    explanation = Column(Text)  # Human-readable explanation
    
    # Actual result (filled later for accuracy tracking)
    actual_price = Column(Float)
    was_correct = Column(Boolean)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    stock = relationship("Stock", back_populates="predictions")


# ============== NEWS ARTICLE MODEL ==============
class NewsArticle(Base):
    """
    News articles related to stocks
    """
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"))  # Can be null for general news
    
    title = Column(String(500), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(100))
    url = Column(String(500))
    image_url = Column(String(500))
    
    published_at = Column(DateTime)
    
    # Sentiment analysis
    sentiment = Column(String(20))  # "positive", "neutral", "negative"
    sentiment_score = Column(Float)  # -1 to 1
    
    # Event classification
    event_type = Column(String(50))  # "earnings", "budget", "election", etc.
    event_impact = Column(Float)  # Expected impact -1 to 1
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    stock = relationship("Stock", back_populates="news_articles")


# ============== ECONOMIC EVENT MODEL ==============
class EconomicEvent(Base):
    """
    Major economic events that affect stock markets
    """
    __tablename__ = "economic_events"

    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50))  # "budget", "election", "rbi_policy", etc.
    
    event_date = Column(DateTime, nullable=False)
    
    # Impact prediction
    expected_impact = Column(String(20))  # "positive", "negative", "neutral"
    impact_sectors = Column(Text)  # JSON list of affected sectors
    
    # Actual impact (filled after event)
    actual_impact = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)


# ============== WATCHLIST MODEL ==============
class Watchlist(Base):
    """
    User's watchlist of stocks
    """
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    
    # Alert settings
    target_price = Column(Float)
    alert_on_price = Column(Boolean, default=False)
    alert_on_news = Column(Boolean, default=True)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watchlist")


# ============== DATABASE HELPER FUNCTIONS ==============
def get_db():
    """
    Dependency to get database session
    Use with FastAPI's Depends()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


# Run this file directly to create tables
if __name__ == "__main__":
    init_db()
