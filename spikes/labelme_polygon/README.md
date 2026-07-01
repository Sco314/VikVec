# Spike: labelme_polygon

Question tested
- Can manual polygon annotation workflows reduce artifact leakage (neighboring fragments) compared to bbox-first crops?

Expected input
- Representative reference images and asset sheets (PNG/JPG) with irregular objects and cluttered backgrounds.

Expected output
- Polygon annotations (LabelMe JSON) and exported mask PNGs; screenshots of the annotation workflow.

Success criteria
- Masks/polygons exclude neighboring fragments that were present in bbox crops.
- Exported polygons or `mask_file` can be applied to produce `final_output_file` RGBA images with clean alpha.

Dependency risk
- Low/medium: `labelme` is a desktop app (PyQt) and not a heavy ML dependency. No model checkpoints required.

How output maps back to VikVec
- `mask_file`: path to PNG mask created or exported
- `polygon`: polygon coordinate arrays exported in JSON → maps to `mask_type: polygon`
- `final_output_file`: result of applying mask (alpha PNG)

Notes
- If a full cloned repo is used, record source in `notes.md` and store under `spikes/labelme_polygon/` rather than modifying `vikvec/`.
