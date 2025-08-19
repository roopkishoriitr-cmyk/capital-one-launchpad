from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db, Loan, User
from loguru import logger

router = APIRouter()

class LoanCreate(BaseModel):
    user_id: str
    loan_type: str
    amount: float
    interest_rate: float
    start_date: datetime
    end_date: datetime
    remaining_amount: float

class LoanResponse(BaseModel):
    id: str
    user_id: str
    loan_type: str
    amount: float
    interest_rate: float
    start_date: datetime
    end_date: datetime
    remaining_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoanUpdate(BaseModel):
    loan_type: Optional[str] = None
    amount: Optional[float] = None
    interest_rate: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    remaining_amount: Optional[float] = None
    status: Optional[str] = None

@router.post("/", response_model=LoanResponse)
async def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    """Create a new loan entry"""
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == loan_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        new_loan = Loan(
            user_id=loan_data.user_id,
            loan_type=loan_data.loan_type,
            amount=loan_data.amount,
            interest_rate=loan_data.interest_rate,
            start_date=loan_data.start_date,
            end_date=loan_data.end_date,
            remaining_amount=loan_data.remaining_amount,
            status="active"
        )
        
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        
        logger.info(f"✅ New loan created: {new_loan.loan_type} for user {loan_data.user_id}")
        return new_loan
        
    except Exception as e:
        logger.error(f"❌ Error creating loan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating loan"
        )

@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(loan_id: str, db: Session = Depends(get_db)):
    """Get loan by ID"""
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        return loan
        
    except Exception as e:
        logger.error(f"❌ Error fetching loan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching loan"
        )

@router.get("/user/{user_id}", response_model=List[LoanResponse])
async def get_user_loans(user_id: str, db: Session = Depends(get_db)):
    """Get all loans for a user"""
    try:
        loans = db.query(Loan).filter(Loan.user_id == user_id).all()
        return loans
        
    except Exception as e:
        logger.error(f"❌ Error fetching user loans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user loans"
        )

@router.put("/{loan_id}", response_model=LoanResponse)
async def update_loan(loan_id: str, loan_data: LoanUpdate, db: Session = Depends(get_db)):
    """Update loan information"""
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        # Update only provided fields
        update_data = loan_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(loan, field, value)
        
        db.commit()
        db.refresh(loan)
        
        logger.info(f"✅ Loan updated: {loan_id}")
        return loan
        
    except Exception as e:
        logger.error(f"❌ Error updating loan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating loan"
        )

@router.delete("/{loan_id}")
async def delete_loan(loan_id: str, db: Session = Depends(get_db)):
    """Delete a loan"""
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        db.delete(loan)
        db.commit()
        
        logger.info(f"✅ Loan deleted: {loan_id}")
        return {"message": "Loan deleted successfully"}
        
    except Exception as e:
        logger.error(f"❌ Error deleting loan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting loan"
        )

@router.get("/", response_model=List[LoanResponse])
async def get_all_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all loans with pagination"""
    try:
        loans = db.query(Loan).offset(skip).limit(limit).all()
        return loans
        
    except Exception as e:
        logger.error(f"❌ Error fetching loans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching loans"
        )

@router.get("/type/{loan_type}", response_model=List[LoanResponse])
async def get_loans_by_type(loan_type: str, db: Session = Depends(get_db)):
    """Get loans by type"""
    try:
        loans = db.query(Loan).filter(Loan.loan_type == loan_type).all()
        return loans
        
    except Exception as e:
        logger.error(f"❌ Error fetching loans by type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching loans by type"
        )

@router.get("/status/{status}", response_model=List[LoanResponse])
async def get_loans_by_status(status: str, db: Session = Depends(get_db)):
    """Get loans by status"""
    try:
        loans = db.query(Loan).filter(Loan.status == status).all()
        return loans
        
    except Exception as e:
        logger.error(f"❌ Error fetching loans by status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching loans by status"
        )

@router.post("/{loan_id}/pay")
async def make_payment(loan_id: str, amount: float, db: Session = Depends(get_db)):
    """Make a payment towards a loan"""
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        if amount > loan.remaining_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount cannot exceed remaining loan amount"
            )
        
        loan.remaining_amount -= amount
        
        # Update status if fully paid
        if loan.remaining_amount <= 0:
            loan.status = "paid"
            loan.remaining_amount = 0
        
        db.commit()
        db.refresh(loan)
        
        logger.info(f"✅ Payment made: ₹{amount} for loan {loan_id}")
        return {
            "message": f"Payment of ₹{amount} processed successfully",
            "remaining_amount": loan.remaining_amount,
            "status": loan.status
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing payment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing payment"
        )

@router.get("/user/{user_id}/summary")
async def get_user_loan_summary(user_id: str, db: Session = Depends(get_db)):
    """Get loan summary for a user"""
    try:
        loans = db.query(Loan).filter(Loan.user_id == user_id).all()
        
        total_loans = len(loans)
        total_amount = sum(loan.amount for loan in loans)
        total_remaining = sum(loan.remaining_amount for loan in loans)
        active_loans = len([loan for loan in loans if loan.status == "active"])
        paid_loans = len([loan for loan in loans if loan.status == "paid"])
        
        return {
            "user_id": user_id,
            "total_loans": total_loans,
            "total_amount": total_amount,
            "total_remaining": total_remaining,
            "total_paid": total_amount - total_remaining,
            "active_loans": active_loans,
            "paid_loans": paid_loans,
            "payment_progress": ((total_amount - total_remaining) / total_amount * 100) if total_amount > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching loan summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching loan summary"
        )
