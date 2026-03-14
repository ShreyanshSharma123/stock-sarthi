"""
Stock Routes - API endpoints for stock data
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.models import get_db, Stock, StockData
from services.stock_service import StockService
from schemas.stock_schemas import (
    StockResponse, 
    StockDataResponse, 
    StockListResponse,
    StockSearchResponse
)

router = APIRouter()


# List of popular Indian stocks (pre-configured)
POPULAR_STOCKS = [
    {"symbol": "RELIANCE.NS", "name": "Reliance Industries Limited", "sector": "Energy"},
    {"symbol": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT"},
    {"symbol": "INFY.NS", "name": "Infosys Limited", "sector": "IT"},
    {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited", "sector": "Banking"},
    {"symbol": "ICICIBANK.NS", "name": "ICICI Bank Limited", "sector": "Banking"},
    {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Banking"},
    {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel Limited", "sector": "Telecom"},
    {"symbol": "ITC.NS", "name": "ITC Limited", "sector": "FMCG"},
    {"symbol": "WIPRO.NS", "name": "Wipro Limited", "sector": "IT"},
    {"symbol": "TATAMOTORS.NS", "name": "Tata Motors Limited", "sector": "Auto"},
    {"symbol": "MARUTI.NS", "name": "Maruti Suzuki India", "sector": "Auto"},
    {"symbol": "HCLTECH.NS", "name": "HCL Technologies", "sector": "IT"},
    {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical", "sector": "Pharma"},
    {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance", "sector": "Finance"},
    {"symbol": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure"},
]


@router.get("/", response_model=List[dict])
def get_all_stocks():
    """
    Get list of all available stocks for selection
    """
    return POPULAR_STOCKS


@router.get("/search")
def search_stocks(
    query: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Search for stocks by name or symbol
    """
    query = query.upper()
    results = []
    
    for stock in POPULAR_STOCKS:
        if query in stock["symbol"].upper() or query in stock["name"].upper():
            results.append(stock)
        if len(results) >= limit:
            break
    
    return results


@router.get("/{symbol}")
def get_stock_details(symbol: str):
    """
    Get detailed information about a specific stock
    """
    stock_service = StockService()
    
    try:
        stock_info = stock_service.get_stock_info(symbol)
        return stock_info
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Stock not found: {str(e)}")


@router.get("/{symbol}/history")
def get_stock_history(
    symbol: str,
    period: str = Query("1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y"),
    interval: str = Query("1d", description="Interval: 1m, 5m, 15m, 1h, 1d, 1wk, 1mo")
):
    """
    Get historical price data for a stock
    
    Parameters:
    - symbol: Stock symbol (e.g., RELIANCE.NS)
    - period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
    - interval: Data interval (1m, 5m, 15m, 1h, 1d, 1wk, 1mo)
    """
    stock_service = StockService()
    
    try:
        history = stock_service.get_historical_data(symbol, period, interval)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@router.get("/{symbol}/live")
def get_live_price(symbol: str):
    """
    Get current live price for a stock
    """
    stock_service = StockService()
    
    try:
        live_data = stock_service.get_live_price(symbol)
        return live_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live data: {str(e)}")


@router.get("/{symbol}/indicators")
def get_technical_indicators(
    symbol: str,
    period: str = Query("3mo", description="Period for calculation")
):
    """
    Get technical indicators for a stock
    
    Returns: SMA, EMA, RSI, MACD, Bollinger Bands
    """
    stock_service = StockService()
    
    try:
        indicators = stock_service.calculate_indicators(symbol, period)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating indicators: {str(e)}")


@router.get("/market/overview")
def get_market_overview():
    """
    Get overall market overview (Nifty 50, Sensex, top movers)
    """
    stock_service = StockService()
    
    try:
        overview = stock_service.get_market_overview()
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market overview: {str(e)}")


@router.get("/sectors/performance")
def get_sector_performance():
    """
    Get sector-wise performance
    """
    stock_service = StockService()
    
    try:
        performance = stock_service.get_sector_performance()
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sector data: {str(e)}")
