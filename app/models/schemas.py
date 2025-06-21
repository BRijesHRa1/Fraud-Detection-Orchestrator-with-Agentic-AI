"""
Simple data models for fraud detection
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class Transaction(BaseModel):
    """Transaction data model"""
    transaction_id: str
    user_id: str
    amount: float
    transaction_type: TransactionType
    merchant: Optional[str] = None
    location: Optional[str] = None
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class FraudPrediction(BaseModel):
    """Fraud prediction result"""
    transaction_id: str
    is_fraud: bool
    confidence_score: float
    risk_factors: list[str]
    agent_votes: Dict[str, bool]
    processing_time_ms: int


class FraudAnalysisRequest(BaseModel):
    """Request for fraud analysis"""
    transaction: Transaction


class FraudAnalysisResponse(BaseModel):
    """Response from fraud analysis"""
    transaction_id: str
    prediction: FraudPrediction
    action: str  # "approve", "decline", "review"
    message: str 