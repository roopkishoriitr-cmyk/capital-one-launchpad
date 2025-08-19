from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db, Crop, User
from loguru import logger

router = APIRouter()

class CropCreate(BaseModel):
    user_id: str
    crop_name: str
    variety: Optional[str] = None
    area: float
    sowing_date: datetime
    expected_harvest_date: datetime
    expected_yield: float
    current_stage: str = "sowing"

class CropResponse(BaseModel):
    id: str
    user_id: str
    crop_name: str
    variety: Optional[str]
    area: float
    sowing_date: datetime
    expected_harvest_date: datetime
    expected_yield: float
    current_stage: str
    created_at: datetime

    class Config:
        from_attributes = True

class CropUpdate(BaseModel):
    crop_name: Optional[str] = None
    variety: Optional[str] = None
    area: Optional[float] = None
    sowing_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    expected_yield: Optional[float] = None
    current_stage: Optional[str] = None

@router.post("/", response_model=CropResponse)
async def create_crop(crop_data: CropCreate, db: Session = Depends(get_db)):
    """Create a new crop entry"""
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == crop_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        new_crop = Crop(
            user_id=crop_data.user_id,
            crop_name=crop_data.crop_name,
            variety=crop_data.variety,
            area=crop_data.area,
            sowing_date=crop_data.sowing_date,
            expected_harvest_date=crop_data.expected_harvest_date,
            expected_yield=crop_data.expected_yield,
            current_stage=crop_data.current_stage
        )
        
        db.add(new_crop)
        db.commit()
        db.refresh(new_crop)
        
        logger.info(f"✅ New crop created: {new_crop.crop_name} for user {crop_data.user_id}")
        return new_crop
        
    except Exception as e:
        logger.error(f"❌ Error creating crop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating crop"
        )

@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: str, db: Session = Depends(get_db)):
    """Get crop by ID"""
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found"
            )
        return crop
        
    except Exception as e:
        logger.error(f"❌ Error fetching crop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching crop"
        )

@router.get("/user/{user_id}", response_model=List[CropResponse])
async def get_user_crops(user_id: str, db: Session = Depends(get_db)):
    """Get all crops for a user"""
    try:
        crops = db.query(Crop).filter(Crop.user_id == user_id).all()
        return crops
        
    except Exception as e:
        logger.error(f"❌ Error fetching user crops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user crops"
        )

@router.put("/{crop_id}", response_model=CropResponse)
async def update_crop(crop_id: str, crop_data: CropUpdate, db: Session = Depends(get_db)):
    """Update crop information"""
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found"
            )
        
        # Update only provided fields
        update_data = crop_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(crop, field, value)
        
        db.commit()
        db.refresh(crop)
        
        logger.info(f"✅ Crop updated: {crop_id}")
        return crop
        
    except Exception as e:
        logger.error(f"❌ Error updating crop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating crop"
        )

@router.delete("/{crop_id}")
async def delete_crop(crop_id: str, db: Session = Depends(get_db)):
    """Delete a crop"""
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found"
            )
        
        db.delete(crop)
        db.commit()
        
        logger.info(f"✅ Crop deleted: {crop_id}")
        return {"message": "Crop deleted successfully"}
        
    except Exception as e:
        logger.error(f"❌ Error deleting crop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting crop"
        )

@router.get("/", response_model=List[CropResponse])
async def get_all_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all crops with pagination"""
    try:
        crops = db.query(Crop).offset(skip).limit(limit).all()
        return crops
        
    except Exception as e:
        logger.error(f"❌ Error fetching crops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching crops"
        )

@router.get("/stage/{stage}", response_model=List[CropResponse])
async def get_crops_by_stage(stage: str, db: Session = Depends(get_db)):
    """Get crops by current stage"""
    try:
        crops = db.query(Crop).filter(Crop.current_stage == stage).all()
        return crops
        
    except Exception as e:
        logger.error(f"❌ Error fetching crops by stage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching crops by stage"
        )

@router.get("/name/{crop_name}", response_model=List[CropResponse])
async def get_crops_by_name(crop_name: str, db: Session = Depends(get_db)):
    """Get crops by name"""
    try:
        crops = db.query(Crop).filter(Crop.crop_name.ilike(f"%{crop_name}%")).all()
        return crops
        
    except Exception as e:
        logger.error(f"❌ Error fetching crops by name: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching crops by name"
        )
