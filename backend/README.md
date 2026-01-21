# Offshore Wind Damage Detection - Backend API

FastAPI backend for wind turbine blade damage detection using YOLOv8.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /api/inference/predict
Upload an image and get damage detection results.

**Request:**
- `file`: Image file (multipart/form-data)
- `conf`: Confidence threshold (optional, default: 0.5)
- `iou`: IoU threshold (optional, default: 0.7)
- `imgsz`: Image size (optional, default: 640)

**Response:**
```json
{
  "success": true,
  "message": "Detection completed. Found 2 damages.",
  "total_detections": 2,
  "damages_found": ["dirt", "le-erosion"],
  "damage_counts": {
    "dirt": 1,
    "le-erosion": 1
  },
  "detections": [
    {
      "class": "dirt",
      "confidence": 0.85,
      "bbox": {
        "x1": 100.5,
        "y1": 200.3,
        "x2": 300.7,
        "y2": 400.9
      }
    }
  ]
}
```

### GET /api/inference/classes
Get list of all damage classes the model can detect.

**Response:**
```json
{
  "success": true,
  "classes": [
    "Drain hole impairment",
    "Lightning Strike",
    "OIL LEAKAGE",
    "PU-tape",
    "Paint",
    "Surface Crack",
    "dirt",
    "le-erosion"
  ],
  "total_classes": 8
}
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── routers/
│   │   └── inference.py     # Inference endpoints
│   ├── services/
│   │   └── inference_service.py  # Business logic
│   └── models/
│       └── schemas.py       # Pydantic models
├── requirements.txt
└── README.md
```

## Testing with curl

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test inference
curl -X POST "http://localhost:8000/api/inference/predict" \
  -F "file=@path/to/image.jpg" \
  -F "conf=0.5" \
  -F "iou=0.7"

# Get damage classes
curl http://localhost:8000/api/inference/classes
```

## Notes

- The model weights (`best.pt`) should be in the root directory of the project
- First inference call may be slower as the model loads into memory
- Subsequent calls are faster due to model caching
