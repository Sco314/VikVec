# Spike: labelme_polygon - first controlled test

## Constraint

Do not install LabelMe, SAM, SAM2, PyTorch, Stable Diffusion, LaMa, model checkpoints, or external repos for this documentation step. This spike only defines the first manual polygon workflow test and expected VikVec manifest mapping.

## Question

Can a LabelMe-style polygon annotation workflow create a clean mask around the process/tank scene and export data that VikVec can use?

## Test image

- `input/reference_scene.png`

## Target asset

- `scene_process_tanks_iso_01`

## Expected manual annotation

- Draw one polygon around only the tank/process scene.
- Exclude neighboring fragments and unrelated scene pieces.
- Use the polygon as the authoritative shape for the asset, with the bbox retained only as candidate/context metadata.

## Expected outputs

- LabelMe JSON annotation.
- Polygon points for `scene_process_tanks_iso_01`.
- `mask_file` path or a manifest `polygon` field that can be rendered into a mask.
- `final_output_file` transparent PNG path later, after mask application is tested.
- Manifest entry later, using the fields shown in `example_manifest_entry.json`.

## Expected VikVec mapping

- `asset_name`: `scene_process_tanks_iso_01`
- `extraction_method`: `labelme_polygon`
- `mask_type`: `polygon`
- `polygon`: polygon points extracted from LabelMe JSON
- `mask_file`: exported or generated mask PNG path
- `final_output_file`: RGBA PNG path after the mask is applied
- `review_status`: `needs_annotation`, then a later review state after testing

## Success criteria

- No neighboring scene fragments remain in the mask/final transparent PNG.
- Polygon points can be stored in the VikVec manifest.
- Output can map cleanly to:
  - `extraction_method: labelme_polygon`
  - `mask_type: polygon`
  - `polygon`
  - `mask_file`
  - `final_output_file`
  - `review_status`

## Dependency risk

Low to medium. LabelMe is lighter than SAM/SAM2 and tests the review workflow before model inference, but it may still require a desktop/PyQt setup.

## Install decision

Do not install LabelMe for this step. Actual install or UI testing requires explicit approval.

Notes
- If a full cloned repo is referenced during evaluation, record the source and license in `notes.md`.
- Keep any cloned, generated, or extracted files under `spikes/labelme_polygon/`.
- Do not modify VikVec core code during this spike.
