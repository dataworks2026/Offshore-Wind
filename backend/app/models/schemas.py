"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    class_name: str = Field(alias="class")
    confidence: float
    bbox: BoundingBox

    class Config:
        populate_by_name = True


class InferenceResponse(BaseModel):
    success: bool
    message: str
    total_detections: int
    damages_found: List[str]
    damage_counts: Dict[str, int]
    detections: List[Detection]
    annotated_image: Optional[str] = None  # base64 encoded image


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None
