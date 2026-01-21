"""
Inference Service - Wraps the main/inference.py module
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image
import io
import base64

# Add parent directory to path to import main.inference
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.inference import predict, predict_detections, load_model, CLASS_NAMES

class InferenceService:
    def __init__(self, model_path: str = "best.pt"):
        """Initialize inference service with model path"""
        self.model_path = Path(__file__).parent.parent.parent.parent / model_path
        self.model = None

    def load_model_if_needed(self):
        """Load model if not already loaded (caching)"""
        if self.model is None:
            self.model = load_model(str(self.model_path))
        return self.model

    def predict_from_bytes(
        self,
        image_bytes: bytes,
        conf: float = 0.5,
        iou: float = 0.7,
        imgsz: int = 640
    ) -> List[Dict]:
        """
        Run inference on image bytes

        Args:
            image_bytes: Image file bytes
            conf: Confidence threshold
            iou: IoU threshold for NMS
            imgsz: Image size for inference

        Returns:
            List of detection dicts: [{"cls": int, "conf": float, "xyxy": [x1,y1,x2,y2]}, ...]
        """
        # Load model
        self.load_model_if_needed()

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Use predict_detections which returns raw detections list
        detections = predict_detections(
            image,
            model_path=str(self.model_path),
            imgsz=imgsz,
            conf=conf,
            iou=iou
        )

        return detections

    def format_detections(self, detections: List[Dict]) -> Dict:
        """
        Format detections into response structure

        Args:
            detections: List of detection dicts from predict()

        Returns:
            Formatted response dict
        """
        # Count damages by class
        damage_counts = {}
        for det in detections:
            cls_idx = det['cls']
            cls_name = CLASS_NAMES[cls_idx]
            if cls_name not in damage_counts:
                damage_counts[cls_name] = 0
            damage_counts[cls_name] += 1

        # Format detections for frontend
        formatted_detections = []
        for det in detections:
            cls_idx = det['cls']
            cls_name = CLASS_NAMES[cls_idx]
            x1, y1, x2, y2 = det['xyxy']

            formatted_detections.append({
                'class': cls_name,
                'confidence': float(det['conf']),
                'bbox': {
                    'x1': float(x1),
                    'y1': float(y1),
                    'x2': float(x2),
                    'y2': float(y2)
                }
            })

        return {
            'total_detections': len(detections),
            'damages_found': list(damage_counts.keys()),
            'damage_counts': damage_counts,
            'detections': formatted_detections
        }

    def image_to_base64(self, image_array: np.ndarray) -> str:
        """Convert numpy image array to base64 string"""
        # Convert BGR to RGB if needed
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            image_array = image_array[:, :, ::-1]

        # Convert to PIL Image
        image = Image.fromarray(image_array.astype('uint8'))

        # Convert to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

        # Encode to base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return f"data:image/jpeg;base64,{img_base64}"


# Global instance
inference_service = InferenceService()
