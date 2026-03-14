"""
Watchlist Routes - API endpoints for managing user watchlists
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.models import get_db, Watchlist, User
from api.routes.users import get_current_user
from services.stock_service import StockService

router = APIRouter()


@router.get("/")
async def get_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's watchlist with live prices
    """
    watchlist = db.query(Watchlist)\
        .filter(Watchlist.user_id == current_user.id)\
        .all()
    
    if not watchlist:
        return {"message": "Watchlist is empty", "stocks": []}
    
    # Get live prices for each stock
    stock_service = StockService()
    result = []
    
    for item in watchlist:
        try:
            live_data = stock_service.get_live_price(item.symbol)
            result.append({
                "id": item.id,
                "symbol": item.symbol,
                "target_price": item.target_price,
                "notes": item.notes,
                "added_at": item.created_at,
                "live_price": live_data.get("price"),
                "change_percent": live_data.get("change_percent")
            })
        except Exception:
            result.append({
                "id": item.id,
                "symbol": item.symbol,
                "target_price": item.target_price,
                "notes": item.notes,
                "added_at": item.created_at,
                "live_price": None,
                "change_percent": None
            })
    
    return {"stocks": result}


@router.post("/add")
async def add_to_watchlist(
    symbol: str,
    target_price: Optional[float] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a stock to watchlist
    """
    # Check if already in watchlist
    existing = db.query(Watchlist)\
        .filter(
            Watchlist.user_id == current_user.id,
            Watchlist.symbol == symbol
        )\
        .first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Stock already in watchlist"
        )
    
    # Add to watchlist
    new_item = Watchlist(
        user_id=current_user.id,
        symbol=symbol,
        target_price=target_price,
        notes=notes
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "message": f"{symbol} added to watchlist",
        "item": {
            "id": new_item.id,
            "symbol": new_item.symbol,
            "target_price": new_item.target_price
        }
    }


@router.delete("/remove/{symbol}")
async def remove_from_watchlist(
    symbol: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a stock from watchlist
    """
    item = db.query(Watchlist)\
        .filter(
            Watchlist.user_id == current_user.id,
            Watchlist.symbol == symbol
        )\
        .first()
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Stock not in watchlist"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": f"{symbol} removed from watchlist"}


@router.put("/update/{symbol}")
async def update_watchlist_item(
    symbol: str,
    target_price: Optional[float] = None,
    notes: Optional[str] = None,
    alert_on_price: Optional[bool] = None,
    alert_on_news: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update watchlist item settings
    """
    item = db.query(Watchlist)\
        .filter(
            Watchlist.user_id == current_user.id,
            Watchlist.symbol == symbol
        )\
        .first()
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Stock not in watchlist"
        )
    
    if target_price is not None:
        item.target_price = target_price
    if notes is not None:
        item.notes = notes
    if alert_on_price is not None:
        item.alert_on_price = alert_on_price
    if alert_on_news is not None:
        item.alert_on_news = alert_on_news
    
    db.commit()
    db.refresh(item)
    
    return {"message": "Watchlist item updated", "item": item}


@router.get("/alerts")
async def get_watchlist_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check for any triggered alerts (price targets reached)
    """
    watchlist = db.query(Watchlist)\
        .filter(
            Watchlist.user_id == current_user.id,
            Watchlist.target_price.isnot(None),
            Watchlist.alert_on_price == True
        )\
        .all()
    
    if not watchlist:
        return {"alerts": []}
    
    stock_service = StockService()
    alerts = []
    
    for item in watchlist:
        try:
            live_data = stock_service.get_live_price(item.symbol)
            current_price = live_data.get("price")
            
            if current_price and item.target_price:
                # Check if target reached
                if current_price >= item.target_price:
                    alerts.append({
                        "symbol": item.symbol,
                        "type": "target_reached",
                        "target_price": item.target_price,
                        "current_price": current_price,
                        "message": f"{item.symbol} has reached your target price of ₹{item.target_price}"
                    })
        except Exception:
            continue
    
    return {"alerts": alerts}
