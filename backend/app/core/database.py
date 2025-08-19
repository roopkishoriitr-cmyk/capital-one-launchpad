from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from app.core.config import settings
import uuid

# Database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)
    language = Column(String, default="hi")
    state = Column(String)
    district = Column(String)
    village = Column(String)
    land_area = Column(Float)  # in acres
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    loans = relationship("Loan", back_populates="user")
    crops = relationship("Crop", back_populates="user")
    soil_reports = relationship("SoilReport", back_populates="user")

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    loan_type = Column(String)  # crop_loan, equipment_loan, etc.
    amount = Column(Float)
    interest_rate = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    remaining_amount = Column(Float)
    status = Column(String)  # active, paid, defaulted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="loans")

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    crop_name = Column(String)
    variety = Column(String)
    area = Column(Float)  # in acres
    sowing_date = Column(DateTime)
    expected_harvest_date = Column(DateTime)
    expected_yield = Column(Float)  # in quintals
    current_stage = Column(String)  # sowing, growing, harvesting
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="crops")

class SoilReport(Base):
    __tablename__ = "soil_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    ph_level = Column(Float)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    organic_carbon = Column(Float)
    report_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="soil_reports")

class MarketPrice(Base):
    __tablename__ = "market_prices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_name = Column(String)
    mandi_name = Column(String)
    state = Column(String)
    min_price = Column(Float)
    max_price = Column(Float)
    modal_price = Column(Float)
    date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    rainfall = Column(Float)
    wind_speed = Column(Float)
    forecast_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Subsidy(Base):
    __tablename__ = "subsidies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_name = Column(String)
    description = Column(Text)
    eligibility_criteria = Column(Text)
    subsidy_amount = Column(Float)
    state = Column(String)
    category = Column(String)  # crop, equipment, irrigation, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    query = Column(Text)
    response = Column(Text)
    language = Column(String)
    agent_used = Column(String)  # finance, agronomy, market, etc.
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DebtForecast(Base):
    __tablename__ = "debt_forecasts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    current_debt = Column(Float)
    projected_debt_free_date = Column(DateTime)
    monthly_payment_needed = Column(Float)
    recommended_crops = Column(Text)  # JSON string
    risk_factors = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
