# Spike: segment-anything-annotator

Question tested
- Can an annotator UI that combines promptable SAM masks with human corrections support the VikVec review workflow (polygon correction and label export)?

Expected input
- Images and asset sheets; optionally small sample masks or example prompts.

Expected output
- Masks, polygons, JSON/COCO-style annotations, and screenshots of the UI workflow showing correction steps.

Success criteria
- Reviewer-corrected masks export clean polygons or mask PNGs that map to `mask_file` and `polygon` manifest fields.
- Workflow reduces manual correction time compared to purely manual annotation.

Dependency risk
- Medium/high: the annotator is a web UI (JS stack) and often integrates SAM as a backend. Running full functionality may require a SAM backend (heavy) but the UI alone can be evaluated.

How output maps back to VikVec
- `mask_file`: exported mask PNG
- `polygon`: exported polygons
- `final_output_file`: masked RGBA result after applying polygon/mask

Notes
- If a full cloned repo is used, record the source (e.g., `segment-anything-annotator` repo) in `notes.md` and keep code under `spikes/`.
