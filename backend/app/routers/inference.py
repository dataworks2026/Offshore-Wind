"""
Inference API Router
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import traceback

from app.services.inference_service import inference_service
from app.models.schemas import InferenceResponse, ErrorResponse

router = APIRouter()


@router.post("/inference/predict", response_model=InferenceResponse)
async def predict_damage(
    file: UploadFile = File(...),
    conf: Optional[float] = Form(0.25),
    iou: Optional[float] = Form(0.45),
    imgsz: Optional[int] = Form(640)
):
    """
    Run damage detection on uploaded wind turbine blade image

    Args:
        file: Image file (jpeg, jpg, png)
        conf: Confidence threshold (0-1)
        iou: IoU threshold for NMS (0-1)
        imgsz: Image size for inference

    Returns:
        Detection results with annotated image
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image bytes
        image_bytes = await file.read()

        # Run inference
        detections = inference_service.predict_from_bytes(
            image_bytes=image_bytes,
            conf=conf,
            iou=iou,
            imgsz=imgsz
        )

        # Format response
        result = inference_service.format_detections(detections)

        # Note: We're not including annotated image to keep response lightweight
        # If you need it, uncomment the following lines:
        # annotated_image = inference_service.image_to_base64(annotated_img)
        # result['annotated_image'] = annotated_image

        return InferenceResponse(
            success=True,
            message=f"Detection completed. Found {result['total_detections']} damages.",
            total_detections=result['total_detections'],
            damages_found=result['damages_found'],
            damage_counts=result['damage_counts'],
            detections=result['detections'],
            annotated_image=None
        )

    except Exception as e:
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"Error in predict_damage: {error_trace}")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error processing image",
                "error": error_msg
            }
        )


@router.get("/inference/classes")
async def get_classes():
    """
    Get list of damage classes the model can detect

    Returns:
        List of class names
    """
    from main.inference import CLASS_NAMES

    return {
        "success": True,
        "classes": CLASS_NAMES,
        "total_classes": len(CLASS_NAMES)
    }
