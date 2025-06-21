"""
Simple SQLite database setup
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
import json

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TransactionRecord(Base):
    """Database model for transactions"""
    __tablename__ = "transactions"
    
    transaction_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    merchant = Column(String)
    location = Column(String)
    timestamp = Column(DateTime, nullable=False)
    metadata = Column(Text)  # JSON string


class FraudAnalysisRecord(Base):
    """Database model for fraud analysis results"""
    __tablename__ = "fraud_analysis"
    
    transaction_id = Column(String, primary_key=True)
    is_fraud = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=False)
    risk_factors = Column(Text)  # JSON string
    agent_votes = Column(Text)  # JSON string
    processing_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)


def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 