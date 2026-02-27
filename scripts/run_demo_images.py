#!/usr/bin/env python3
"""
Curate demo-ready images (original + annotated) that are:
- Correct: predicted class matches a GT box of same class with IoU >= iou_min
- Clean: strong confidence, reasonable box size, low clutter in frame

Reuses existing repo helpers:
- scripts/run_inference.py: auto_find_data_yaml, resolve_dataset_base, list_images_from_yaml_split,
                           image_to_label_path, yolo_txt_to_xyxy, iou_xyxy
- main/inference.py: auto_find_best_pt, predict_detections, predict, CLASS_NAMES

Example:
  python scripts/curate_demo_images.py ^
    --data-yaml wind-combined-2/data_8class_oversampled_max.yaml ^
    --weights best.pt ^
    --split val ^
    --outdir demo_images ^
    --imgsz 640 --conf 0.5 --iou 0.7 ^
    --conf-clean 0.45 --iou-min 0.50 ^
    --per-class 4 --max-per-class 30 ^
    --limit 2000
"""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import yaml

from main.inference import auto_find_best_pt, predict_detections, predict, CLASS_NAMES
from scripts.run_inference import (
    auto_find_data_yaml,
    resolve_dataset_base,
    list_images_from_yaml_split,
    image_to_label_path,
    yolo_txt_to_xyxy,
    iou_xyxy,
)

# -----------------------------
# Helpers
# -----------------------------

def safe_name(s: str) -> str:
    return (
        s.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )

def box_is_clean_xyxy(
    xyxy: List[float],
    img_w: int,
    img_h: int,
    min_wh_px: int = 24,
    min_area_frac: float = 0.001,
    max_area_frac: float = 0.70,
) -> bool:
    x1, y1, x2, y2 = xyxy
    bw = max(0.0, x2 - x1)
    bh = max(0.0, y2 - y1)
    if bw < min_wh_px or bh < min_wh_px:
        return False
    area = bw * bh
    frac = area / float(img_w * img_h + 1e-9)
    return (frac >= min_area_frac) and (frac <= max_area_frac)

def resolve_target_class_ids(target_names: List[str]) -> Dict[int, str]:
    """
    Map user-friendly target strings to CLASS_NAMES IDs (case-insensitive substring match).
    Returns dict {class_id: canonical_class_name}.
    """
    ids: Dict[int, str] = {}

    lower_names = [n.lower() for n in CLASS_NAMES]

    for t in target_names:
        tl = t.lower().strip()
        # direct exact match
        if tl in lower_names:
            cid = lower_names.index(tl)
            ids[cid] = CLASS_NAMES[cid]
            continue

        # substring match (e.g. "leading edge erosion" -> "le-erosion")
        matches = [i for i, cn in enumerate(lower_names) if tl in cn or cn in tl]
        if len(matches) == 1:
            cid = matches[0]
            ids[cid] = CLASS_NAMES[cid]
            continue

        # common aliases for your repo class names
        alias_map = {
            "surface cracks": "surface crack",
            "surface crack": "surface crack",
            "leading-edge erosion": "le-erosion",
            "leading edge erosion": "le-erosion",
            "le erosion": "le-erosion",
            "lightning strike damage": "lightning strike",
            "lightning strike": "lightning strike",
            "oil leakage": "oil leakage",
            "oil leak": "oil leakage",
        }
        if tl in alias_map:
            want = alias_map[tl]
            if want in lower_names:
                cid = lower_names.index(want)
                ids[cid] = CLASS_NAMES[cid]
                continue

        raise ValueError(
            f"Could not map target '{t}' to a CLASS_NAMES entry.\n"
            f"CLASS_NAMES={CLASS_NAMES}"
        )

    return ids

