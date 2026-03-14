"""
News Routes - API endpoints for financial news and events
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.models import get_db, NewsArticle, EconomicEvent
from services.news_service import NewsService

router = APIRouter()


@router.get("/")
def get_latest_news(
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None, description="Filter by category")
):
    news_service = NewsService()

    try:
        news = news_service.get_latest_news(limit=limit, category=category)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/stock/{symbol}")
def get_stock_news(
    symbol: str,
    limit: int = Query(10, ge=1, le=50)
):
    news_service = NewsService()

    try:
        company_name = symbol.split(".")[0].title()
        news = news_service.get_company_news(company_name, limit=limit)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock news: {str(e)}")


@router.get("/sentiment/{symbol}")
def get_news_sentiment(symbol: str):
    news_service = NewsService()

    try:
        sentiment = news_service.get_sentiment_analysis(symbol)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")


@router.get("/events")
def get_upcoming_events(
    days: int = Query(30, ge=1, le=90, description="Days ahead to look")
):
    news_service = NewsService()

    try:
        events = news_service.get_upcoming_events(days=days)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")


@router.get("/events/{event_id}")
def get_event_details(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EconomicEvent).filter(EconomicEvent.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


# ✅ FIXED ROUTE
@router.get("/events/impact/{event_type}")
def get_event_impact_analysis(
    event_type: str = Path(..., description="Event type: budget, election, rbi_policy, earnings")
):
    news_service = NewsService()

    try:
        impact = news_service.get_historical_event_impact(event_type)
        return impact
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/sectors/{sector}")
def get_sector_news(
    sector: str,
    limit: int = Query(10, ge=1, le=50)
):
    news_service = NewsService()

    try:
        news = news_service.get_sector_news(sector, limit=limit)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/analyze")
def analyze_news_text(
    text: str = Query(..., description="News text to analyze")
):
    news_service = NewsService()

    try:
        analysis = news_service.analyze_text_sentiment(text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")