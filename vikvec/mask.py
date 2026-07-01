from pathlib import Path

from PIL import Image, ImageDraw


def polygon_bbox(points: list[tuple[float, float]] | list[list[float]]) -> tuple[int, int, int, int]:
    """Return a crop box (left, upper, right, lower) that encloses polygon points."""
    if not points:
        raise ValueError("Polygon must contain at least one point")

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left = max(0, int(min(xs)))
    upper = max(0, int(min(ys)))
    right = max(left + 1, int(max(xs)) + 1)
    lower = max(upper + 1, int(max(ys)) + 1)
    return left, upper, right, lower


def apply_polygon_mask(input_path: str | Path, output_path: str | Path, polygon: list[tuple[int, int]] | list[list[int]], coordinate_space: str = "crop") -> Path:
    """Apply a polygon-based alpha mask to an RGBA image and save the result."""
    if coordinate_space not in {"crop", "source"}:
        raise ValueError("coordinate_space must be 'crop' or 'source'")

    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    if len(polygon) < 3:
        raise ValueError("A polygon must contain at least three points")

    with Image.open(source) as image:
        rgba_image = image.convert("RGBA")
        width, height = rgba_image.size
        mask = Image.new("L", (width, height), 0)

        draw = ImageDraw.Draw(mask)
        draw.polygon([(int(x), int(y)) for x, y in polygon], fill=255)

        rgba_image.putalpha(mask)
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        rgba_image.save(target, format="PNG")
        return target


def apply_source_polygon_mask(input_path: str | Path, output_path: str | Path, polygon: list[tuple[float, float]] | list[list[float]]) -> Path:
    """Apply a source-coordinate polygon mask, crop to the polygon bbox, and save RGBA."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    if len(polygon) < 3:
        raise ValueError("A polygon must contain at least three points")

    with Image.open(source) as image:
        rgba_image = image.convert("RGBA")
        width, height = rgba_image.size
        mask = Image.new("L", (width, height), 0)

        draw = ImageDraw.Draw(mask)
        draw.polygon([(int(x), int(y)) for x, y in polygon], fill=255)

        rgba_image.putalpha(mask)
        left, upper, right, lower = polygon_bbox(polygon)
        right = min(width, right)
        lower = min(height, lower)
        cropped = rgba_image.crop((left, upper, right, lower))

        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(target, format="PNG")
        return target


def apply_mask_file(input_path: str | Path, mask_path: str | Path, output_path: str | Path) -> Path:
    """Apply a grayscale mask image as the alpha channel for an RGBA image."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input image was not found: {source}")

    mask_source = Path(mask_path)
    if not mask_source.exists():
        raise FileNotFoundError(f"Mask image was not found: {mask_source}")

    with Image.open(source) as image:
        rgba_image = image.convert("RGBA")

        with Image.open(mask_source) as mask_image:
            mask = mask_image.convert("L")
            if mask.size != rgba_image.size:
                mask = mask.resize(rgba_image.size, getattr(Image, "Resampling", Image).LANCZOS)

            rgba_image.putalpha(mask)
            target = Path(output_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            rgba_image.save(target, format="PNG")
            return target
