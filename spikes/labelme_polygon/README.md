# Spike: labelme_polygon — concrete test plan

Question tested
- Can a LabelMe-style polygon annotation workflow produce a usable `mask_file` and `final_output_file` for VikVec for a single target asset (without installing dependencies now)?

Test image
- `input/reference_scene.png`

Target asset
- `scene_process_tanks_iso_01` (first target: annotate the tank/process scene)

Expected annotation
- A polygon drawn around only the tank/process scene, explicitly excluding neighboring fragments and other scene clutter.

Expected LabelMe output
- A JSON annotation file containing a polygon (list of [x, y] points) for the target object, and optionally an exported mask PNG rendered from that polygon.

Expected VikVec mapping
- `asset_name`: `scene_process_tanks_iso_01`
- `extraction_method`: `labelme_polygon`
- `mask_type`: `polygon`
- `polygon`: list of polygon points extracted from LabelMe JSON
- `mask_file`: path to exported mask PNG (relative or absolute)
- `final_output_file`: RGBA PNG produced by applying the mask to the source crop or source image
- `review_status`: e.g., `final_needs_visual_review` or `success`

Success criteria
- Produce one clean transparent PNG asset where the tank/process is isolated and no neighboring scene fragments remain.
- Polygon points are storable in the manifest and map correctly to the `polygon` field.
- The manual annotation workflow is practical for reviewer correction (scales moderately well for spot-corrections, not bulk automation).

Install decision
- Do not install LabelMe for this spike without approval. This README defines the test plan only; actual installs or UI runs require explicit signoff.

Notes
- If a full cloned repo is referenced during evaluation, record the source and license in `notes.md`. Keep any cloned or extracted files under `spikes/labelme_polygon/` and do not modify `vikvec/` core.
