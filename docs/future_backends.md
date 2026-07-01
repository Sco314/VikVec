# Future optional backends

These modules are planned as optional future capabilities. They are not required for the current lightweight extraction workflow.

## SAM / SAM2

SAM and SAM2 are promising for promptable segmentation. In the future, they could support point-prompted or box-prompted object masks for hard cases such as workers, tanks, chairs, or pipes.

These should be implemented as optional backends that produce a mask or final asset with the same manifest fields as the current workflow.

## rembg

rembg is useful for AI background removal. It can be used later as a background-removal backend for difficult scenes, but it should not be required for the base workflow.

## Inpaint-Anything pattern

The Inpaint-Anything pattern is a useful design model for cleanup and compositing:

1. generate a mask,
2. dilate or erode it,
3. remove or replace the object,
4. fill or composite the background.

This is useful later for cleanup, but it is not the current core extraction path.

## sam2vec pattern

The sam2vec idea suggests moving from mask to vector outline. VikVec can adopt this later as a mask-to-SVG path for outlines or clipping paths, but that remains a future optional backend.

## Sketch2Motion pattern

Sketch2Motion is a useful inspiration for later SVG path-reveal animation. It is not a semantic object detector, but it can inform how traced outlines become simple animated motion previews.

## Design rule

Future backends should remain optional and pluggable. The manifest, review workflow, and output structure should stay stable even when the extraction engine changes.
