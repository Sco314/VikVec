# VikVec

VikVec is a local-first prototype for turning composite isometric training images into reusable industrial asset libraries. It focuses on simple, readable tooling that works without paid APIs or cloud services.

## What VikVec does

VikVec helps you:

- inspect an image to understand its size, mode, and alpha support
- crop regions from a composite scene into individual raster assets
- remove simple black or white backgrounds to create transparent PNGs
- build starter manifests for organizing extracted assets
- batch-crop assets described in a JSON manifest
- apply polygon or mask-file alpha masks to keep only the intended isometric scene shape

## Raster crops vs true vector assets

A cropped PNG is a useful raster asset, but it is not the same as a clean SVG vector asset. Raster crops preserve the pixels from the source image, while true vector assets are built from shapes and layers that can be edited and scaled cleanly.

This prototype focuses on the first step: extraction. Later, cleaned SVG versions can be rebuilt from the extracted assets.

## Why auto-vectorization is not the same as clean SVG

Auto-vectorization can be helpful for rough tracing, but it does not automatically produce polished industrial SVGs. A generated outline may contain messy geometry, embedded raster artifacts, or poor layer structure. VikVec keeps the process honest by treating raster crops as extraction outputs and leaving true vector rebuilding as a later, manual or semi-manual step.

## Current direction

VikVec is moving to a mask-first asset pipeline. Bounding boxes may still be useful for rough candidate detection or crop windows, but bboxes are not the final asset boundary.

The manual LabelMe polygon spike proved the mask-first data path:

LabelMe polygon JSON -> VikVec manifest -> transparent PNG -> contact sheet review.

Mask-first does not mean manual-first. LabelMe proved the data path. The production target is automated candidate masks plus human correction only for failures.

The target workflow is:

1. Generate automated/scriptable candidate masks.
2. Write VikVec manifest entries.
3. Finalize transparent PNG outputs.
4. Review results in contact sheets.
5. Use LabelMe only to fix failed or dirty masks.
6. Reimport corrected polygon or mask annotations if needed.

LabelMe is now positioned as a fallback correction/review tool, not the intended production workflow for every asset. The next research focus is headless/scriptable mask generation, especially `osam` headless probes, SAM/SAM2 automatic mask generation, SAM-remove-background style scriptable cutout workflows, and Grounded-SAM style text-driven detection later.

## Suggested workflow

1. Inspect the source screenshot.
2. Crop scene islands and reusable parts.
3. Remove simple backgrounds when needed.
4. Save manifest entries for each asset.
5. Add polygon masks for angled scene assets when the rectangular crop includes extra fragments.
6. Finalize the asset to a transparent PNG in output/png_assets/final/.
7. Rebuild high-value assets as clean SVGs later if needed.

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

### Apply a polygon mask to a single asset

```bash
python -m vikvec.cli apply-mask output/png_assets/trimmed/scene_candidate_01.png output/png_assets/final/scene_training_room_iso_01.png --polygon "20,65 95,10 180,55 115,130"
```

### Finalize assets from a manifest

```bash
python -m vikvec.cli finalize-assets output/manifests/manual_scene_manifest.json
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
4. Edit the manifest to add polygon masks for angled scenes where the rough bounding box includes neighboring geometry.
5. Run finalize-assets to produce transparent final PNGs in output/png_assets/final/.
6. Review the final contact sheet at output/contact_sheets/final_review.png before using the assets for animation or later sub-asset extraction.

## Mask terminology

- bbox = rough rectangular crop; useful for fast isolation, but not the final visible shape
- mask = the final visible shape, expressed as an alpha channel
- polygon mask = best for isometric room or floor shapes because it follows the angled perimeter
- mask file = best for people or complex objects later when a hand-authored PNG mask is available

## Recommended sequence

A. Detect scenes
B. Crop rough boxes
C. Inspect the review contact sheet
D. Edit the manual manifest
E. Add polygon masks for angled scenes
F. Run finalize-assets
G. Inspect final_review.png
H. Only use output/png_assets/final/ for animation or sub-asset extraction

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
