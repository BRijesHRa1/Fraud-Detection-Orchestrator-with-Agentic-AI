"""
FastAPI routes for fraud detection
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

from app.models.schemas import (
    FraudAnalysisRequest, 
    FraudAnalysisResponse, 
    Transaction,
    TransactionType
)
from app.services.fraud_service import FraudDetectionService

# Create router
router = APIRouter()

# Initialize fraud detection service
fraud_service = FraudDetectionService()


@router.post("/analyze", response_model=FraudAnalysisResponse)
async def analyze_transaction(request: FraudAnalysisRequest):
    """Analyze a transaction for fraud"""
    try:
        # Run fraud analysis
        prediction = await fraud_service.analyze_transaction(request.transaction)
        
        # Get final decision
        action, message = fraud_service.get_fraud_decision(prediction)
        
        # Return response
        return FraudAnalysisResponse(
            transaction_id=prediction.transaction_id,
            prediction=prediction,
            action=action,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/quick-test")
async def quick_test():
    """Quick test endpoint with sample transaction"""
    
    # Create sample transaction
    sample_transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        user_id="user_123",
        amount=15000.0,  # High amount to trigger fraud detection
        transaction_type=TransactionType.PURCHASE,
        merchant="Online Store",
        location="New York, NY",
        timestamp=datetime.now(),
        metadata={"device": "mobile", "ip": "192.168.1.1"}
    )
    
    # Analyze the transaction
    prediction = await fraud_service.analyze_transaction(sample_transaction)
    action, message = fraud_service.get_fraud_decision(prediction)
    
    return {
        "test_transaction": sample_transaction.dict(),
        "prediction": prediction.dict(),
        "action": action,
        "message": message
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Fraud Detection API",
        "timestamp": datetime.now().isoformat()
    } 