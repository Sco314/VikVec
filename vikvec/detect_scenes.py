from pathlib import Path

import cv2
import numpy as np


def detect_scene_islands(input_path, background="white", threshold=245, min_area=500, padding=10):
    """Detect large connected scene islands in an image using OpenCV."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    image = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Unable to read image: {source}")

    if image.ndim == 2:
        gray = image
        alpha = None
    elif image.shape[2] >= 3:
        gray = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)
        alpha = image[:, :, 3] if image.shape[2] == 4 else None

    if background.lower() == "white":
        if alpha is not None:
            mask = (alpha > 0) & (gray < threshold)
        else:
            mask = gray < threshold
    else:
        if alpha is not None:
            mask = (alpha > 0) & (gray > threshold)
        else:
            mask = gray > threshold

    mask = mask.astype(np.uint8)
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)

    boxes = []
    for label in range(1, num_labels):
        x, y, w, h, area = [int(value) for value in stats[label]]
        if area < min_area:
            continue

        candidate = [max(0, x - padding), max(0, y - padding), w + padding * 2, h + padding * 2]
        merged = False
        for item in boxes:
            bx, by, bw, bh = item["bbox"]
            overlap_w = max(0, min(candidate[0] + candidate[2], bx + bw) - max(candidate[0], bx))
            overlap_h = max(0, min(candidate[1] + candidate[3], by + bh) - max(candidate[1], by))
            overlap_area = overlap_w * overlap_h
            if overlap_area > 0:
                smaller_area = min(candidate[2] * candidate[3], bw * bh)
                if overlap_area >= smaller_area * 0.35:
                    item["bbox"] = [
                        min(candidate[0], bx),
                        min(candidate[1], by),
                        max(candidate[0] + candidate[2], bx + bw) - min(candidate[0], bx),
                        max(candidate[1] + candidate[3], by + bh) - min(candidate[1], by),
                    ]
                    item["area"] = item["bbox"][2] * item["bbox"][3]
                    merged = True
                    break

        if not merged:
            boxes.append(
                {
                    "bbox": candidate,
                    "area": area,
                    "asset_name_suggestion": f"scene_candidate_{len(boxes) + 1:02d}",
                    "quality_status": "detected_candidate",
                }
            )

    final_boxes = []
    for index, item in enumerate(boxes, start=1):
        x, y, w, h = [max(0, int(value)) for value in item["bbox"]]
        w = min(image.shape[1], max(1, w))
        h = min(image.shape[0], max(1, h))
        final_boxes.append(
            {
                "bbox": [x, y, w, h],
                "area": w * h,
                "asset_name_suggestion": f"scene_candidate_{index:02d}",
                "quality_status": "detected_candidate",
            }
        )

    return final_boxes
