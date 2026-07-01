import argparse
import json
import sys
from pathlib import Path
from shutil import copy2

from .labelme_import import load_labelme_manifest
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

    apply_mask_parser = subparsers.add_parser("apply-mask", help="Apply a polygon or mask-file mask to an image")
    apply_mask_parser.add_argument("input_path")
    apply_mask_parser.add_argument("output_path")
    apply_mask_parser.add_argument("--polygon", help="Polygon points as 'x1,y1 x2,y2 x3,y3'")
    apply_mask_parser.add_argument("--mask-file", help="Path to a PNG mask image")

    finalize_assets_parser = subparsers.add_parser("finalize-assets", help="Finalize assets from a manifest")
    finalize_assets_parser.add_argument("manifest_path")

    contact_sheet_parser = subparsers.add_parser("contact-sheet", help="Create a contact sheet from trimmed assets")
    contact_sheet_parser.add_argument("manifest_path")
    contact_sheet_parser.add_argument("output_path")

    review_report_parser = subparsers.add_parser("review-report", help="Summarize review status for a manifest")
    review_report_parser.add_argument("manifest_path")

    import_labelme_parser = subparsers.add_parser("import-labelme", help="Import LabelMe polygons into a manifest")
    import_labelme_parser.add_argument("input_json")
    import_labelme_parser.add_argument("output_manifest_json")

    return parser


def resolve_manifest_path(raw_path: str | Path, manifest_path: str | Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or path.exists():
        return path

    manifest_relative = Path(manifest_path).parent / path
    if manifest_relative.exists():
        return manifest_relative

    if "input" in path.parts:
        input_index = path.parts.index("input")
        repo_relative = Path(*path.parts[input_index:])
        if repo_relative.exists():
            return repo_relative

    return path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "inspect":
            from .image_inspect import inspect_image

            result = inspect_image(args.image_path)
            print(f"width: {result['width']}")
            print(f"height: {result['height']}")
            print(f"mode: {result['mode']}")
            print(f"file_size: {result['file_size']}")
            print(f"has_alpha: {result['has_alpha']}")

        elif args.command == "crop":
            from .crop_assets import crop_image

            size = crop_image(args.input_path, args.output_path, tuple(args.bbox))
            print(f"output_path: {Path(args.output_path).resolve()}")
            print(f"crop_size: {size[0]}x{size[1]}")

        elif args.command == "remove-bg":
            from .background import remove_background

            output = remove_background(args.input_path, args.output_path, color=args.color, threshold=args.threshold)
            print(f"output_path: {output.resolve()}")
            print("background_removed: true")

        elif args.command == "manifest":
            manifest = build_manifest(project_name="VikVec")
            output = write_manifest(manifest, args.output_path)
            print(f"manifest_written: {output.resolve()}")

        elif args.command == "detect-scenes":
            from .detect_scenes import detect_scene_islands

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

                from .crop_assets import crop_image
                from PIL import Image

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

        elif args.command == "apply-mask":
            from .mask import apply_mask_file, apply_polygon_mask

            if args.polygon and args.mask_file:
                raise ValueError("Choose either --polygon or --mask-file, not both")
            if args.polygon:
                points = []
                for token in args.polygon.split():
                    if "," not in token:
                        raise ValueError(f"Invalid point token: {token}")
                    x_text, y_text = token.split(",", 1)
                    points.append((int(x_text), int(y_text)))
                output = apply_polygon_mask(args.input_path, args.output_path, points)
            elif args.mask_file:
                output = apply_mask_file(args.input_path, args.mask_file, args.output_path)
            else:
                raise ValueError("Provide --polygon or --mask-file")
            print(f"output_path: {output.resolve()}")

        elif args.command == "finalize-assets":
            manifest = load_manifest(args.manifest_path)
            assets = manifest.get("assets", [])
            if not assets:
                raise ValueError("The manifest does not contain any assets to process")

            output_dir = Path("output/png_assets/final")
            output_dir.mkdir(parents=True, exist_ok=True)
            updated_assets = []

            for asset in assets:
                from .mask import apply_mask_file, apply_polygon_mask, apply_source_polygon_mask

                source_rel = (
                    asset.get("source_file")
                    if asset.get("extraction_method") == "labelme_polygon"
                    else asset.get("trimmed_output_file") or asset.get("raw_output_file") or asset.get("output_file")
                )
                if not source_rel:
                    raise ValueError(f"Asset {asset.get('asset_name', 'unknown')} is missing an input file")

                source_path = resolve_manifest_path(source_rel, args.manifest_path)
                if not source_path.exists():
                    raise FileNotFoundError(f"Input asset file was not found: {source_path}")

                final_output_file = asset.get("final_output_file")
                if final_output_file:
                    final_path = Path(final_output_file)
                    final_name = final_path.name
                else:
                    final_name = Path(source_rel).name
                    final_path = output_dir / final_name
                mask_type = asset.get("mask_type", "bbox")

                if asset.get("extraction_method") == "labelme_polygon" and mask_type == "polygon":
                    polygon = asset.get("polygon", [])
                    if not polygon:
                        raise ValueError(f"Asset {asset.get('asset_name', 'unknown')} is missing polygon points")
                    apply_source_polygon_mask(source_path, final_path, polygon)
                elif mask_type == "polygon":
                    polygon = asset.get("polygon", [])
                    if not polygon:
                        raise ValueError(f"Asset {asset.get('asset_name', 'unknown')} is missing polygon points")
                    apply_polygon_mask(source_path, final_path, polygon)
                elif mask_type == "mask_file":
                    mask_file = asset.get("mask_file")
                    if not mask_file:
                        raise ValueError(f"Asset {asset.get('asset_name', 'unknown')} is missing mask_file")
                    apply_mask_file(source_path, mask_file, final_path)
                else:
                    copy2(source_path, final_path)

                asset_record = dict(asset)
                asset_record["final_output_file"] = str(final_path)
                asset_record["review_status"] = "final_needs_visual_review"
                updated_assets.append(asset_record)

            updated_manifest = dict(manifest)
            updated_manifest["assets"] = updated_assets
            output = write_manifest(updated_manifest, Path("output/manifests/manifest_updated.json"))
            print(f"updated_manifest: {output.resolve()}")
            print(f"processed_assets: {len(updated_assets)}")

        elif args.command == "contact-sheet":
            from PIL import Image

            manifest = load_manifest(args.manifest_path)
            assets = manifest.get("assets", [])
            if not assets:
                raise ValueError("The manifest does not contain any assets to process")

            images = []
            labels = []
            for asset in assets:
                output_path = Path(asset.get("final_output_file") or asset.get("output_file") or "")
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
                sheet.alpha_composite(resized, dest=(x, y))
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

        elif args.command == "import-labelme":
            manifest = load_labelme_manifest(args.input_json)
            output = write_manifest(manifest, args.output_manifest_json)
            print(f"manifest_written: {output.resolve()}")
            print(f"assets_imported: {len(manifest.get('assets', []))}")

        else:
            parser.print_help()

    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
