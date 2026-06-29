import argparse
import json
import sys
from pathlib import Path

from PIL import Image

from .background import remove_background
from .crop_assets import crop_image
from .detect_scenes import detect_scene_islands
from .image_inspect import inspect_image
from .manifest import build_manifest, load_manifest, write_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VikVec local-first asset extraction prototype")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect an image file")
    inspect_parser.add_argument("image_path")

    crop_parser = subparsers.add_parser("crop", help="Crop an image to a bounding box")
    crop_parser.add_argument("input_path")
    crop_parser.add_argument("output_path")
    crop_parser.add_argument("--bbox", nargs=4, type=int, required=True, metavar=("X", "Y", "WIDTH", "HEIGHT"))

    remove_bg_parser = subparsers.add_parser("remove-bg", help="Make background pixels transparent")
    remove_bg_parser.add_argument("input_path")
    remove_bg_parser.add_argument("output_path")
    remove_bg_parser.add_argument("--color", choices=["black", "white"], default="black")
    remove_bg_parser.add_argument("--threshold", type=int, default=30)

    manifest_parser = subparsers.add_parser("manifest", help="Create a starter manifest")
    manifest_parser.add_argument("output_path")

    detect_parser = subparsers.add_parser("detect-scenes", help="Detect scene-island candidates")
    detect_parser.add_argument("input_path")
    detect_parser.add_argument("output_manifest")

    batch_parser = subparsers.add_parser("batch-crop", help="Crop all assets listed in a manifest")
    batch_parser.add_argument("input_path")
    batch_parser.add_argument("manifest_path")

    contact_sheet_parser = subparsers.add_parser("contact-sheet", help="Create a contact sheet from trimmed assets")
    contact_sheet_parser.add_argument("manifest_path")
    contact_sheet_parser.add_argument("output_path")

    review_report_parser = subparsers.add_parser("review-report", help="Summarize review status for a manifest")
    review_report_parser.add_argument("manifest_path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "inspect":
            result = inspect_image(args.image_path)
            print(f"width: {result['width']}")
            print(f"height: {result['height']}")
            print(f"mode: {result['mode']}")
            print(f"file_size: {result['file_size']}")
            print(f"has_alpha: {result['has_alpha']}")

        elif args.command == "crop":
            size = crop_image(args.input_path, args.output_path, tuple(args.bbox))
            print(f"output_path: {Path(args.output_path).resolve()}")
            print(f"crop_size: {size[0]}x{size[1]}")

        elif args.command == "remove-bg":
            output = remove_background(args.input_path, args.output_path, color=args.color, threshold=args.threshold)
            print(f"output_path: {output.resolve()}")
            print("background_removed: true")

        elif args.command == "manifest":
            manifest = build_manifest(project_name="VikVec")
            output = write_manifest(manifest, args.output_path)
            print(f"manifest_written: {output.resolve()}")

        elif args.command == "detect-scenes":
            candidates = detect_scene_islands(args.input_path)
            assets = []
            for index, candidate in enumerate(candidates, start=1):
                output_rel = Path("output/png_assets/trimmed") / f"{candidate['asset_name_suggestion']}.png"
                assets.append(
                    {
                        "asset_name": candidate["asset_name_suggestion"],
                        "asset_type": "scene",
                        "source_file": args.input_path,
                        "bbox": candidate["bbox"],
                        "output_file": str(output_rel),
                        "quality_status": candidate["quality_status"],
                        "review_status": "needs_review",
                        "notes": "Detected candidate scene island",
                    }
                )

            manifest = build_manifest(project_name="VikVec detected scenes", assets=assets)
            output = write_manifest(manifest, args.output_manifest)
            print(f"manifest_written: {output.resolve()}")
            print(f"scene_candidates: {len(assets)}")

        elif args.command == "batch-crop":
            manifest = load_manifest(args.manifest_path)
            assets = manifest.get("assets", [])
            if not assets:
                raise ValueError("The manifest does not contain any assets to process")

            updated_assets = []
            for asset in assets:
                input_path = Path(args.input_path)
                raw_output_path = Path("output/png_assets/raw") / Path(asset["output_file"]).name
                trimmed_output_path = Path(asset["output_file"])
                bbox = tuple(asset["bbox"])

                crop_image(input_path, raw_output_path, bbox)

                with Image.open(raw_output_path) as image:
                    bbox_image = image.getbbox()
                    if bbox_image is None:
                        asset_record = dict(asset)
                        asset_record["quality_status"] = "needs_recrop"
                        asset_record["review_status"] = "rejected_blank_crop"
                        updated_assets.append(asset_record)
                        continue

                    content_image = image.crop(bbox_image)
                    trimmed_output_path.parent.mkdir(parents=True, exist_ok=True)
                    content_image.save(trimmed_output_path, format="PNG")

                asset_record = dict(asset)
                if content_image.size[0] * content_image.size[1] < 400:
                    asset_record["quality_status"] = "needs_recrop"
                    asset_record["review_status"] = "low_content"
                else:
                    asset_record["quality_status"] = "success"
                    asset_record["review_status"] = "needs_review"
                updated_assets.append(asset_record)

            updated_manifest = dict(manifest)
            updated_manifest["assets"] = updated_assets
            output = write_manifest(updated_manifest, Path("output/manifests/manifest_updated.json"))
            print(f"updated_manifest: {output.resolve()}")
            print(f"processed_assets: {len(updated_assets)}")

        elif args.command == "contact-sheet":
            manifest = load_manifest(args.manifest_path)
            assets = manifest.get("assets", [])
            if not assets:
                raise ValueError("The manifest does not contain any assets to process")

            images = []
            labels = []
            for asset in assets:
                output_path = Path(asset.get("output_file", ""))
                if output_path.exists():
                    images.append(Image.open(output_path).convert("RGBA"))
                    labels.append(asset.get("asset_name", output_path.stem))

            if not images:
                raise ValueError("No trimmed assets were found for the contact sheet")

            cols = 2
            rows = (len(images) + 1) // cols
            cell_w = 220
            cell_h = 220
            sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h + 40 * rows), (255, 255, 255, 255))

            for index, (image, label) in enumerate(zip(images, labels)):
                row = index // cols
                col = index % cols
                x = col * cell_w + 10
                y = row * cell_h + 10 + row * 40
                resized = image.resize((200, 200))
                sheet.paste(resized, (x, y))
                draw = Image.new("RGBA", sheet.size, (255, 255, 255, 0))
                from PIL import ImageDraw, ImageFont

                font = ImageFont.load_default()
                draw_text = ImageDraw.Draw(draw)
                draw_text.text((x, y + 205), label, fill=(0, 0, 0, 255), font=font)
                sheet = Image.alpha_composite(sheet, draw)

            output = Path(args.output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            sheet.save(output, format="PNG")
            print(f"contact_sheet: {output.resolve()}")

        elif args.command == "review-report":
            manifest = load_manifest(args.manifest_path)
            assets = manifest.get("assets", [])
            report = {
                "total_assets": len(assets),
                "needs_review": sum(1 for asset in assets if asset.get("review_status") == "needs_review"),
                "needs_recrop": sum(1 for asset in assets if asset.get("quality_status") == "needs_recrop"),
                "rejected_blank_crop": sum(1 for asset in assets if asset.get("review_status") == "rejected_blank_crop"),
                "low_content": sum(1 for asset in assets if asset.get("review_status") == "low_content"),
                "output_contact_sheet_path": "output/contact_sheets/review.png",
            }
            print(json.dumps(report, indent=2))

        else:
            parser.print_help()

    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
