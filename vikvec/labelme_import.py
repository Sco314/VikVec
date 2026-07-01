import json
import math
from pathlib import Path

from .manifest import build_manifest


def polygon_bbox(points: list[list[float]]) -> list[int]:
    """Return a VikVec bbox [x, y, width, height] that encloses polygon points."""
    if not points:
        raise ValueError("Polygon must contain at least one point")

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x = math.floor(min(xs))
    min_y = math.floor(min(ys))
    max_x = math.ceil(max(xs))
    max_y = math.ceil(max(ys))
    return [min_x, min_y, max_x - min_x, max_y - min_y]


def load_labelme_manifest(labelme_json_path: str | Path) -> dict:
    """Convert a LabelMe JSON annotation into a VikVec manifest dictionary."""
    path = Path(labelme_json_path)
    if not path.exists():
        raise FileNotFoundError(f"LabelMe JSON file was not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        labelme_data = json.load(handle)

    source_file = labelme_data.get("imagePath")
    image_height = labelme_data.get("imageHeight")
    image_width = labelme_data.get("imageWidth")
    shapes = labelme_data.get("shapes", [])

    if not source_file:
        raise ValueError("LabelMe JSON is missing imagePath")
    if image_height is None or image_width is None:
        raise ValueError("LabelMe JSON is missing imageHeight or imageWidth")
    if not shapes:
        raise ValueError("LabelMe JSON does not contain any shapes")

    assets = []
    for shape in shapes:
        asset_name = shape.get("label")
        polygon = shape.get("points")
        if not asset_name:
            raise ValueError("LabelMe shape is missing label")
        if not polygon:
            raise ValueError(f"LabelMe shape {asset_name} is missing points")

        assets.append(
            {
                "asset_name": asset_name,
                "asset_type": "scene",
                "source_file": source_file,
                "image_width": image_width,
                "image_height": image_height,
                "bbox": polygon_bbox(polygon),
                "extraction_method": "labelme_polygon",
                "mask_type": "polygon",
                "polygon": polygon,
                "mask_file": None,
                "final_output_file": f"output/png_assets/final/{asset_name}.png",
                "review_status": "needs_visual_review",
                "animation_role": "static_background",
                "movable": False,
                "layer_order": 10,
                "notes": "Imported from LabelMe polygon annotation.",
            }
        )

    return build_manifest(project_name="VikVec LabelMe import", assets=assets)
