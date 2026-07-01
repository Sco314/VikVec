# Spike plan and controlled evaluation policy for mask tools

This document defines a conservative, auditable approach for evaluating external segmentation and annotation tools. The goal is to let engineers test candidate tooling while avoiding heavy dependency or license surprises.

## Spike principles

- Keep spikes isolated under `spikes/` or `external_reference/` — do not modify `vikvec/` core code as part of a spike.
- Prefer evaluation by example and minimal, shallow code to port ideas — prefer reimplementation of small utilities rather than wholesale copying.
- Avoid heavy installs (PyTorch, model weights) unless explicitly approved and environment constraints are satisfied.
- Mask-first does not mean manual-first. Manual LabelMe polygon correction is already proven; future spikes should prioritize automated/scriptable candidate mask generation.

## Headless automation priority

The next spike question is:

Can we programmatically generate candidate masks for `input/reference_scene.png`?

Manual LabelMe polygon annotation is already proven and should not be repeated as the primary workflow. GUI tools are valuable mainly when they support correction/review or export reusable data.

`osam` should be the immediate headless probe because LabelMe installed it and it appears to expose SAM2-style automation.

Candidate order:

1. `osam` headless/scriptable probe
2. SAM/SAM2 automatic mask generation
3. SAM-remove-background scriptable mask/cutout flow
4. `segment-anything-annotator` only if its useful parts can be scripted or used as correction UI
5. Grounded-SAM for later text-driven detection
6. LabelMe GUI as correction fallback

## Allowed during isolated spikes

1. Shallow clone
   - Use `git clone --depth 1` into `spikes/<repo_name>/`.
   - Do not clone into the VikVec package itself.

2. Sparse checkout
   - Use sparse checkout when only a small folder or files are needed from a large repo.
   - Store results under `spikes/` or `external_reference/` with clear notes.

3. Cherry-picking / porting
   - Allowed for small utilities (mask dilation, erosion, overlay visualization, crop-around-mask, paste-with-mask, contour-to-SVG helper).
   - Must record source attribution and license. Prefer rewriting the utility in a minimal, well-documented form.

4. Vendoring / scavenging
   - Allowed only after explicit approval and only for small files with compatible licenses.
   - Must document: source repo, file path, license, reason for vendoring, and changes made.
   - Do not vendor entire heavy repos.

## Future research autonomy

Allowed in isolated spikes without asking again:

- Create spike-local virtual environments.
- Install dependencies inside spike-local environments.
- Shallow clone repos into `external_reference/`.
- Download model files into spike-local model/cache folders.
- Write probe scripts under `spikes/`.
- Run candidate tools against `input/reference_scene.png`.
- Produce outputs under `spikes/<tool>/outputs/`.

## Not allowed without explicit approval

- Modify VikVec core code based on a spike.
- Change repo-level requirements or package config.
- Commit large model files.
- Vendor external repo code into VikVec core.
- Push major integration changes without a review point.

## Spike repo layout (recommended)

```
spikes/
  labelme_polygon/
    README.md        # goal, commands used
    notes.md         # findings and logs
    inputs/          # sample input images
    outputs/         # result artifacts (masks, polygons, screenshots)
  segment_anything_annotator/
    README.md
    notes.md
    outputs/
  sam_remove_background/
    README.md
    notes.md
    outputs/
```

## Per-spike documentation checklist

- Question being tested (one sentence)
- Install risk (low/medium/high)
- Dependency weight (light/medium/heavy)
- Input image(s) used
- Expected output(s)
- Success criteria (pass/fail thresholds or manual checks)
- Mapping to VikVec manifest fields: `mask_file`, `final_output_file`, `svg_output_file`, `extraction_method`, `review_status`

## Recommended first spike

- `osam` headless/scriptable probe — the top priority is automated candidate mask generation that can feed manifest entries, transparent PNG finalization, and contact sheet QA. LabelMe remains the fallback correction tool for failed/dirty masks.

## Operational rules

- Do not install heavy dependencies or download model weights during the spike unless explicitly approved by the team lead.
- If cherry-picking code, include a `NOTES` header in the file that records source and license. Keep the ported utility small and well-tested.
- After a successful spike, propose a minimal integration plan that keeps the manifest unchanged and adds an optional backend adapter under `vikvec/backends/`.
