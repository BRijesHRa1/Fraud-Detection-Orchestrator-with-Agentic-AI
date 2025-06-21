"""
Simple configuration for local fraud detection system
"""
import os

class Settings:
    """Simple application settings"""
    
    # Application
    APP_NAME = "Fraud Detection System"
    
    # Server
    HOST = "0.0.0.0"  # Changed to bind to all interfaces for Docker
    PORT = int(os.getenv("PORT", 8000))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fraud_detection.db")
    
    # ChromaDB
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
    # Ollama
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Fraud Detection
    FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "0.7"))
    MAX_RESPONSE_TIME = int(os.getenv("MAX_RESPONSE_TIME", "500"))  # milliseconds


# Global settings instance
settings = Settings() 