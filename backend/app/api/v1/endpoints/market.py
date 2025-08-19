from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db, MarketPrice
from loguru import logger

router = APIRouter()

class MarketPriceCreate(BaseModel):
    crop_name: str
    mandi_name: str
    state: str
    min_price: float
    max_price: float
    modal_price: float
    date: datetime

class MarketPriceResponse(BaseModel):
    id: str
    crop_name: str
    mandi_name: str
    state: str
    min_price: float
    max_price: float
    modal_price: float
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/prices", response_model=MarketPriceResponse)
async def create_market_price(price_data: MarketPriceCreate, db: Session = Depends(get_db)):
    """Create a new market price entry"""
    try:
        new_price = MarketPrice(
            crop_name=price_data.crop_name,
            mandi_name=price_data.mandi_name,
            state=price_data.state,
            min_price=price_data.min_price,
            max_price=price_data.max_price,
            modal_price=price_data.modal_price,
            date=price_data.date
        )
        
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        
        logger.info(f"✅ New market price created: {new_price.crop_name} at {new_price.mandi_name}")
        return new_price
        
    except Exception as e:
        logger.error(f"❌ Error creating market price: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating market price"
        )

@router.get("/prices", response_model=List[MarketPriceResponse])
async def get_market_prices(
    crop_name: Optional[str] = None,
    mandi_name: Optional[str] = None,
    state: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get market prices with optional filters"""
    try:
        query = db.query(MarketPrice)
        
        if crop_name:
            query = query.filter(MarketPrice.crop_name.ilike(f"%{crop_name}%"))
        if mandi_name:
            query = query.filter(MarketPrice.mandi_name.ilike(f"%{mandi_name}%"))
        if state:
            query = query.filter(MarketPrice.state.ilike(f"%{state}%"))
        
        prices = query.offset(skip).limit(limit).all()
        return prices
        
    except Exception as e:
        logger.error(f"❌ Error fetching market prices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching market prices"
        )

@router.get("/prices/{crop_name}", response_model=List[MarketPriceResponse])
async def get_prices_by_crop(crop_name: str, db: Session = Depends(get_db)):
    """Get market prices for a specific crop"""
    try:
        prices = db.query(MarketPrice).filter(
            MarketPrice.crop_name.ilike(f"%{crop_name}%")
        ).all()
        return prices
        
    except Exception as e:
        logger.error(f"❌ Error fetching prices for crop {crop_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching crop prices"
        )

@router.get("/prices/mandi/{mandi_name}", response_model=List[MarketPriceResponse])
async def get_prices_by_mandi(mandi_name: str, db: Session = Depends(get_db)):
    """Get market prices for a specific mandi"""
    try:
        prices = db.query(MarketPrice).filter(
            MarketPrice.mandi_name.ilike(f"%{mandi_name}%")
        ).all()
        return prices
        
    except Exception as e:
        logger.error(f"❌ Error fetching prices for mandi {mandi_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching mandi prices"
        )

@router.get("/prices/state/{state}", response_model=List[MarketPriceResponse])
async def get_prices_by_state(state: str, db: Session = Depends(get_db)):
    """Get market prices for a specific state"""
    try:
        prices = db.query(MarketPrice).filter(
            MarketPrice.state.ilike(f"%{state}%")
        ).all()
        return prices
        
    except Exception as e:
        logger.error(f"❌ Error fetching prices for state {state}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching state prices"
        )

@router.get("/insights/{crop_name}")
async def get_market_insights(crop_name: str, db: Session = Depends(get_db)):
    """Get market insights for a specific crop"""
    try:
        # Get recent prices for the crop
        recent_prices = db.query(MarketPrice).filter(
            MarketPrice.crop_name.ilike(f"%{crop_name}%")
        ).order_by(MarketPrice.date.desc()).limit(10).all()
        
        if not recent_prices:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No price data found for {crop_name}"
            )
        
        # Calculate insights
        avg_price = sum(price.modal_price for price in recent_prices) / len(recent_prices)
        min_price = min(price.min_price for price in recent_prices)
        max_price = max(price.max_price for price in recent_prices)
        
        # Price trend (simple comparison of latest vs oldest)
        if len(recent_prices) >= 2:
            latest_price = recent_prices[0].modal_price
            oldest_price = recent_prices[-1].modal_price
            price_change = latest_price - oldest_price
            price_change_percent = (price_change / oldest_price) * 100
            trend = "rising" if price_change > 0 else "falling" if price_change < 0 else "stable"
        else:
            trend = "stable"
            price_change_percent = 0
        
        # Top mandis by price
        mandi_prices = {}
        for price in recent_prices:
            if price.mandi_name not in mandi_prices:
                mandi_prices[price.mandi_name] = []
            mandi_prices[price.mandi_name].append(price.modal_price)
        
        top_mandis = sorted(
            [(mandi, sum(prices) / len(prices)) for mandi, prices in mandi_prices.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "crop_name": crop_name,
            "average_price": round(avg_price, 2),
            "price_range": {
                "min": min_price,
                "max": max_price
            },
            "trend": trend,
            "price_change_percent": round(price_change_percent, 2),
            "top_mandis": [
                {"mandi": mandi, "avg_price": round(price, 2)} 
                for mandi, price in top_mandis
            ],
            "data_points": len(recent_prices),
            "last_updated": recent_prices[0].date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating market insights for {crop_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating market insights"
        )

@router.get("/trends")
async def get_market_trends(db: Session = Depends(get_db)):
    """Get overall market trends"""
    try:
        # Get all crops
        crops = db.query(MarketPrice.crop_name).distinct().all()
        crop_names = [crop[0] for crop in crops]
        
        trends = []
        for crop_name in crop_names[:10]:  # Limit to top 10 crops
            try:
                recent_prices = db.query(MarketPrice).filter(
                    MarketPrice.crop_name == crop_name
                ).order_by(MarketPrice.date.desc()).limit(5).all()
                
                if len(recent_prices) >= 2:
                    latest_price = recent_prices[0].modal_price
                    oldest_price = recent_prices[-1].modal_price
                    price_change = latest_price - oldest_price
                    price_change_percent = (price_change / oldest_price) * 100
                    
                    trends.append({
                        "crop_name": crop_name,
                        "current_price": latest_price,
                        "price_change_percent": round(price_change_percent, 2),
                        "trend": "rising" if price_change > 0 else "falling" if price_change < 0 else "stable"
                    })
            except Exception as e:
                logger.warning(f"Could not calculate trend for {crop_name}: {e}")
                continue
        
        # Sort by absolute price change
        trends.sort(key=lambda x: abs(x["price_change_percent"]), reverse=True)
        
        return {
            "total_crops": len(crop_names),
            "trends": trends[:10],  # Return top 10 trends
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating market trends: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating market trends"
        )
