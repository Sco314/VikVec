from pathlib import Path

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
        pixels = []
        for red, green, blue, alpha in rgba.getdata():
            if color_name == "black" and (red <= threshold and green <= threshold and blue <= threshold):
                alpha = 0
            elif color_name == "white" and (red >= 255 - threshold and green >= 255 - threshold and blue >= 255 - threshold):
                alpha = 0
            pixels.append((red, green, blue, alpha))

        rgba.putdata(pixels)
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        rgba.save(target, format="PNG")
        return target
