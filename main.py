"""
Main FastAPI application for Fraud Detection System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config.settings import settings
from app.api.routes import router
from app.database.database import create_tables

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered fraud detection system with collaborative agents",
    version="1.0.0"
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1/fraud")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting Fraud Detection System...")
    create_tables()
    print("✅ Database initialized")
    print(f"🔍 Fraud threshold set to: {settings.FRAUD_THRESHOLD}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fraud Detection System with Agentic AI",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/v1/fraud/analyze",
            "quick_test": "/api/v1/fraud/quick-test",
            "health": "/api/v1/fraud/health",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 