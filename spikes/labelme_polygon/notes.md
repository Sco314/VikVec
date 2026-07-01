# Notes: labelme_polygon spike — concrete execution plan

Purpose
- Track the step-by-step plan for validating whether LabelMe-style polygon annotation yields usable `mask_file` and `final_output_file` artifacts for VikVec.

Planned steps (do not install anything yet)
1. Prepare test inputs: confirm `input/reference_scene.png` exists in the workspace. If it does not exist, add a small representative image under `spikes/labelme_polygon/inputs/`.
2. (Manual) Open the image in LabelMe (desktop) and draw a polygon around `scene_process_tanks_iso_01`, excluding neighboring fragments.
3. Export LabelMe JSON annotation and, if possible, an exported mask PNG. Capture a screenshot of the polygon in the UI.
4. Locally (prototype script), convert the polygon into a mask PNG if LabelMe did not export one. Do this in the spike folder only.
5. Apply the mask to the source image to produce a `final_output_file` RGBA (alpha) PNG.
6. Record results in `spikes/labelme_polygon/notes.md` and copy artifacts to `spikes/labelme_polygon/outputs/`.

Checklist for each run
- Input present: `input/reference_scene.png`
- Polygon JSON exported and polygon points verified
- Mask PNG present (either exported or generated)
- `final_output_file` RGBA produced and visually verified (no neighboring fragments)
- Manifest mapping verified: polygon points and mask path recorded

Mapping to VikVec manifest fields (example)
```
{
	"asset_name": "scene_process_tanks_iso_01",
	"extraction_method": "labelme_polygon",
	"mask_type": "polygon",
	"polygon": [[x1,y1],[x2,y2],...],
	"mask_file": "spikes/labelme_polygon/outputs/scene_process_tanks_mask.png",
	"final_output_file": "spikes/labelme_polygon/outputs/scene_process_tanks_final.png",
	"review_status": "final_needs_visual_review"
}
```

Success criteria
- One clean transparent PNG produced for the target asset with no neighboring fragments.
- Polygon points are storable and mappable in the manifest as above.

Risk and mitigations
- Risk: LabelMe requires desktop and PyQt. Mitigation: do not install as part of this spike; run manual evaluation on a separate approved machine or get approval first.

Recordkeeping
- Save screenshots, exported JSON, generated mask PNG, and final RGBA in `spikes/labelme_polygon/outputs/` with timestamps.

Next actions after approval
- If the manual spike succeeds and the process is valuable, propose either:
	- a small helper script in `spikes/labelme_polygon/` to convert LabelMe JSON → mask PNG and integrate into a `vikvec/backends/labelme_polygon.py` adapter (design only), or
	- document a reviewer workflow linking to `docs/spike_plan_mask_tools.md` and update architecture docs.
