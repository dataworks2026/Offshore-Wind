
"""
main.inference
==============

Thin inference + evaluation helpers around Ultralytics YOLO for this repo.

Why this exists
---------------
This project needs two things:
1) A **cached YOLO model loader** so repeated inference calls do not reload `best.pt`.
2) Stable, script-friendly wrappers for:
   - `model.val(...)` (notebook-parity validation metrics)
   - `model.predict(...)` for deployment-style inference
   - an "evaluation-friendly" prediction format: a list of dicts
     [{"cls": int, "conf": float, "xyxy": [x1,y1,x2,y2]}, ...]

Key notes
---------
- `validate()` returns the Ultralytics metrics object so callers can read fields like
  `metrics.box.map`, `metrics.box.map50`, `metrics.box.map75`, `metrics.box.p`, `metrics.box.r`. :contentReference[oaicite:1]{index=1}
- `predict()` is a light wrapper over Ultralytics `model.predict(...)` with common knobs
  (`imgsz`, `conf`, `iou`) and returns detections in pixel xyxy coordinates. :contentReference[oaicite:2]{index=2}
- `predict_v2()` preserves an older contract used by the notebook/CLI: annotated RGB image + per-class counts.

Typical usage
-------------
>>> from main.inference import validate, predict
>>> metrics = validate("path/to/data.yaml", "best.pt")
>>> print(metrics.box.map)   # mAP50-95 :contentReference[oaicite:3]{index=3}
>>> dets = predict("image.jpg", "best.pt", imgsz=640, conf=0.25, iou=0.45)
>>> print(dets[:2])
"""


from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple, Union, List

import numpy as np
from PIL import Image
import cv2

from ultralytics import YOLO

# CORRECT CLASS NAMES
CLASS_NAMES = ['Drain hole impairment',
                'Lightning Strike',
                'OIL LEAKAGE',
                'PU-tape',
                'Paint',
                'Surface Crack',
                'dirt',
                'le-erosion']


# Module-level cache (so repeated calls don't reload weights)
_MODEL: Optional[YOLO] = None
_MODEL_PATH: Optional[str] = None

# main/inference.py
from typing import Any  # add at top if not present


def validate(data_yaml_path: Union[str, Path], model_path: Optional[Union[str, Path]] = None) -> Any:
    """
    Run Ultralytics validation (notebook-parity).

    This is a thin wrapper around `YOLO(model_path).val(data=...)` and returns the
    Ultralytics metrics object so callers can access:

        metrics.box.map     # mAP50-95
        metrics.box.map50   # mAP50
        metrics.box.map75   # mAP75
        metrics.box.p       # per-class precision array
        metrics.box.r       # per-class recall array

    See Ultralytics Val mode docs and Metric reference for details. :contentReference[oaicite:4]{index=4}

    Args:
        data_yaml_path: Dataset YAML path (Ultralytics format).
        model_path: Path to weights (e.g., best.pt). If None, auto-resolves best.pt.

    Returns:
        Ultralytics metrics object produced by `model.val(...)`.
    """
    model = load_model(model_path=model_path)
    metrics = model.val(data=str(Path(data_yaml_path).resolve()), verbose = True)
    return metrics


def auto_find_best_pt(
    preferred_path: Optional[Union[str, Path]] = "best.pt",
    filename: str = "best.pt",
    search_root: Optional[Union[str, Path]] = None,
) -> str:
    """
    Run Ultralytics validation (notebook-parity).

    This is a thin wrapper around `YOLO(model_path).val(data=...)` and returns the
    Ultralytics metrics object so callers can access:

        metrics.box.map     # mAP50-95
        metrics.box.map50   # mAP50
        metrics.box.map75   # mAP75
        metrics.box.p       # per-class precision array
        metrics.box.r       # per-class recall array

    See Ultralytics Val mode docs and Metric reference for details. :contentReference[oaicite:4]{index=4}

    Args:
        data_yaml_path: Dataset YAML path (Ultralytics format).
        model_path: Path to weights (e.g., best.pt). If None, auto-resolves best.pt.

    Returns:
        Ultralytics metrics object produced by `model.val(...)`.
    """
    if preferred_path is not None:
        p = Path(preferred_path)
        if p.exists():
            return str(p.resolve())

    if search_root is None:
        # repo root heuristic: .../main/inference.py -> repo root is parent of "main"
        search_root = Path(__file__).resolve().parents[1]

    search_root = Path(search_root).resolve()
    matches: List[Path] = [m for m in search_root.rglob(filename) if m.is_file()]

    if not matches:
        raise FileNotFoundError(
            f"Could not find {filename} under {search_root}.\n"
            f"Place best.pt at repo root (./best.pt) or pass model_path explicitly."
        )

    matches.sort(key=lambda x: (len(str(x)), str(x)))
    return str(matches[0].resolve())


