"""
FastAPI Backend for Offshore Wind Turbine Damage Detection
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inference

app = FastAPI(
    title="Offshore Wind Damage Detection API",
    description="API for detecting damage on offshore wind turbine blades using YOLOv8",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inference.router, prefix="/api", tags=["inference"])

@app.get("/")
async def root():
    return {
        "message": "Offshore Wind Turbine Damage Detection API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
