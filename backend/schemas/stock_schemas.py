"""
Pydantic schemas for Stock-related API requests/responses
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StockBase(BaseModel):
    """Base schema for stock information"""
    symbol: str
    name: str
    sector: Optional[str] = None


class StockResponse(StockBase):
    """Response schema for stock details"""
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    volume: Optional[int] = None
    pe_ratio: Optional[float] = None
    
    class Config:
        from_attributes = True


class StockDataPoint(BaseModel):
    """Single data point in stock history"""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockDataResponse(BaseModel):
    """Response schema for historical data"""
    symbol: str
    period: str
    interval: str
    data_points: int
    data: List[StockDataPoint]


class StockListResponse(BaseModel):
    """Response for list of stocks"""
    stocks: List[StockBase]
    count: int


class StockSearchResponse(BaseModel):
    """Response for stock search"""
    results: List[StockBase]
    query: str


class LivePriceResponse(BaseModel):
    """Response for live price"""
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: Optional[int]
    timestamp: str


class TechnicalIndicatorsResponse(BaseModel):
    """Response for technical indicators"""
    symbol: str
    sma_10: Optional[float]
    sma_20: Optional[float]
    sma_50: Optional[float]
    ema_10: Optional[float]
    ema_20: Optional[float]
    rsi: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    macd_histogram: Optional[float]
    bollinger_upper: Optional[float]
    bollinger_middle: Optional[float]
    bollinger_lower: Optional[float]
    current_price: float
