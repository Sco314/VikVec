# Repo Survey: Mask-first tooling for VikVec

## Overview

VikVec is currently a manifest-driven, local-first asset extraction workflow. The existing pipeline is heavily rectangle/bbox-centered: detection emits bounding boxes, the CLI crops rectangles, and downstream steps operate on those crops. This has practical limitations — rectangular crops often include neighboring scene fragments that should be excluded.

The strategic direction is mask-first, not manual-first. LabelMe proved the data path, but the production target is automated/scriptable candidate masks plus human correction only for failures.

## Problem statement

The `final_review.png` contact-sheet commonly shows neighboring scene fragments inside trimmed assets because rectangular bboxes are not an adequate final representation for irregular objects. The recommended architectural shift is: make masks the central abstraction (mask-first), and keep bboxes only as a fast candidate detection step.

## Tool / repo comparison

The following table compares repositories and concepts relevant to a mask-first migration.

| Tool / Repo | What problem it solves | Input | Output | Dependencies | Helps VikVec now? | Role (backend/dependency/inspiration) | Risks |
|---|---|---|---|---:|---|---|---|
| osam | Headless/scriptable SAM-family point/box prompted masks; installed by LabelMe 6.3.1 | Image + prompt JSON/API calls | Masks, boxes, JSON responses, visualizations | onnxruntime, model blobs | Yes — immediate headless probe | Candidate automated backend | Cache/model placement must stay spike-local; prompted not automatic |
| facebookresearch/segment-anything (SAM) | Promptable segmentation; produces high-quality masks from points/boxes | Image + prompts (points/boxes) | Masks (PNG, RLE, numpy) | PyTorch, heavy model weights | Not yet (heavy install) | Future backend | Heavy deps, checkpoints, infra cost |
| facebookresearch/sam2 | Promptable segmentation for images (and video-friendly variants), plus possible automatic-mask workflows | Image (+ prompts); may support video frames | Masks per-frame, improved inter-frame consistency | PyTorch, model weights | Not yet | Future automated/promptable backend | Same as SAM; added complexity for videos |
| segment-anything-annotator | Annotation UI combining LabelMe-like editor with SAM masks | Images; point/box prompts; human edits | Masks, polygons, labels, exportable annotations | Web UI stack (js), optional SAM backend | Maybe — useful if parts can be scripted or used for correction UI | Correction UI / reusable pattern | GUI-only workflows are less central now |
| MrSyee/SAM-remove-background | Scriptable or click-to-mask transparent cutout flow | Image + click/box prompt | Transparent PNG (alpha), masks | SAM (PyTorch), script glue | Conceptually useful | Scriptable cutout spike candidate | Depends on SAM; may reproduce heavy deps |
| wkentaro/labelme | Manual polygon annotation tool with export | Image + human polygon annotations | Polygons, JSON annotations | Python, PyQt (desktop) | Yes — proven correction/review fallback | Tool for manual correction only | Manual work; not automated; UI dependency |
| Grounded-Segment-Anything | Text-driven detection + SAM masks | Image + text query | Masks for textual queries (e.g., 'worker') | SAM + grounding model (extra deps) | Later | Future backend for text-driven detection | Extra ML components; ambiguity in text queries |
| Inpaint-Anything (pattern) | Mask-driven inpainting, erase/replace workflows | Mask + image (+ prompt) | Inpainted image, cleaned background | Diffusion/inpainting tools (optional) | Later | Inspiration for cleanup/compositing backends | Heavy models if used; optional only |
| sam2vec (concept) | Mask-first → vector-second (mask to SVG) | Mask / contour | SVG path / simplified vector | Tracing libraries, svg helpers | Later | Inspiration for mask→SVG pipeline | Lossy vectorization; UX complexity |
| Sketch2Motion (concept) | SVG path-reveal animation techniques | SVG paths | Animated previews (MP4/GIF) | SVG animation libs | No — future animation stage | Inspiration for animation | Not for detection/extraction |

## Framing and recommendations from the survey

- Treat `osam` as the immediate headless/scriptable probe because it is already installed through LabelMe and can expose SAM-family prompted-mask workflows.
- Treat SAM / SAM2 as important backend engines, especially for automatic mask generation or point/box prompt APIs, but keep them isolated from core dependencies.
- Treat LabelMe as the proven correction/review fallback, not the main automated extractor.
- Treat `segment-anything-annotator` as useful if it exposes reusable SAM-assisted annotation patterns or correction UI; GUI-only extraction is lower priority.
- Use `SAM-remove-background` patterns if they expose scriptable mask/cutout generation.
- Keep Grounded-SAM for later text-prompt object detection/segmentation.
- Keep Inpaint-Anything, sam2vec, and Sketch2Motion as later cleanup, vectorization, and animation inspirations.

## Mapping to VikVec manifest fields

- `mask_file`: natural output for any segmentation backend or annotation tool.
- `polygon`: exported polygon lists from LabelMe or annotator UIs map directly to `mask_type: polygon`.
- `final_output_file`: result of applying a mask (alpha PNG) or running a cleanup backend.

## Short conclusion

The immediate practical investment is automated/scriptable candidate mask generation that can feed manifest entries, transparent PNG finalization, and contact sheet QA. LabelMe remains the fallback correction path for masks that fail review.
