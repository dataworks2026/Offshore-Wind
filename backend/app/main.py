"""
FastAPI Backend for Offshore Wind Turbine Damage Detection
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inference

app = FastAPI(
    title="Offshore Wind Damage Detection API",
    description="API for detecting damage on offshore wind turbine blades using YOLOv8",
    version="1.0.0"
)

# CORS configuration for frontend
# Use ALLOWED_ORIGINS env var, or default to allowing all origins
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
if allowed_origins_env == "*":
    # Allow all origins
    allow_origins = ["*"]
else:
    # Parse comma-separated origins
    allow_origins = [origin.strip() for origin in allowed_origins_env.split(",")]

# Always include common development origins
default_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]
for origin in default_origins:
    if origin not in allow_origins and "*" not in allow_origins:
        allow_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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
