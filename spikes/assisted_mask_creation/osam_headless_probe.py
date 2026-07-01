from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import numpy as np
import osam
from PIL import Image
from skimage import measure


REPO_ROOT = Path(__file__).resolve().parents[2]
SPIKE_ROOT = Path(__file__).resolve().parent
INPUT_IMAGE = REPO_ROOT / "input" / "reference_scene.png"
OUTPUT_DIR = SPIKE_ROOT / "outputs" / "osam_probe"
MODEL_NAME = os.environ.get("OSAM_PROBE_MODEL", "efficientsam:10m")


PROMPTS: list[dict[str, Any]] = [
    {
        "name": "scene_process_tanks_box",
        "description": "Approximate bbox around scene_process_tanks_iso_01.",
        "points": [[302.0, 47.0], [494.0, 198.0]],
        "point_labels": [2, 3],
    },
    {
        "name": "scene_process_tanks_points",
        "description": "Foreground point on process/tank scene plus background points.",
        "points": [[405.0, 125.0], [250.0, 120.0], [480.0, 225.0]],
        "point_labels": [1, 0, 0],
    },
]


def _full_mask(annotation: osam.types.Annotation, image_shape: tuple[int, int]) -> np.ndarray:
    if annotation.mask is None or annotation.bounding_box is None:
        raise ValueError("annotation must include mask and bounding_box")
    mask = np.zeros(image_shape, dtype=bool)
    bb = annotation.bounding_box
    mask[bb.ymin : bb.ymax + 1, bb.xmin : bb.xmax + 1] = annotation.mask
    return mask


def _mask_to_polygon(mask: np.ndarray) -> list[list[float]]:
    contours = measure.find_contours(mask.astype(np.uint8), 0.5)
    if not contours:
        return []
    contour = max(contours, key=len)
    return [[float(x), float(y)] for y, x in contour]


def _save_mask(path: Path, mask: np.ndarray) -> None:
    Image.fromarray((mask.astype(np.uint8) * 255), mode="L").save(path)


def _save_cutout(path: Path, image: np.ndarray, mask: np.ndarray) -> None:
    rgba = np.zeros((*image.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = image[:, :, :3]
    rgba[:, :, 3] = mask.astype(np.uint8) * 255
    Image.fromarray(rgba, mode="RGBA").save(path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image = np.asarray(Image.open(INPUT_IMAGE).convert("RGB"))
    report: dict[str, Any] = {
        "model": MODEL_NAME,
        "input_file": str(INPUT_IMAGE.relative_to(REPO_ROOT)),
        "output_dir": str(OUTPUT_DIR.relative_to(REPO_ROOT)),
        "supports_automatic_mask_generation": False,
        "notes": [
            "osam SAM-family models are headless/scriptable for prompted masks.",
            "This probe found no automatic mask generation API in osam 0.5.0.",
        ],
        "candidates": [],
    }

    model_type = osam.apis.get_model_type_by_name(MODEL_NAME)
    if model_type.get_size() is None:
        raise RuntimeError(
            f"Model {MODEL_NAME!r} is not pulled. Run with spike-local HOME: "
            f"HOME={SPIKE_ROOT} .venv/bin/osam pull {MODEL_NAME}"
        )

    for prompt_config in PROMPTS:
        prompt = osam.types.Prompt(
            points=prompt_config["points"],
            point_labels=prompt_config["point_labels"],
        )
        response = osam.apis.generate(
            request=osam.types.GenerateRequest(
                model=MODEL_NAME,
                image=image,
                prompt=prompt,
            )
        )

        for index, annotation in enumerate(response.annotations):
            stem = f"{prompt_config['name']}_{index:02d}"
            mask = _full_mask(annotation, image.shape[:2])
            polygon = _mask_to_polygon(mask)
            mask_path = OUTPUT_DIR / f"{stem}_mask.png"
            cutout_path = OUTPUT_DIR / f"{stem}_cutout.png"
            _save_mask(mask_path, mask)
            _save_cutout(cutout_path, image, mask)

            bbox = annotation.bounding_box
            report["candidates"].append(
                {
                    "name": stem,
                    "prompt": prompt_config,
                    "bbox": None
                    if bbox is None
                    else {
                        "xmin": bbox.xmin,
                        "ymin": bbox.ymin,
                        "xmax": bbox.xmax,
                        "ymax": bbox.ymax,
                    },
                    "mask_file": str(mask_path.relative_to(REPO_ROOT)),
                    "final_output_file": str(cutout_path.relative_to(REPO_ROOT)),
                    "polygon_points": len(polygon),
                    "polygon": polygon,
                    "vikvec_mapping": {
                        "extraction_method": "osam_headless_prompt",
                        "mask_type": "mask",
                        "mask_file": str(mask_path.relative_to(REPO_ROOT)),
                        "polygon": "available_in_report",
                        "final_output_file": str(cutout_path.relative_to(REPO_ROOT)),
                        "review_status": "needs_visual_review",
                    },
                }
            )

    report_path = OUTPUT_DIR / "report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
