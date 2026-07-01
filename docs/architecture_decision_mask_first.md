# Architecture decision: Make VikVec Mask-First

## Decision summary

VikVec will adopt a mask-first architecture: masks (alpha channels or polygons) are the primary extraction representation. Bounding boxes remain useful as a fast candidate detector, but they are not the final asset representation. The primary motivation is that rectangular crops frequently include neighboring scene fragments that should be excluded from final assets.

## Why change: practical symptom

- Observed symptom: contact sheets (`final_review.png`) often show neighboring fragments inside cropped assets.
- Root cause: the pipeline treats bounding boxes as final outputs, which is brittle for irregular shapes.

## Core VikVec abstractions (unchanging)

- `manifest` — single source of truth for project, assets, and review state.
- `asset_name` and naming rules — deterministic, human-friendly names.
- `review/contact sheets` — visualization and human review tools.
- `final_output_file` — the canonical transparent PNG for downstream use.
- `animation metadata` — future fields for motion/assembly.

## New central abstraction

- `mask` — an alpha mask or polygon describing exact object shape. All backends should be able to produce or accept a `mask_file` that maps to manifest entries.
- `extraction_method` should include mask-first types: `mask_file`, `polygon`, `sam_point`, `sam_box`, `auto_foreground`.

## Recommended backend taxonomy

- `opencv_foreground`: lightweight default for simple white-sheet extraction (current `auto_foreground`).
- `labelme_polygon`: manual correction and polygon-export fallback for review.
- `sam_point` / `sam_box`: optional future SAM-backed prompt segmentation.
- `sam2_point` / `sam2_box`: future image/video segmentation backends.
- `grounded_sam_text`: optional text-prompt driven finder for domain concepts.
- `rembg`: optional background removal backend for difficult cases.
- `inpaint_remove`: optional cleanup/compositing backend for final artifacts.
- `mask_to_svg`: optional mask→vector conversion pipeline (sam2vec-style).
- `svg_path_reveal`: optional animation backend for path reveals.

## Dataflow (mask-first)

1. Candidate detection: quick bbox detection (OpenCV) → candidate list in manifest.
2. Mask generation: preferred path — generate mask (auto or prompted) for candidate area.
3. Mask refinement: manual polygon edits or small morphology ops (dilate/erode).
4. Trim/compose: crop around mask tight bounds; apply mask to produce trimmed `final_output_file` (RGBA) and `mask_file`.
5. Review: contact sheets should composite final `final_output_file` images (alpha-aware) and show mask overlays.

## Implementation guidance & constraints

- Preserve the manifest schema and add clear `mask_file` and `polygon` mapping.
- Keep bboxes as candidate detectors only — don't treat `trimmed_output_file` from a bbox crop as a final asset unless it has been masked/refined.
- Prefer small, dependency-light utilities early: mask dilation, erosion, overlay visualizer, contour-to-SVG helper.
- Do not install heavy ML dependencies (PyTorch/SAM) or download model checkpoints yet. Evaluate in isolated spikes per the spike policy.

## Explicit recommendation

- Stop investing effort in bbox-only cleanup. Make masks the central abstraction for extraction and review.
- Use LabelMe-style polygon editing or an annotator that supports SAM masks for review UX.
- Keep backends optional and pluggable; the manifest and review flow remain the durable contract.
