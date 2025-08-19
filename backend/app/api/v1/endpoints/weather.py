from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db, WeatherData
from loguru import logger

router = APIRouter()

class WeatherDataCreate(BaseModel):
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    weather_condition: str
    date: datetime

class WeatherDataResponse(BaseModel):
    id: str
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    weather_condition: str
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/data", response_model=WeatherDataResponse)
async def create_weather_data(weather_data: WeatherDataCreate, db: Session = Depends(get_db)):
    """Create a new weather data entry"""
    try:
        new_weather = WeatherData(
            location=weather_data.location,
            temperature=weather_data.temperature,
            humidity=weather_data.humidity,
            wind_speed=weather_data.wind_speed,
            precipitation=weather_data.precipitation,
            weather_condition=weather_data.weather_condition,
            date=weather_data.date
        )
        
        db.add(new_weather)
        db.commit()
        db.refresh(new_weather)
        
        logger.info(f"✅ New weather data created for {new_weather.location}")
        return new_weather
        
    except Exception as e:
        logger.error(f"❌ Error creating weather data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating weather data"
        )

@router.get("/data", response_model=List[WeatherDataResponse])
async def get_weather_data(
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get weather data with optional location filter"""
    try:
        query = db.query(WeatherData)
        
        if location:
            query = query.filter(WeatherData.location.ilike(f"%{location}%"))
        
        weather_data = query.order_by(WeatherData.date.desc()).offset(skip).limit(limit).all()
        return weather_data
        
    except Exception as e:
        logger.error(f"❌ Error fetching weather data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching weather data"
        )

@router.get("/data/{location}", response_model=List[WeatherDataResponse])
async def get_weather_by_location(location: str, db: Session = Depends(get_db)):
    """Get weather data for a specific location"""
    try:
        weather_data = db.query(WeatherData).filter(
            WeatherData.location.ilike(f"%{location}%")
        ).order_by(WeatherData.date.desc()).all()
        return weather_data
        
    except Exception as e:
        logger.error(f"❌ Error fetching weather for {location}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching weather data"
        )

@router.get("/current/{location}")
async def get_current_weather(location: str, db: Session = Depends(get_db)):
    """Get current weather for a location"""
    try:
        current_weather = db.query(WeatherData).filter(
            WeatherData.location.ilike(f"%{location}%")
        ).order_by(WeatherData.date.desc()).first()
        
        if not current_weather:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No weather data found for {location}"
            )
        
        return current_weather
        
    except Exception as e:
        logger.error(f"❌ Error fetching current weather for {location}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching current weather"
        )

@router.get("/forecast/{location}")
async def get_weather_forecast(location: str, days: int = 7, db: Session = Depends(get_db)):
    """Get weather forecast for a location (mock implementation)"""
    try:
        # This is a mock implementation - in real scenario, you'd integrate with a weather API
        from datetime import timedelta
        import random
        
        forecast = []
        base_temp = 25.0  # Base temperature
        base_humidity = 60.0  # Base humidity
        
        for i in range(days):
            # Generate mock forecast data
            temp_variation = random.uniform(-5, 5)
            humidity_variation = random.uniform(-10, 10)
            
            forecast.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temperature": round(base_temp + temp_variation, 1),
                "humidity": round(max(0, min(100, base_humidity + humidity_variation)), 1),
                "wind_speed": round(random.uniform(5, 20), 1),
                "precipitation": round(random.uniform(0, 10), 1),
                "weather_condition": random.choice([
                    "Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain"
                ])
            })
        
        return {
            "location": location,
            "forecast_days": days,
            "forecast": forecast,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating forecast for {location}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating weather forecast"
        )

@router.get("/alerts/{location}")
async def get_weather_alerts(location: str, db: Session = Depends(get_db)):
    """Get weather alerts for a location"""
    try:
        # Get current weather
        current_weather = db.query(WeatherData).filter(
            WeatherData.location.ilike(f"%{location}%")
        ).order_by(WeatherData.date.desc()).first()
        
        alerts = []
        
        if current_weather:
            # Check for extreme conditions
            if current_weather.temperature > 40:
                alerts.append({
                    "type": "heat_warning",
                    "severity": "high",
                    "message": f"Extreme heat warning: Temperature is {current_weather.temperature}°C",
                    "recommendation": "Avoid outdoor activities during peak hours"
                })
            elif current_weather.temperature < 5:
                alerts.append({
                    "type": "cold_warning",
                    "severity": "medium",
                    "message": f"Cold weather alert: Temperature is {current_weather.temperature}°C",
                    "recommendation": "Protect crops from frost damage"
                })
            
            if current_weather.precipitation > 50:
                alerts.append({
                    "type": "heavy_rain",
                    "severity": "high",
                    "message": f"Heavy rainfall alert: {current_weather.precipitation}mm",
                    "recommendation": "Ensure proper drainage and avoid field work"
                })
            
            if current_weather.wind_speed > 30:
                alerts.append({
                    "type": "strong_wind",
                    "severity": "medium",
                    "message": f"Strong wind alert: {current_weather.wind_speed} km/h",
                    "recommendation": "Secure loose objects and avoid spraying operations"
                })
        
        # Add seasonal alerts
        current_month = datetime.now().month
        if current_month in [6, 7, 8, 9]:  # Monsoon season
            alerts.append({
                "type": "monsoon_alert",
                "severity": "low",
                "message": "Monsoon season is active",
                "recommendation": "Plan irrigation accordingly and monitor for waterlogging"
            })
        elif current_month in [3, 4, 5]:  # Summer
            alerts.append({
                "type": "summer_alert",
                "severity": "low",
                "message": "Summer season - high evaporation expected",
                "recommendation": "Increase irrigation frequency and use mulching"
            })
        
        return {
            "location": location,
            "alerts": alerts,
            "total_alerts": len(alerts),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating alerts for {location}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating weather alerts"
        )

@router.get("/agricultural-advice/{location}")
async def get_agricultural_weather_advice(location: str, db: Session = Depends(get_db)):
    """Get agricultural advice based on weather conditions"""
    try:
        current_weather = db.query(WeatherData).filter(
            WeatherData.location.ilike(f"%{location}%")
        ).order_by(WeatherData.date.desc()).first()
        
        if not current_weather:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No weather data found for {location}"
            )
        
        advice = []
        
        # Temperature-based advice
        if current_weather.temperature > 35:
            advice.append({
                "category": "irrigation",
                "priority": "high",
                "advice": "Increase irrigation frequency due to high temperature",
                "details": "High temperatures increase water loss through evaporation"
            })
        elif current_weather.temperature < 10:
            advice.append({
                "category": "crop_protection",
                "priority": "medium",
                "advice": "Protect sensitive crops from cold stress",
                "details": "Consider using row covers or temporary shelters"
            })
        
        # Humidity-based advice
        if current_weather.humidity > 80:
            advice.append({
                "category": "disease_management",
                "priority": "high",
                "advice": "High humidity increases disease risk",
                "details": "Monitor for fungal diseases and consider preventive sprays"
            })
        
        # Precipitation-based advice
        if current_weather.precipitation > 20:
            advice.append({
                "category": "field_operations",
                "priority": "medium",
                "advice": "Avoid field operations during wet conditions",
                "details": "Wet soil can lead to compaction and poor seed germination"
            })
        
        # Wind-based advice
        if current_weather.wind_speed > 20:
            advice.append({
                "category": "spraying",
                "priority": "high",
                "advice": "Avoid pesticide spraying in windy conditions",
                "details": "Wind can cause spray drift and reduce effectiveness"
            })
        
        return {
            "location": location,
            "current_weather": {
                "temperature": current_weather.temperature,
                "humidity": current_weather.humidity,
                "wind_speed": current_weather.wind_speed,
                "precipitation": current_weather.precipitation,
                "condition": current_weather.weather_condition
            },
            "advice": advice,
            "total_advice": len(advice),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating agricultural advice for {location}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating agricultural advice"
        )