def load_model(model_path: Optional[Union[str, Path]] = None) -> YOLO:
    """
    Loads and caches YOLO model (best.pt).
    """
    global _MODEL, _MODEL_PATH

    if model_path is None:
        model_path = auto_find_best_pt(preferred_path="best.pt", filename="best.pt")

    model_path = str(Path(model_path).resolve())

    # If already loaded with same path, reuse
    if _MODEL is not None and _MODEL_PATH == model_path:
        return _MODEL

    _MODEL = YOLO(model_path)
    _MODEL_PATH = model_path
    return _MODEL


ImageLike = Union[Image.Image, np.ndarray, str, Path]

from typing import Dict, Any

def predict(
    image: ImageLike,
    model_path: Optional[Union[str, Path]] = None,
    imgsz=640,
    conf=0.5,
    iou=0.7,
    display = False
) -> List[Dict[str, Any]]:
    """
    Run YOLO inference and return detections in an evaluation-friendly structure.

    Internally calls Ultralytics `model.predict(...)` with common inference knobs:
    - imgsz: resize/letterbox target size
    - conf: confidence threshold
    - iou: NMS IoU threshold :contentReference[oaicite:5]{index=5}

    Args:
        image: Image input. Can be PIL.Image, numpy array (BGR/RGB), filepath, or Path.
        model_path: Weights path (best.pt). If None, uses cached auto-resolved best.pt.
        imgsz: Inference size passed to Ultralytics.
        conf: Confidence threshold passed to Ultralytics.
        iou: NMS IoU threshold passed to Ultralytics.
        display: If True, renders an OpenCV window with the annotated result.

    Returns:
        List of detections, each:
            {
              "cls": int,              # class index
              "conf": float,           # confidence score
              "xyxy": [x1,y1,x2,y2]    # pixel coords (floats)
            }
        Returns an empty list if no boxes are found.
    """
    model = load_model(model_path=model_path)

    results = model.predict(
        source=image,
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        verbose = False
        )

    res = results[0]

    if display:
        # Annotated image (Ultralytics plot -> BGR). Convert BGR -> RGB to match notebook.
        annotated_bgr = res.plot()
        annotated_rgb = annotated_bgr[:, :, ::-1]
        cv2.imshow("annotated", annotated_bgr)

    dets: List[Dict[str, Any]] = []
    if res.boxes is None or len(res.boxes) == 0:
        return dets

    xyxy = res.boxes.xyxy.cpu().numpy()
    conf = res.boxes.conf.cpu().numpy()
    cls  = res.boxes.cls.cpu().numpy().astype(int)

    for i in range(len(cls)):
        dets.append({
            "cls": int(cls[i]),
            "conf": float(conf[i]),
            "xyxy": [float(x) for x in xyxy[i]],
        })

    return dets


def predict_v2(image: ImageLike,
               model_path: Optional[Union[str, Path]] = None,
               imgsz=640,
               conf=0.5,
               iou=0.7,
               ) -> Tuple[np.ndarray, str]:
    """
    Legacy/contract-stable inference wrapper used by CLI + notebook-style outputs.

    Runs Ultralytics prediction and returns:
      1) annotated RGB image (np.ndarray, HxWx3)
      2) a newline-separated summary of counts per class, in CLASS_NAMES order

    Args:
        image: Image input (same accepted types as `predict()`).
        model_path: Weights path (best.pt). If None, uses cached auto-resolved best.pt.
        imgsz: Inference size.
        conf: Confidence threshold.
        iou: NMS IoU threshold.

    Returns:
        (annotated_rgb, summary_text)

        summary_text format:
            "<ClassName0>: <count0>\\n<ClassName1>: <count1>\\n..."
    """
    model = load_model(model_path=model_path)

    results = model.predict(
        source=image,
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        verbose=False,
    )
    res = results[0]

    # Annotated image (Ultralytics plot -> BGR). Convert BGR -> RGB to match notebook.
    annotated_bgr = res.plot()
    annotated_rgb = annotated_bgr[:, :, ::-1]

    # Count detections per class (only those within CLASS_NAMES range)
    counts = {name: 0 for name in CLASS_NAMES}

    if res.boxes is not None and len(res.boxes) > 0:
        class_ids = res.boxes.cls.cpu().numpy().astype(int)
        for cid in class_ids:
            if 0 <= cid < len(CLASS_NAMES):
                counts[CLASS_NAMES[cid]] += 1

    # EXACT formatting: same order, newline joined
    summary = "\n".join([f"{name}: {counts[name]}" for name in CLASS_NAMES])

    return annotated_rgb, summary
