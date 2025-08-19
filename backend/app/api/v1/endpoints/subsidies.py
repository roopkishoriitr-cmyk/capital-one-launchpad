from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db, Subsidy
from loguru import logger

router = APIRouter()

class SubsidyCreate(BaseModel):
    scheme_name: str
    scheme_type: str
    description: str
    eligibility_criteria: str
    amount: float
    state: str
    application_deadline: Optional[datetime] = None
    contact_info: str

class SubsidyResponse(BaseModel):
    id: str
    scheme_name: str
    scheme_type: str
    description: str
    eligibility_criteria: str
    amount: float
    state: str
    application_deadline: Optional[datetime]
    contact_info: str
    created_at: datetime

    class Config:
        from_attributes = True

class SubsidyUpdate(BaseModel):
    scheme_name: Optional[str] = None
    scheme_type: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    amount: Optional[float] = None
    state: Optional[str] = None
    application_deadline: Optional[datetime] = None
    contact_info: Optional[str] = None

@router.post("/", response_model=SubsidyResponse)
async def create_subsidy(subsidy_data: SubsidyCreate, db: Session = Depends(get_db)):
    """Create a new subsidy scheme"""
    try:
        new_subsidy = Subsidy(
            scheme_name=subsidy_data.scheme_name,
            scheme_type=subsidy_data.scheme_type,
            description=subsidy_data.description,
            eligibility_criteria=subsidy_data.eligibility_criteria,
            amount=subsidy_data.amount,
            state=subsidy_data.state,
            application_deadline=subsidy_data.application_deadline,
            contact_info=subsidy_data.contact_info
        )
        
        db.add(new_subsidy)
        db.commit()
        db.refresh(new_subsidy)
        
        logger.info(f"✅ New subsidy scheme created: {new_subsidy.scheme_name}")
        return new_subsidy
        
    except Exception as e:
        logger.error(f"❌ Error creating subsidy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating subsidy"
        )

