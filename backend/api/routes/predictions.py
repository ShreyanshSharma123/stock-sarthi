"""
Prediction Routes - API endpoints for AI predictions
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.models import get_db, Prediction
from services.prediction_service import PredictionService
from ml.predictor import StockPredictor

router = APIRouter()


@router.get("/{symbol}")
def get_prediction(
    symbol: str,
    days: int = Query(7, ge=1, le=30, description="Days to predict ahead")
):
    """
    Get AI prediction for a specific stock
    
    Returns:
    - predicted_price: Expected price
    - signal: BUY / HOLD / SELL
    - confidence: Confidence score (0-1)
    - explanation: Why this prediction
    """
    prediction_service = PredictionService()
    
    try:
        prediction = prediction_service.get_prediction(symbol, days)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.get("/{symbol}/detailed")
def get_detailed_prediction(symbol: str):
    """
    Get detailed prediction with all factors
    
    Returns comprehensive analysis including:
    - Technical analysis score
    - Sentiment score from news
    - Event impact score
    - Historical accuracy
    - Supporting factors
    """
    prediction_service = PredictionService()
    
    try:
        detailed = prediction_service.get_detailed_prediction(symbol)
        return detailed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/{symbol}/factors")
def get_prediction_factors(symbol: str):
    """
    Get breakdown of factors affecting the prediction
    
    Shows:
    - Technical indicators contribution
    - News sentiment contribution
    - Event impact contribution
    - Pattern recognition results
    """
    prediction_service = PredictionService()
    
    try:
        factors = prediction_service.get_prediction_factors(symbol)
        return factors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/")
def get_all_predictions(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recent predictions for all stocks
    """
    predictions = db.query(Prediction)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    return predictions


@router.get("/accuracy/{symbol}")
def get_prediction_accuracy(
    symbol: str,
    days: int = Query(30, description="Days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get historical accuracy of predictions for a stock
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    predictions = db.query(Prediction)\
        .filter(
            Prediction.symbol == symbol,
            Prediction.created_at >= cutoff_date,
            Prediction.was_correct.isnot(None)
        )\
        .all()
    
    if not predictions:
        return {"message": "No historical predictions found", "accuracy": None}
    
    correct = sum(1 for p in predictions if p.was_correct)
    total = len(predictions)
    
    return {
        "symbol": symbol,
        "period_days": days,
        "total_predictions": total,
        "correct_predictions": correct,
        "accuracy": round(correct / total * 100, 2) if total > 0 else 0
    }


@router.post("/{symbol}/generate")
def generate_new_prediction(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Generate a new prediction for a stock (triggers ML model)
    """
    prediction_service = PredictionService()
    
    try:
        # Generate new prediction
        new_prediction = prediction_service.generate_prediction(symbol)
        
        # Save to database
        db_prediction = Prediction(
            symbol=symbol,
            target_date=new_prediction["target_date"],
            current_price=new_prediction["current_price"],
            predicted_price=new_prediction["predicted_price"],
            price_change_percent=new_prediction["price_change_percent"],
            signal=new_prediction["signal"],
            confidence=new_prediction["confidence"],
            model_name=new_prediction["model_name"],
            technical_score=new_prediction.get("technical_score"),
            sentiment_score=new_prediction.get("sentiment_score"),
            explanation=new_prediction.get("explanation")
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return new_prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating prediction: {str(e)}")


@router.get("/signals/today")
def get_todays_signals():
    """
    Get today's buy/sell signals across all stocks
    """
    prediction_service = PredictionService()
    
    try:
        signals = prediction_service.get_daily_signals()
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