def image_passes_for_targets(
    img_path: Path,
    preds: List[Dict],
    gts: List[Tuple[int, List[float]]],
    target_ids: List[int],
    conf_clean: float,
    iou_min: float,
    max_total_boxes: int,
    max_non_target_strong: int,
    min_wh_px: int,
) -> List[int]:
    """
    Returns list of target class IDs that this image qualifies for (can be multiple).
    Criteria:
      - low clutter
      - at least one pred of target class is clean AND matches an un-matched GT of same class with IoU>=iou_min
    """
    # Load image dims once
    im = cv2.imread(str(img_path))
    if im is None:
        return []
    h, w = im.shape[:2]

    # clutter constraints
    if len(preds) > max_total_boxes:
        return []

    non_target_strong = 0
    for p in preds:
        if float(p["conf"]) >= conf_clean and int(p["cls"]) not in target_ids:
            non_target_strong += 1
    if non_target_strong > max_non_target_strong:
        return []

    # prepare GT by class
    gt_by_cls: Dict[int, List[Dict]] = {}
    for cid, box in gts:
        gt_by_cls.setdefault(int(cid), []).append({"box": box, "matched": False})

    # strong preds grouped by class (only targets)
    preds_by_cls: Dict[int, List[Dict]] = {cid: [] for cid in target_ids}
    for p in preds:
        cid = int(p["cls"])
        if cid not in target_ids:
            continue
        if float(p["conf"]) < conf_clean:
            continue
        if not box_is_clean_xyxy(p["xyxy"], w, h, min_wh_px=min_wh_px):
            continue
        preds_by_cls[cid].append(p)

    qualified: List[int] = []

    for cid in target_ids:
        gt_list = gt_by_cls.get(cid, [])
        if not gt_list:
            continue
        if not preds_by_cls[cid]:
            continue

        # Greedy: sort preds by conf desc, match to best unmatched GT by IoU
        preds_sorted = sorted(preds_by_cls[cid], key=lambda d: float(d["conf"]), reverse=True)

        ok = False
        for p in preds_sorted:
            best_j = None
            best_iou = 0.0
            for j, gt in enumerate(gt_list):
                if gt["matched"]:
                    continue
                v = iou_xyxy(p["xyxy"], gt["box"])
                if v > best_iou:
                    best_iou = v
                    best_j = j
            if best_j is not None and best_iou >= iou_min:
                gt_list[best_j]["matched"] = True
                ok = True
                break

        if ok:
            qualified.append(cid)

    return qualified

def ensure_dirs(outdir: Path, class_name: str):
    cdir = outdir / safe_name(class_name)
    (cdir / "originals").mkdir(parents=True, exist_ok=True)
    (cdir / "annotated").mkdir(parents=True, exist_ok=True)
    return cdir

# -----------------------------
# Main
# -----------------------------

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-yaml", type=str, default=r"wind-combined-2\data_8class_oversampled_max.yaml")
    ap.add_argument("--weights", type=str, default=None)
    ap.add_argument("--split", type=str, default="val", help="val/valid/test per dataset yaml")
    ap.add_argument("--outdir", type=str, default="demo_images")

    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--conf", type=float, default=0.5, help="Inference conf (predict_detections)")
    ap.add_argument("--iou", type=float, default=0.7, help="Inference NMS IoU (predict_detections)")

    ap.add_argument("--conf-clean", type=float, default=0.45, help="Clean-box minimum conf")
    ap.add_argument("--iou-min", type=float, default=0.50, help="IoU vs GT to consider 'correct'")

    ap.add_argument("--max-total-boxes", type=int, default=8)
    ap.add_argument("--max-non-target-strong", type=int, default=2)
    ap.add_argument("--min-wh-px", type=int, default=24)

    ap.add_argument("--per-class", type=int, default=4, help="Target minimum examples per class (goal)")
    ap.add_argument("--max-per-class", type=int, default=40, help="Hard cap per class")
    ap.add_argument("--limit", type=int, default=None, help="Only scan first N images")

    ap.add_argument(
        "--targets",
        nargs="+",
        default=[
            "Surface Crack",
            "le-erosion",
            "Lightning Strike",
            "OIL LEAKAGE",
        ],
        help="Target class names (must map to CLASS_NAMES).",
    )
    return ap.parse_args()

