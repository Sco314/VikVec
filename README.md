# VikVec

VikVec is a local-first prototype for turning composite isometric training images into reusable industrial asset libraries. It focuses on simple, readable tooling that works without paid APIs or cloud services.

## What VikVec does

VikVec helps you:

- inspect an image to understand its size, mode, and alpha support
- crop regions from a composite scene into individual raster assets
- remove simple black or white backgrounds to create transparent PNGs
- build starter manifests for organizing extracted assets
- batch-crop assets described in a JSON manifest

## Raster crops vs true vector assets

A cropped PNG is a useful raster asset, but it is not the same as a clean SVG vector asset. Raster crops preserve the pixels from the source image, while true vector assets are built from shapes and layers that can be edited and scaled cleanly.

This prototype focuses on the first step: extraction. Later, cleaned SVG versions can be rebuilt from the extracted assets.

## Why auto-vectorization is not the same as clean SVG

Auto-vectorization can be helpful for rough tracing, but it does not automatically produce polished industrial SVGs. A generated outline may contain messy geometry, embedded raster artifacts, or poor layer structure. VikVec keeps the process honest by treating raster crops as extraction outputs and leaving true vector rebuilding as a later, manual or semi-manual step.

## Suggested workflow

1. Inspect the source screenshot.
2. Crop scene islands and reusable parts.
3. Remove simple backgrounds when needed.
4. Save manifest entries for each asset.
5. Rebuild high-value assets as clean SVGs later if needed.

## Commands

### Inspect an image

```bash
python -m vikvec.cli inspect input/image.png
```

### Detect scene islands

```bash
python -m vikvec.cli detect-scenes input/reference_scene.png output/manifests/detected_scenes_manifest.json
```

### Batch crop assets from a manifest

```bash
python -m vikvec.cli batch-crop input/reference_scene.png output/manifests/detected_scenes_manifest.json
```

### Create a contact sheet

```bash
python -m vikvec.cli contact-sheet output/manifests/manifest_updated.json output/contact_sheets/review.png
```

### Review report

```bash
python -m vikvec.cli review-report output/manifests/manifest_updated.json
```

### Crop an image

```bash
python -m vikvec.cli crop input/image.png output/png_assets/scene_process_tanks_iso_01.png --bbox 330 45 170 105
```

### Remove a simple background

```bash
python -m vikvec.cli remove-bg input/crop.png output/png_assets/crop_transparent.png --color black --threshold 30
```

### Create a starter manifest

```bash
python -m vikvec.cli manifest output/manifests/manifest.json
```

## Recommended workflow

1. Detect candidate scene islands from a composite screenshot.
2. Batch-crop each candidate to raw and trimmed PNG assets.
3. Review the trimmed crops with a contact sheet.
4. Use the review report to flag blank or low-content crops.

## Future optional integrations

The current prototype intentionally stays local-first. Future optional integrations may include:

- rembg for background removal
- SAM for prompted object masks
- Potrace or VTracer for rough raster-to-SVG conversion

## Documentation

Additional guidance is available in the docs folder:

- docs/style_guide.md
- docs/asset_taxonomy.md
- docs/naming_rules.md
- docs/extraction_rules.md
- docs/vector_rebuild_rules.md
