"""
Main fraud detection service
"""

import time
import json
from datetime import datetime
from typing import Dict, Any

from app.agents.fraud_agents import FraudDetectionAgents
from app.models.schemas import Transaction, FraudPrediction
from app.database.database import get_db, TransactionRecord, FraudAnalysisRecord
from app.config.settings import settings


class FraudDetectionService:
    """Main service for fraud detection"""
    
    def __init__(self):
        self.agents = FraudDetectionAgents()
    
    async def analyze_transaction(self, transaction: Transaction) -> FraudPrediction:
        """Analyze a transaction for fraud"""
        start_time = time.time()
        
        # Convert transaction to dict for agents
        transaction_data = {
            'transaction_id': transaction.transaction_id,
            'user_id': transaction.user_id,
            'amount': transaction.amount,
            'transaction_type': transaction.transaction_type.value,
            'merchant': transaction.merchant,
            'location': transaction.location,
            'timestamp': transaction.timestamp.isoformat(),
            'metadata': transaction.metadata or {}
        }
        
        # Run agent analysis
        try:
            analysis_result = self.agents.analyze_transaction(transaction_data)
            
            # Calculate processing time
            processing_time = int((time.time() - start_time) * 1000)
            
            # Create prediction result
            prediction = FraudPrediction(
                transaction_id=transaction.transaction_id,
                is_fraud=analysis_result['is_fraud'],
                confidence_score=analysis_result['confidence_score'],
                risk_factors=analysis_result['risk_factors'],
                agent_votes=analysis_result['agent_votes'],
                processing_time_ms=processing_time
            )
            
            # Store results in database
            await self._store_analysis_result(transaction, prediction)
            
            return prediction
            
        except Exception as e:
            # Fallback simple analysis if agents fail
            return self._fallback_analysis(transaction, start_time)
    
    def _fallback_analysis(self, transaction: Transaction, start_time: float) -> FraudPrediction:
        """Simple fallback fraud detection if agents fail"""
        processing_time = int((time.time() - start_time) * 1000)
        
        # Simple rule-based detection
        is_fraud = False
        risk_factors = []
        
        # High amount check
        if transaction.amount > 10000:
            is_fraud = True
            risk_factors.append("High amount transaction")
        
        # Round number check
        if transaction.amount % 1000 == 0 and transaction.amount >= 5000:
            is_fraud = True
            risk_factors.append("Round number pattern")
        
        confidence = 0.6 if is_fraud else 0.3
        
        return FraudPrediction(
            transaction_id=transaction.transaction_id,
            is_fraud=is_fraud,
            confidence_score=confidence,
            risk_factors=risk_factors,
            agent_votes={"fallback": is_fraud},
            processing_time_ms=processing_time
        )
    
    async def _store_analysis_result(self, transaction: Transaction, prediction: FraudPrediction):
        """Store transaction and analysis result in database"""
        try:
            db = next(get_db())
            
            # Store transaction
            transaction_record = TransactionRecord(
                transaction_id=transaction.transaction_id,
                user_id=transaction.user_id,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type.value,
                merchant=transaction.merchant,
                location=transaction.location,
                timestamp=transaction.timestamp,
                metadata=json.dumps(transaction.metadata or {})
            )
            
            # Store fraud analysis
            analysis_record = FraudAnalysisRecord(
                transaction_id=prediction.transaction_id,
                is_fraud=prediction.is_fraud,
                confidence_score=prediction.confidence_score,
                risk_factors=json.dumps(prediction.risk_factors),
                agent_votes=json.dumps(prediction.agent_votes),
                processing_time_ms=prediction.processing_time_ms,
                timestamp=datetime.now()
            )
            
            db.add(transaction_record)
            db.add(analysis_record)
            db.commit()
            db.close()
            
        except Exception as e:
            print(f"Database error: {e}")
    
    def get_fraud_decision(self, prediction: FraudPrediction) -> tuple[str, str]:
        """Get final fraud decision and message"""
        if prediction.confidence_score >= settings.FRAUD_THRESHOLD:
            if prediction.is_fraud:
                return "decline", "Transaction declined due to fraud risk"
            else:
                return "review", "Transaction flagged for manual review"
        else:
            return "approve", "Transaction approved" 