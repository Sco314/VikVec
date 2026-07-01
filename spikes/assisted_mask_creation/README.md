# Assisted mask creation research

## Purpose

This spike researches practical ways to reduce manual polygon drawing for VikVec asset masks while preserving human review and correction.

## Proven baseline

The previous LabelMe spike proved this pipeline:

LabelMe polygon JSON -> VikVec manifest -> transparent PNG cutout -> contact sheet review.

That baseline works architecturally. The remaining problem is how to create cleaner masks faster than drawing many manual polygon vertices.

## New goal

Find a practical assisted-mask workflow for `input/reference_scene.png`, focused on `scene_process_tanks_iso_01`, that can produce a usable LabelMe JSON, mask, or transparent PNG while still allowing a human to review and correct the result.

## Sandbox rules

- Keep research inside `spikes/assisted_mask_creation/`, candidate spike folders, or `external_reference/`.
- Do not modify VikVec core files under `vikvec/`.
- Do not modify repo-level dependency files.
- Use spike-local virtual environments for heavy candidates.
- Put model files only under a spike-local `models/` folder or a documented spike-local cache.
- Run candidates only on `input/reference_scene.png`.
- Write outputs only under candidate spike `outputs/` folders.
- Do not commit cloned `external_reference/` repos or large model files without explicit approval.

## Success criteria

- Fewer manual points than the manual LabelMe polygon.
- No neighboring scene fragments in the final mask or transparent PNG.
- Output supports human review/correction.
- Output maps cleanly to VikVec fields: `extraction_method`, `mask_type`, `polygon`, `mask_file`, `final_output_file`, and `review_status`.
- Setup burden is realistic for a correction/review workflow.

