"""
scripts.run_inference
=====================

CLI entrypoint to evaluate YOLO weights on a dataset split and to compare:

1) Ultralytics `val()` metrics (notebook-parity) via `main.inference.validate()`. :contentReference[oaicite:6]{index=6}
2) A lightweight, inference-driven evaluation that uses `main.inference.predict()` outputs
   to compute sanity-check precision/recall (overall + per-class).

This script is intentionally "no notebook required": it reads the dataset YAML, resolves
the split image list, runs inference on those images, and prints metrics to stdout.

Typical usage
-------------
python scripts/run_inference.py --mode test_pr --weights path/to/best.pt --data-yaml wind-combined-2/data_8class_oversampled_max.yaml
"""
# scripts/run_inference.py
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

import numpy as np

import yaml
from main.inference import auto_find_best_pt, validate, predict

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
import cv2

#=========================================================================

def resolve_dataset_base(yaml_path: Path, data: dict) -> Path:
    """
    Ultralytics dataset yamls often have:
      path: /dataset/root
      train: images/train
      val: images/val
      test: images/test
    If 'path' is missing, base is yaml's parent.
    """
    if "path" in data and data["path"] is not None:
        return Path(data["path"]).expanduser().resolve()
    return yaml_path.parent.resolve()


def list_images_from_yaml_split(yaml_path: Path, split_value: str) -> List[Path]:
    """
    split_value can be:
      - a directory (e.g., test/images)
      - a txt file listing image paths
    """
    p = Path(split_value)
    if p.suffix.lower() == ".txt":
        # list file
        lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        return [Path(ln) for ln in lines]
    else:
        # directory
        if p.is_dir():
            return sorted([f for f in p.rglob("*") if f.suffix.lower() in IMG_EXTS])
        # if it's a glob or missing dir, treat as pattern
        return sorted([Path(x) for x in p.parent.glob(p.name)])


def image_to_label_path(img_path: Path) -> Path:
    """
    Standard YOLO dataset structure: images/.../foo.jpg -> labels/.../foo.txt
    """
    parts = list(img_path.parts)
    # replace first occurrence of "images" with "labels"
    if "images" in parts:
        i = parts.index("images")
        parts[i] = "labels"
        return Path(*parts).with_suffix(".txt")
    # fallback: same folder, .txt
    return img_path.with_suffix(".txt")


def yolo_txt_to_xyxy(label_txt: Path, img_w: int, img_h: int):
    """
    YOLO label format: class x_center y_center width height (normalized 0..1). :contentReference[oaicite:3]{index=3}
    Returns list of (cls_id, [x1,y1,x2,y2]) in pixel coords.
    """
    gts = []
    if not label_txt.exists():
        return gts
    content = label_txt.read_text(encoding="utf-8").strip()
    if not content:
        return gts

    for line in content.splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        cls_id = int(float(parts[0]))
        xc = float(parts[1]) * img_w
        yc = float(parts[2]) * img_h
        w  = float(parts[3]) * img_w
        h  = float(parts[4]) * img_h

        x1 = xc - w / 2
        y1 = yc - h / 2
        x2 = xc + w / 2
        y2 = yc + h / 2
        gts.append((cls_id, [x1, y1, x2, y2]))
    return gts


