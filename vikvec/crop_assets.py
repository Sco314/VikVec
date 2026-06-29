from pathlib import Path

from PIL import Image


def crop_image(input_path: str | Path, output_path: str | Path, bbox: tuple[int, int, int, int]) -> tuple[int, int]:
    """Crop an image using x, y, width, height and save it as a PNG."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    x, y, width, height = bbox
    if width <= 0 or height <= 0:
        raise ValueError("Bounding box width and height must be greater than zero")

    with Image.open(source) as image:
        cropped = image.crop((x, y, x + width, y + height))
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(target, format="PNG")
        return cropped.size