def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    outdir = (repo_root / args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    weights = args.weights or auto_find_best_pt(preferred_path=repo_root / "best.pt", filename="best.pt", search_root=repo_root)

    yaml_path = auto_find_data_yaml(repo_root, preferred=args.data_yaml)
    data = yaml.safe_load(Path(yaml_path).read_text(encoding="utf-8"))
    base = resolve_dataset_base(Path(yaml_path), data)

    # resolve split key exactly like in YAML
    split_key = args.split
    if split_key not in data:
        # common fallback
        if split_key == "valid" and "val" in data:
            split_key = "val"
        elif split_key == "val" and "valid" in data:
            split_key = "valid"
        else:
            raise RuntimeError(f"Split '{args.split}' not found in dataset yaml keys: {list(data.keys())}")

    split_value = data[split_key]
    split_path = (base / split_value).resolve() if not Path(split_value).is_absolute() else Path(split_value).resolve()

    image_paths = list_images_from_yaml_split(Path(yaml_path), str(split_path))
    if args.limit is not None and args.limit > 0:
        image_paths = image_paths[: args.limit]

    # map targets to class IDs
    target_map = resolve_target_class_ids(args.targets)  # {cid: name}
    target_ids = sorted(target_map.keys())

    # prepare output dirs and counters
    counts: Dict[int, int] = {cid: 0 for cid in target_ids}
    summary_rows = []

    for img_path in tqdm(image_paths, desc=f"Scanning {split_key}"):
        # stop if everyone hit max-per-class
        if all(counts[cid] >= args.max_per_class for cid in target_ids):
            break

        frame = cv2.imread(str(img_path))
        if frame is None:
            continue
        h, w = frame.shape[:2]

        # preds
        preds = predict_detections(
            frame,
            model_path=weights,
            imgsz=int(args.imgsz),
            conf=float(args.conf),
            iou=float(args.iou),
        )

        if not preds:
            continue

        # GT
        lbl_path = image_to_label_path(img_path)
        gts = yolo_txt_to_xyxy(lbl_path, w, h)

        # find which target classes this image qualifies for
        qualified = image_passes_for_targets(
            img_path=img_path,
            preds=preds,
            gts=gts,
            target_ids=target_ids,
            conf_clean=float(args.conf_clean),
            iou_min=float(args.iou_min),
            max_total_boxes=int(args.max_total_boxes),
            max_non_target_strong=int(args.max_non_target_strong),
            min_wh_px=int(args.min_wh_px),
        )
        if not qualified:
            continue

        # compute annotated once (RGB), then reuse
        ann_rgb, ann_summary = predict(
            frame,
            model_path=weights,
            imgsz=int(args.imgsz),
            conf=float(args.conf),
            iou=float(args.iou),
        )
        ann_bgr = ann_rgb[:, :, ::-1]

        for cid in qualified:
            if counts[cid] >= args.max_per_class:
                continue

            cname = target_map[cid]
            cdir = ensure_dirs(outdir, cname)

            # copy original
            dst_orig = cdir / "originals" / img_path.name
            if not dst_orig.exists():
                shutil.copy2(img_path, dst_orig)

            # save annotated
            dst_ann = cdir / "annotated" / f"{img_path.stem}_ann.jpg"
            if not dst_ann.exists():
                cv2.imwrite(str(dst_ann), ann_bgr)

            counts[cid] += 1

            summary_rows.append({
                "class_id": cid,
                "class_name": cname,
                "image": str(img_path),
                "saved_original": str(dst_orig),
                "saved_annotated": str(dst_ann),
                "conf_clean": float(args.conf_clean),
                "iou_min": float(args.iou_min),
            })

        # optional early exit: once each class has at least --per-class (goal)
        if all(counts[cid] >= args.per_class for cid in target_ids):
            # keep scanning to collect "as many additional" unless you want to stop.
            # If you DO want to stop here, uncomment next line:
            # break
            pass

    # write summary.csv
    summary_csv = outdir / "summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["class_id","class_name","image","saved_original","saved_annotated","conf_clean","iou_min"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in summary_rows:
            w.writerow(r)

    print("\nDone.")
    print("Weights:", weights)
    print("Dataset YAML:", yaml_path)
    print("Split:", split_key, "=>", split_path)
    print("Output:", outdir)
    print("Counts:")
    for cid in target_ids:
        print(f"  {target_map[cid]} ({cid}): {counts[cid]}")
    print("Summary:", summary_csv)

if __name__ == "__main__":
    main()