@router.get("/", response_model=List[SubsidyResponse])
async def get_subsidies(
    scheme_type: Optional[str] = None,
    state: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get subsidies with optional filters"""
    try:
        query = db.query(Subsidy)
        
        if scheme_type:
            query = query.filter(Subsidy.scheme_type == scheme_type)
        if state:
            query = query.filter(Subsidy.state.ilike(f"%{state}%"))
        
        subsidies = query.offset(skip).limit(limit).all()
        return subsidies
        
    except Exception as e:
        logger.error(f"❌ Error fetching subsidies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching subsidies"
        )

@router.get("/{subsidy_id}", response_model=SubsidyResponse)
async def get_subsidy(subsidy_id: str, db: Session = Depends(get_db)):
    """Get subsidy by ID"""
    try:
        subsidy = db.query(Subsidy).filter(Subsidy.id == subsidy_id).first()
        if not subsidy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsidy not found"
            )
        return subsidy
        
    except Exception as e:
        logger.error(f"❌ Error fetching subsidy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching subsidy"
        )

@router.get("/type/{scheme_type}", response_model=List[SubsidyResponse])
async def get_subsidies_by_type(scheme_type: str, db: Session = Depends(get_db)):
    """Get subsidies by scheme type"""
    try:
        subsidies = db.query(Subsidy).filter(Subsidy.scheme_type == scheme_type).all()
        return subsidies
        
    except Exception as e:
        logger.error(f"❌ Error fetching subsidies by type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching subsidies by type"
        )

@router.get("/state/{state}", response_model=List[SubsidyResponse])
async def get_subsidies_by_state(state: str, db: Session = Depends(get_db)):
    """Get subsidies by state"""
    try:
        subsidies = db.query(Subsidy).filter(Subsidy.state.ilike(f"%{state}%")).all()
        return subsidies
        
    except Exception as e:
        logger.error(f"❌ Error fetching subsidies by state: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching subsidies by state"
        )

@router.put("/{subsidy_id}", response_model=SubsidyResponse)
async def update_subsidy(subsidy_id: str, subsidy_data: SubsidyUpdate, db: Session = Depends(get_db)):
    """Update subsidy information"""
    try:
        subsidy = db.query(Subsidy).filter(Subsidy.id == subsidy_id).first()
        if not subsidy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsidy not found"
            )
        
        # Update only provided fields
        update_data = subsidy_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(subsidy, field, value)
        
        db.commit()
        db.refresh(subsidy)
        
        logger.info(f"✅ Subsidy updated: {subsidy_id}")
        return subsidy
        
    except Exception as e:
        logger.error(f"❌ Error updating subsidy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating subsidy"
        )

@router.delete("/{subsidy_id}")
async def delete_subsidy(subsidy_id: str, db: Session = Depends(get_db)):
    """Delete a subsidy"""
    try:
        subsidy = db.query(Subsidy).filter(Subsidy.id == subsidy_id).first()
        if not subsidy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsidy not found"
            )
        
        db.delete(subsidy)
        db.commit()
        
        logger.info(f"✅ Subsidy deleted: {subsidy_id}")
        return {"message": "Subsidy deleted successfully"}
        
    except Exception as e:
        logger.error(f"❌ Error deleting subsidy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting subsidy"
        )

@router.get("/search/{keyword}", response_model=List[SubsidyResponse])
async def search_subsidies(keyword: str, db: Session = Depends(get_db)):
    """Search subsidies by keyword"""
    try:
        subsidies = db.query(Subsidy).filter(
            (Subsidy.scheme_name.ilike(f"%{keyword}%")) |
            (Subsidy.description.ilike(f"%{keyword}%")) |
            (Subsidy.eligibility_criteria.ilike(f"%{keyword}%"))
        ).all()
        return subsidies
        
    except Exception as e:
        logger.error(f"❌ Error searching subsidies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching subsidies"
        )

@router.get("/active/deadlines", response_model=List[SubsidyResponse])
async def get_active_subsidies_with_deadlines(db: Session = Depends(get_db)):
    """Get active subsidies with upcoming deadlines"""
    try:
        current_date = datetime.now()
        active_subsidies = db.query(Subsidy).filter(
            (Subsidy.application_deadline > current_date) |
            (Subsidy.application_deadline.is_(None))
        ).order_by(Subsidy.application_deadline).all()
        return active_subsidies
        
    except Exception as e:
        logger.error(f"❌ Error fetching active subsidies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching active subsidies"
        )

@router.get("/summary/state/{state}")
async def get_subsidy_summary_by_state(state: str, db: Session = Depends(get_db)):
    """Get subsidy summary for a state"""
    try:
        subsidies = db.query(Subsidy).filter(Subsidy.state.ilike(f"%{state}%")).all()
        
        if not subsidies:
            return {
                "state": state,
                "total_schemes": 0,
                "total_amount": 0,
                "scheme_types": [],
                "message": f"No subsidies found for {state}"
            }
        
        total_schemes = len(subsidies)
        total_amount = sum(subsidy.amount for subsidy in subsidies)
        scheme_types = list(set(subsidy.scheme_type for subsidy in subsidies))
        
        # Group by scheme type
        type_summary = {}
        for subsidy in subsidies:
            if subsidy.scheme_type not in type_summary:
                type_summary[subsidy.scheme_type] = {
                    "count": 0,
                    "total_amount": 0
                }
            type_summary[subsidy.scheme_type]["count"] += 1
            type_summary[subsidy.scheme_type]["total_amount"] += subsidy.amount
        
        return {
            "state": state,
            "total_schemes": total_schemes,
            "total_amount": total_amount,
            "scheme_types": scheme_types,
            "type_summary": type_summary,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating subsidy summary for {state}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating subsidy summary"
        )

@router.get("/eligibility-check/{subsidy_id}")
async def check_eligibility(subsidy_id: str, user_land_area: float, user_state: str, db: Session = Depends(get_db)):
    """Check eligibility for a specific subsidy"""
    try:
        subsidy = db.query(Subsidy).filter(Subsidy.id == subsidy_id).first()
        if not subsidy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsidy not found"
            )
        
        # Basic eligibility checks (mock implementation)
        eligibility_checks = {
            "state_match": subsidy.state.lower() == user_state.lower(),
            "land_area_sufficient": user_land_area >= 0.5,  # Minimum 0.5 acres
            "scheme_active": True  # Assume all schemes are active
        }
        
        is_eligible = all(eligibility_checks.values())
        
        return {
            "subsidy_id": subsidy_id,
            "scheme_name": subsidy.scheme_name,
            "is_eligible": is_eligible,
            "eligibility_checks": eligibility_checks,
            "next_steps": [
                "Contact the provided contact information",
                "Prepare required documents",
                "Submit application before deadline"
            ] if is_eligible else [
                "Check if you meet the eligibility criteria",
                "Contact local agriculture office for guidance"
            ],
            "contact_info": subsidy.contact_info,
            "deadline": subsidy.application_deadline.isoformat() if subsidy.application_deadline else None
        }
        
    except Exception as e:
        logger.error(f"❌ Error checking eligibility: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking eligibility"
        )