def iou_xyxy(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    denom = area_a + area_b - inter
    return inter / denom if denom > 0 else 0.0

def best_iou_anyclass(pred_box, gts):
    best = 0.0
    best_cls = None
    for cls_id, gt_box in gts:
        v = iou_xyxy(pred_box, gt_box)
        if v > best:
            best = v
            best_cls = cls_id
    return best, best_cls

from collections import defaultdict
from typing import Dict, List, Tuple

def eval_predict_per_class_pr(
    image_paths: List[Path],
    weights: str,
    num_classes: int,
    conf_filter: float | None = None,   # if None, use preds as returned; else filter here
    debug: bool = False,
) -> Dict:
    """
    Compute per-class TP/FP/FN + precision/recall using greedy matching.

    Pipeline (per image):
      - Load image and GT labels (YOLO txt).
      - Run `predict(...)` to get detections: [{"cls","conf","xyxy"}, ...].
      - Optionally filter predictions by confidence (`conf_filter`).
      - Greedily match predictions to GT of the same class by highest IoU.
      - Count TP/FP/FN per class; then compute precision/recall per class.

    Important:
      - This is a "single operating point" metric unless you sweep `conf_filter`.
      - This does NOT compute mAP/AP curves (which require PR integration).

    Args:
        image_paths: List of image paths for evaluation.
        weights: Path to YOLO weights.
        num_classes: Total number of classes in the dataset YAML.
        conf_filter: If set, only predictions with conf >= conf_filter are used.
        debug: If True, may print debug messages.

    Returns:
        Dict containing arrays:
          tp, fp, fn, gt, pred, precision, recall
        each shaped (num_classes,).
    """

    # per-class counters
    tp = np.zeros(num_classes, dtype=np.int64)
    fp = np.zeros(num_classes, dtype=np.int64)
    fn = np.zeros(num_classes, dtype=np.int64)
    gt_count = np.zeros(num_classes, dtype=np.int64)
    pred_count = np.zeros(num_classes, dtype=np.int64)

    for img_path in image_paths:
        frame = cv2.imread(str(img_path))
        h, w = frame.shape[:2]

        # preds: list of dicts: {"cls": int, "conf": float, "xyxy": [x1,y1,x2,y2]}
        preds = predict(frame, model_path=weights)

        if conf_filter is not None:
            preds = [p for p in preds if float(p["conf"]) >= float(conf_filter)]

        # GT
        lbl_path = image_to_label_path(img_path)
        gts = yolo_txt_to_xyxy(lbl_path, w, h)

        for cls_id, _ in gts:
            if 0 <= cls_id < num_classes:
                gt_count[cls_id] += 1

        for p in preds:
            cid = int(p["cls"])
            if 0 <= cid < num_classes:
                pred_count[cid] += 1

        # group gts by class
        gt_by_cls = defaultdict(list)
        for cls_id, box in gts:
            if 0 <= cls_id < num_classes:
                gt_by_cls[cls_id].append({"box": box, "matched": False})

        preds_sorted = sorted(preds, key=lambda d: float(d["conf"]), reverse=True)

        for p in preds_sorted:
            cls_id = int(p["cls"])
            if not (0 <= cls_id < num_classes):
                continue

            pbox = p["xyxy"]
            candidates = gt_by_cls.get(cls_id, [])

            best_i = -1
            best_iou = 0.0
            for j, gt in enumerate(candidates):
                if gt["matched"]:
                    continue
                iou = iou_xyxy(pbox, gt["box"])
                if iou > best_iou:
                    best_iou = iou
                    best_i = j

            if best_i >= 0 :
                candidates[best_i]["matched"] = True
                tp[cls_id] += 1
            else:
                fp[cls_id] += 1

        # FNs: unmatched GTs
        for cls_id, items in gt_by_cls.items():
            for gt in items:
                if not gt["matched"]:
                    fn[cls_id] += 1

    precision = np.divide(tp, tp + fp, out=np.zeros_like(tp, dtype=float), where=(tp + fp) > 0)
    recall = np.divide(tp, tp + fn, out=np.zeros_like(tp, dtype=float), where=(tp + fn) > 0)

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "gt": gt_count,
        "pred": pred_count,
        "precision": precision,
        "recall": recall,
        "conf_filter": conf_filter,
    }


def eval_predict_precision_recall(
    image_paths: List[Path],
    weights: str,
    match_iou: float = 0.25,
    debug: bool = False
) -> dict:
    """
    Compute overall precision/recall (single threshold) on a dataset split.

    This is a simple sanity-check metric:
      - Uses `predict(...)` to generate detections.
      - Greedy matching by IoU against same-class GT boxes.
      - Aggregates TP/FP/FN across all classes to output a single P/R.

    Args:
        image_paths: Images to evaluate.
        weights: Path to YOLO weights.
        match_iou: IoU threshold to count a match as TP (if enforced in code).
        debug: Print debug diagnostics.

    Returns:
        Dict with images, gt, pred, tp, fp, fn, precision, recall, match_iou.
    """
    TP = FP = FN = 0
    n_images = 0
    n_gt = 0
    n_pred = 0

    for img_path in image_paths:
        frame = cv2.imread(str(img_path))
        h,w = frame.shape[0:2]
        #h,w,c = Mat.shape

        # Predictions (already filtered by conf=0.25 inside inference.py)
        preds = predict(frame, model_path=weights)

        n_pred += len(preds)

        # Ground-truth
        lbl_path = image_to_label_path(img_path)
        gts = yolo_txt_to_xyxy(lbl_path, w, h)
        n_gt += len(gts)

        # group gts by class with "matched" flags
        gt_by_cls = {}
        for cls_id, box in gts:
            gt_by_cls.setdefault(cls_id, []).append({"box": box, "matched": False})

        # sort predictions by confidence desc
        preds_sorted = sorted(preds, key=lambda d: d["conf"], reverse=True)

        if preds_sorted and gts and debug:
            biou, bcls = best_iou_anyclass(preds_sorted[0]["xyxy"], gts)
            print(f"[DEBUG] {img_path.name} bestIoU_anyclass={biou:.3f} bestGTcls={bcls} predCls={preds_sorted[0]['cls']}")


        for p in preds_sorted:
            cls_id = p["cls"]
            pbox = p["xyxy"]

            candidates = gt_by_cls.get(cls_id, [])
            best_iou = 0.0
            best_j = None
            for j, gt in enumerate(candidates):
                if gt["matched"]:
                    continue
                iou = iou_xyxy(pbox, gt["box"])
                if iou > best_iou:
                    best_iou = iou
                    best_j = j

            if best_j is not None:
            #if best_j is not None and best_iou >= match_iou:
                candidates[best_j]["matched"] = True
                TP += 1
            else:
                FP += 1

        # any unmatched GT is FN
        for cls_id, items in gt_by_cls.items():
            for gt in items:
                if not gt["matched"]:
                    FN += 1

        n_images += 1

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0

    return {
        "images": n_images,
        "gt": n_gt,
        "pred": n_pred,
        "tp": TP,
        "fp": FP,
        "fn": FN,
        "precision": precision,
        "recall": recall,
        "match_iou": match_iou,
    }


