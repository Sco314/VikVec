# VikVec roadmap

## Stage 1: Lightweight extraction

Use Pillow, OpenCV, and NumPy for the current core workflow:

- detect scene candidates
- crop and trim assets
- apply auto_foreground isolation for white-background sheets
- validate outputs
- create contact sheets
- export transparent PNG final assets

## Stage 2: Review and metadata

Add richer manifest metadata:

- manual bbox corrections
- manual or fallback polygon masks
- animation metadata
- review flags and final manifest output

## Stage 3: Optional segmentation backends

Add optional backends for:

- rembg
- SAM / SAM2 point or box-mask extraction

These should integrate through the same manifest and review flow.

## Stage 4: Optional cleanup and inpainting

Support backend-driven cleanup tasks:

- remove stray fragments
- fill missing background
- paste objects into scenes
- improve generated composites

## Stage 5: Vector and motion

Later support:

- mask-to-SVG outline generation
- SVG path-reveal animation
- limited motion planning and simple animated previews such as MP4 or GIF outputs
