from pathlib import Path

from PIL import Image

from vikvec.mask import apply_mask_file, apply_polygon_mask


def test_apply_polygon_mask_makes_parts_transparent(tmp_path: Path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGBA", (200, 200), (10, 20, 30, 255))
    image.save(input_path)

    polygon = [(20, 20), (180, 20), (180, 180), (20, 180)]
    apply_polygon_mask(input_path, output_path, polygon)

    with Image.open(output_path) as result:
        alpha = result.getchannel("A")
        assert result.mode == "RGBA"
        assert alpha.getpixel((10, 10)) == 0
        assert alpha.getpixel((100, 100)) > 0


def test_apply_mask_file_uses_mask_as_alpha(tmp_path: Path) -> None:
    input_path = tmp_path / "input.png"
    mask_path = tmp_path / "mask.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    image.save(input_path)

    mask = Image.new("L", (100, 100), 0)
    mask.putpixel((50, 50), 255)
    mask.save(mask_path)

    apply_mask_file(input_path, mask_path, output_path)

    with Image.open(output_path) as result:
        assert result.mode == "RGBA"
        assert result.getchannel("A").getpixel((50, 50)) == 255
        assert result.getchannel("A").getpixel((0, 0)) == 0