def run_test_pr_mode(repo_root: Path, weights: str, args) -> None:
    """
    Load dataset YAML, resolve the requested split image list, and print:

      1) Overall fixed-threshold precision/recall (sanity-check)
      2) Per-class precision/recall arrays (matching YAML class order)

    Inputs are controlled by CLI args:
      --data-yaml, --limit, --match_iou, and the inference settings used inside `predict()`.

    Side effects:
      - Prints evaluation summaries to stdout.
    """

    yaml_path = auto_find_data_yaml(repo_root, preferred=args.data_yaml)
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    base = resolve_dataset_base(yaml_path, data)

    # Prefer "test" split; fallback to "val" if missing
    split_key = "val" if "val" in data else ("val" if "val" in data else None)
    if split_key is None:
        raise RuntimeError(f"No 'test' or 'val' key found in dataset yaml: {yaml_path}")

    split_value = data[split_key]
    split_path = (base / split_value).resolve() if not Path(split_value).is_absolute() else Path(split_value).resolve()

    image_paths = list_images_from_yaml_split(yaml_path, str(split_path))

    if not image_paths:
        raise RuntimeError(f"No images found for split '{split_key}' using path: {split_path}")

    # only top N images
    limit = getattr(args, "limit", None)
    if limit is not None and int(limit) > 0:
        image_paths = image_paths[: int(limit)]
    
    match_iou = getattr(args, "match_iou", 0.25)

    print(f"Predict-eval split: {split_key}")
    print(f"Dataset YAML      : {yaml_path}")
    print(f"Split path        : {split_path}")
    print(f"Using weights     : {weights}")
    print(f"Images evaluated  : {len(image_paths)}")
    print(f"Match IoU thresh  : {match_iou}")
    print(f"Predict settings  : imgsz=640, conf=0.25 (inference.py), NMS iou=0.45 (inference.py)")

    metrics = eval_predict_precision_recall(image_paths, weights=weights, match_iou=float(match_iou))

    print("\n=== Predict-on-test — Fixed-threshold Metrics (for predict() sanity) ===")
    print("Images     :", metrics["images"])
    print("GT boxes   :", metrics["gt"])
    print("Pred boxes :", metrics["pred"])
    print("TP         :", metrics["tp"])
    print("FP         :", metrics["fp"])
    print("FN         :", metrics["fn"])
    print("Precision  :", metrics["precision"])
    print("Recall     :", metrics["recall"])

    names = data.get("names", [])
    num_classes = len(names)

    #m = eval_predict_per_class_pr(image_paths, weights, num_classes, conf_filter=0.25)
    m = eval_predict_per_class_pr(image_paths, weights, num_classes, conf_filter=None)

    # print(f"{'Class':<22} {'GT':>6} {'Pred':>6} {'TP':>6} {'FP':>6} {'FN':>6} {'P':>8} {'R':>8}")
    # for i, name in enumerate(names):
    #     print(f"{name:<22} {m['gt'][i]:>6} {m['pred'][i]:>6} {m['tp'][i]:>6} {m['fp'][i]:>6} {m['fn'][i]:>6}"
    #         f" {m['precision'][i]:>8.3f} {m['recall'][i]:>8.3f}")

    p_list = []
    r_list = []
    for i, name in enumerate(names):
        if m['gt'][i] > 0:
            #print(f"{name:<22} {m['precision'][i]:>8.3f} {m['recall'][i]:>8.3f}")
            p_list.append(round(float(m['precision'][i]),3))
            r_list.append(round(float(m['recall'][i]),3))

    print(f"Precision:    {p_list}")
    print(f"Recall:       {r_list}")

#=========================================================================

