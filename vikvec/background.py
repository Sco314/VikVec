from pathlib import Path

import numpy as np
from PIL import Image


def remove_background(input_path: str | Path, output_path: str | Path, color: str = "black", threshold: int = 30) -> Path:
    """Make near-black or near-white pixels transparent in an image."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    if threshold < 0 or threshold > 255:
        raise ValueError("Threshold must be between 0 and 255")

    color_name = color.lower()
    if color_name not in {"black", "white"}:
        raise ValueError("Color must be either 'black' or 'white'")

    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        arr = np.array(rgba)
        red, green, blue = arr[..., 0], arr[..., 1], arr[..., 2]

        if color_name == "black":
            background = (red <= threshold) & (green <= threshold) & (blue <= threshold)
        else:
            limit = 255 - threshold
            background = (red >= limit) & (green >= limit) & (blue >= limit)

        arr[..., 3][background] = 0
        result = Image.fromarray(arr, "RGBA")

        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        result.save(target, format="PNG")
        return target


def isolate_auto_foreground(input_path: str | Path, output_path: str | Path, threshold: int = 240) -> Path:
    """Remove a light white background for white-background asset sheets.

    This is a lightweight current-backend fallback for the common case of sheet-based
    references. It can later be replaced by optional segmentation or background-removal
    backends without changing the manifest workflow.
    """

    return remove_background(input_path, output_path, color="white", threshold=threshold)
