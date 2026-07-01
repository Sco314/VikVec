# Repo Survey: Mask-first tooling for VikVec

## Overview

VikVec is currently a manifest-driven, local-first asset extraction workflow. The existing pipeline is heavily rectangle/bbox-centered: detection emits bounding boxes, the CLI crops rectangles, and downstream steps operate on those crops. This has practical limitations — rectangular crops often include neighboring scene fragments that should be excluded.

## Problem statement

The `final_review.png` contact-sheet commonly shows neighboring scene fragments inside trimmed assets because rectangular bboxes are not an adequate final representation for irregular objects. The recommended architectural shift is: make masks the central abstraction (mask-first), and keep bboxes only as a fast candidate detection step.

## Tool / repo comparison

The following table compares repositories and concepts relevant to a mask-first migration.

| Tool / Repo | What problem it solves | Input | Output | Dependencies | Helps VikVec now? | Role (backend/dependency/inspiration) | Risks |
|---|---|---|---|---:|---|---|---|
| facebookresearch/segment-anything (SAM) | Promptable segmentation; produces high-quality masks from points/boxes | Image + prompts (points/boxes) | Masks (PNG, RLE, numpy) | PyTorch, heavy model weights | Not yet (heavy install) | Future backend | Heavy deps, checkpoints, infra cost |
| facebookresearch/sam2 | Promptable segmentation for images (and video-friendly variants) | Image (+ prompts); may support video frames | Masks per-frame, improved inter-frame consistency | PyTorch, model weights | Not yet | Future backend for images/videos | Same as SAM; added complexity for videos |
| segment-anything-annotator | Annotation UI combining LabelMe-like editor with SAM masks | Images; point/box prompts; human edits | Masks, polygons, labels, exportable annotations | Web UI stack (js), optional SAM backend | Yes — workflow inspiration | UI integration complexity; needs lightweight hosting |
| MrSyee/SAM-remove-background | Click-to-mask then produce transparent object | Image + click prompt | Transparent PNG (alpha) | SAM (PyTorch), script glue | Conceptually useful | Inspiration / spike candidate | Depends on SAM; may reproduce heavy deps |
| wkentaro/labelme | Manual polygon annotation tool with export | Image + human polygon annotations | Polygons, JSON annotations | Python, PyQt (desktop) | Yes — immediate review fallback | Dependency / tool for manual correction | Manual work; not automated; UI dependency |
| Grounded-Segment-Anything | Text-driven detection + SAM masks | Image + text query | Masks for textual queries (e.g., 'worker') | SAM + grounding model (extra deps) | Not yet | Future backend (text-driven) | Extra ML components; ambiguity in text queries |
| Inpaint-Anything (pattern) | Mask-driven inpainting, erase/replace workflows | Mask + image (+ prompt) | Inpainted image, cleaned background | Diffusion/inpainting tools (optional) | No — inspiration for cleanup | Inspiration for cleanup/compositing backends | Heavy models if used; optional only |
| sam2vec (concept) | Mask-first → vector-second (mask to SVG) | Mask / contour | SVG path / simplified vector | Tracing libraries, svg helpers | No — future idea | Inspiration for mask→SVG pipeline | Lossy vectorization; UX complexity |
| Sketch2Motion (concept) | SVG path-reveal animation techniques | SVG paths | Animated previews (MP4/GIF) | SVG animation libs | No — future animation stage | Inspiration for animation | Not for detection/extraction |

## Framing and recommendations from the survey

- Treat SAM / SAM2 as optional future segmentation backends — powerful, but heavy. Do not add them to core dependencies now.
- LabelMe and `segment-anything-annotator` are the closest fits for the review/correction workflow: they provide polygons, editing, and exporting annotations that map cleanly to `mask_file` and polygon manifest fields.
- Use `SAM-remove-background` patterns as conceptual examples for producing transparent final objects from masks, but avoid installing SAM yet.
- Inpaint-Anything, sam2vec, and Sketch2Motion are important inspirations for later cleanup, vectorization, and animation stages — do not treat them as immediate dependencies.

## Mapping to VikVec manifest fields

- `mask_file`: natural output for any segmentation backend or annotation tool.
- `polygon`: exported polygon lists from LabelMe or annotator UIs map directly to `mask_type: polygon`.
- `final_output_file`: result of applying a mask (alpha PNG) or running a cleanup backend.

## Short conclusion

The immediate practical investments are lightweight review/correction tools that produce polygons/masks (LabelMe, segment-anything-annotator workflows) and small mask utilities (dilate/erode, overlay visualization). Heavy segmentation models like SAM/SAM2 remain future backends to evaluate in isolated spikes.