def auto_find_data_yaml(repo_root: Path, preferred: Optional[str] = None) -> Path:
    """
    If user passes --data-yaml, use it.
    Otherwise try to locate data_8class_oversampled_max.yaml anywhere under repo root.
    """
    if preferred:
        p = Path(preferred)
        if p.exists():
            return p.resolve()
        raise FileNotFoundError(f"--data-yaml path not found: {p}")

    # Common filename used in notebook
    filename = "data_8class_oversampled_max.yaml"
    matches = list(repo_root.rglob(filename))
    if not matches:
        raise FileNotFoundError(
            f"Could not find {filename} under repo root: {repo_root}\n"
            f"Pass it explicitly with --data-yaml <path>."
        )
    matches.sort(key=lambda x: (len(str(x)), str(x)))
    return matches[0].resolve()


def run_val_mode(repo_root: Path, weights: str, args) -> None:
    # Notebook parity variables
    root = Path(args.root)
    yaml_oversampled_path = auto_find_data_yaml(repo_root, preferred=args.data_yaml)

    run_name = args.run_name
    run_dir = Path(args.runs_detect_dir) / run_name

    # weights_path in notebook (you set it to "best.pt")
    weights_path = weights

    # ---- EXACT notebook prints ----
    print("Loading oversampled model from:", weights_path)
    print("Using YAML:", yaml_oversampled_path)

    # 1) Load best weights and run numeric eval (via inference.py wrapper)
    metrics_os = validate(data_yaml_path=yaml_oversampled_path, model_path=weights_path)

    print("\n=== 8-Class Oversampled + Augmented Model — Numeric Metrics ===")
    print("mAP50-95:", metrics_os.box.map)
    print("mAP50   :", metrics_os.box.map50)
    print("mAP75   :", metrics_os.box.map75)
    print("Precision:", metrics_os.box.p)
    print("Recall   :", metrics_os.box.r)
    print("False alarm rate   :", 1 - metrics_os.box.p)
    print("Missed damage rate :", 1 - metrics_os.box.r)

    print("\n=== Precision-Recall Metrics (AVG) ===")
    pr_avg = sum(metrics_os.box.p)/len(metrics_os.box.p)
    re_avg = sum(metrics_os.box.r)/len(metrics_os.box.r)
    print("Precision:", pr_avg)
    print("Recall   :", re_avg)

    # 2) Visual metrics: confusion matrix + training curves
    print("\n=== Visual Metrics ===")
    cm_path = run_dir / "confusion_matrix.png"
    res_path = run_dir / "results.png"

    if cm_path.exists():
        # Notebook uses display(); in CLI we print the path (still parity-friendly)
        print("confusion_matrix.png:", cm_path)
    else:
        print("No confusion_matrix.png found at", cm_path)

    if res_path.exists():
        print("results.png:", res_path)
    else:
        print("No results.png found at", res_path)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        #choices=["infer", "val"],
        choices=["infer", "val", "test_pr"],
        default="test_pr",
        help="infer: run predict() on images; val: run YOLO validation like the notebook.",
    )
    ap.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Path to best.pt. If omitted, auto-find best.pt under repo root.",
    )

    # ---- infer mode args ----
    ap.add_argument(
        "--images",
        nargs="*",
        default=None,
        help="One or more image paths. If omitted, uses cases/*/images/*.",
    )
    ap.add_argument(
        "--outdir",
        type=str,
        default="out_inference",
        help="Output directory for annotated images + summaries (infer mode).",
    )

    # ---- val mode args (notebook parity) ----
    ap.add_argument(
        "--data-yaml",
        type=str,
        default=r"wind-combined-2\data_8class_oversampled_max.yaml",
        help="Path to data_8class_oversampled_max.yaml. If omitted, auto-searches under repo root.",
    )
    ap.add_argument(
        "--root",
        type=str,
        default="wind-combined-2",
        help="Notebook variable 'root' (used only for printing parity).",
    )
    ap.add_argument(
        "--run-name",
        type=str,
        default="train_8class_oversampled_max",
        help="Notebook variable 'run_name' (used to locate runs/detect/<run_name> pngs).",
    )
    ap.add_argument(
        "--runs-detect-dir",
        type=str,
        default="runs/detect",
        help="Base runs/detect directory (used for confusion_matrix.png and results.png checks).",
    )

    ap.add_argument("--limit", type=int, default=None, help="Only evaluate top N test images (sorted).")
    ap.add_argument("--match_iou", type=float, default=0.25, help="IoU threshold to match pred->GT for TP.")


    return ap.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    weights = args.weights or auto_find_best_pt(
        preferred_path=repo_root / "best.pt",
        filename="best.pt",
        search_root=repo_root,
    )

    print("\n=================================== Ultralytics validate() ===================================\n")
    run_val_mode(repo_root, weights, args)
    print("\n=================================== Inference-based-Validaton() ===================================\n")
    run_test_pr_mode(repo_root, weights, args)

if __name__ == "__main__":
    main()
