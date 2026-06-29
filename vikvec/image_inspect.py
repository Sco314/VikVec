from pathlib import Path

from PIL import Image


def inspect_image(image_path: str | Path) -> dict:
    """Return a small summary of an image file."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file was not found: {path}")

    with Image.open(path) as image:
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "file_size": path.stat().st_size,
            "has_alpha": "A" in image.getbands(),
        }
