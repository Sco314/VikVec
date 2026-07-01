from pathlib import Path

from PIL import Image

from vikvec.cli import main
from vikvec.manifest import write_manifest


def test_finalize_assets_supports_auto_foreground(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    source_path = tmp_path / "source.png"
    image = Image.new("RGBA", (40, 40), (255, 255, 255, 255))
    image.save(source_path)

    manifest_path = tmp_path / "manifest.json"
    write_manifest(
        {
            "project_name": "VikVec",
            "assets": [
                {
                    "asset_name": "sheet_item",
                    "asset_type": "industrial_object",
                    "source_file": str(source_path),
                    "bbox": [0, 0, 40, 40],
                    "trimmed_output_file": str(tmp_path / "trimmed.png"),
                    "extraction_method": "auto_foreground",
                    "mask_type": "auto_foreground",
                    "quality_status": "pending",
                    "review_status": "needs_review",
                    "notes": "Auto foreground test",
                }
            ],
        },
        manifest_path,
    )

    trimmed_path = tmp_path / "trimmed.png"
    image.save(trimmed_path)

    exit_code = main(["finalize-assets", str(manifest_path)])

    assert exit_code == 0
    final_output = tmp_path / "output" / "png_assets" / "final" / "trimmed.png"
    assert final_output.exists()

    with Image.open(final_output) as result:
        assert result.mode == "RGBA"
        assert result.getchannel("A").getpixel((0, 0)) == 0
