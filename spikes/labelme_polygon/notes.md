# Notes: labelme_polygon spike - first controlled test

## Purpose

Track the plan and later findings for validating whether a LabelMe-style polygon annotation workflow can produce clean mask data for VikVec before testing heavier model-backed inference.

## Test contract

- Test image: `input/reference_scene.png`
- Target asset: `scene_process_tanks_iso_01`
- Core question: Can a LabelMe-style polygon annotation workflow create a clean mask around the process/tank scene and export data that VikVec can use?
- Expected manual annotation: one polygon around only the tank/process scene, excluding neighboring fragments.
- Initial manifest example: `spikes/labelme_polygon/example_manifest_entry.json`

## Planned steps (do not install anything yet)

1. Confirm `input/reference_scene.png` is present.
2. After explicit approval, install/run LabelMe locally.
3. Open `input/reference_scene.png` in LabelMe.
4. Draw a polygon around `scene_process_tanks_iso_01`, excluding neighboring fragments and unrelated scene pieces.
5. Save the LabelMe JSON annotation under `spikes/labelme_polygon/outputs/`.
6. Record the polygon points from the LabelMe JSON.
7. Export a mask PNG if LabelMe supports it in the approved local setup; otherwise plan a small spike-only JSON-to-mask conversion helper later.
8. Later, apply the mask to produce a transparent PNG and record the `final_output_file` path.
9. Later, update the manifest entry fields once real outputs exist.

## Expected outputs

- LabelMe JSON annotation.
- Polygon points for the target asset.
- `mask_file` or `polygon` field.
- `final_output_file` transparent PNG path later.
- Manifest entry later.

## Checklist for each run

- Input present: `input/reference_scene.png`
- Polygon JSON exported.
- Polygon points verified.
- Mask PNG present, either exported or generated later.
- `final_output_file` RGBA produced later.
- Visual review confirms no neighboring scene fragments remain.
- Manifest mapping verified for `extraction_method`, `mask_type`, `polygon`, `mask_file`, `final_output_file`, and `review_status`.

## VikVec manifest mapping

```
{
  "asset_name": "scene_process_tanks_iso_01",
  "extraction_method": "labelme_polygon",
  "mask_type": "polygon",
  "polygon": [],
  "mask_file": "spikes/labelme_polygon/outputs/scene_process_tanks_iso_01_mask.png",
  "final_output_file": "spikes/labelme_polygon/outputs/scene_process_tanks_iso_01.png",
  "review_status": "needs_annotation"
}
```

## Success criteria

- No neighboring scene fragments remain.
- Polygon points can be stored in the VikVec manifest.
- Output can map to:
  - `extraction_method: labelme_polygon`
  - `mask_type: polygon`
  - `polygon`
  - `mask_file`
  - `final_output_file`
  - `review_status`

## Dependency risk

Low to medium. LabelMe is lighter than SAM/SAM2 and tests the review workflow before model inference, but it can still involve Python desktop UI dependencies such as PyQt.

## Recordkeeping

- Save screenshots, exported JSON, generated mask PNG, and final RGBA in `spikes/labelme_polygon/outputs/` with timestamps.
- Do not modify VikVec core code as part of this spike.
- Do not install SAM/SAM2, torch, Stable Diffusion, LaMa, or checkpoints.

## Next action after approval

Install and run LabelMe locally, then annotate `input/reference_scene.png` and save the JSON output under `spikes/labelme_polygon/outputs/`.
