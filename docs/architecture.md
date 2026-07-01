# VikVec architecture

VikVec is an asset workflow, not a single-model pipeline. Its core job is to take source images, extract candidate assets, organize them in manifests, and produce reviewable transparent PNG outputs.

## Core principle

The manifest, file layout, review states, contact sheets, and final outputs are the durable architecture. Extraction backends are interchangeable modules that produce either a mask or a final asset from a source image.

## Workflow

1. Detect candidate scenes or objects from a reference image or asset sheet.
2. Crop the candidate into a raw asset and a trimmed asset.
3. Apply an extraction method such as bbox, auto_foreground, polygon, or mask_file.
4. Validate the result and mark review status.
5. Produce a final transparent PNG for downstream use.
6. Store the asset in a manifest for review and later animation planning.

## Manifest fields

Each asset entry should support the following fields:

- asset_name
- asset_type
- source_file
- bbox
- raw_output_file
- trimmed_output_file
- final_output_file
- mask_file
- mask_type
- extraction_method
- quality_status
- review_status
- animation_role
- movable
- layer_order
- pivot_point
- anchor_point
- motion_presets
- notes

Supported extraction methods in the current lightweight workflow:

- bbox
- auto_foreground
- polygon
- mask_file

## Pluggable backend model

VikVec keeps the same manifest and review flow regardless of the backend used:

- lightweight local methods such as bbox, auto_foreground, and polygon masks
- optional future segmentation backends for prompted masks
- optional future cleanup or compositing backends for object removal and replacement
- optional future vector or animation modules for SVG outlines and motion previews

Backends should produce either:

- a mask,
- a trimmed asset,
- or a final transparent asset.

They should not replace the manifest review system.
