# Assisted mask creation notes

## Current direction note

Manual LabelMe polygon annotation validated the end-to-end mask-first path, but the project is now shifting to automated candidate mask generation.

Do not spend the next phase manually testing AI-Box one asset at a time. The next concrete technical test is to inspect `osam` CLI/API behavior and determine whether it can generate masks headlessly from an image, box, point, or automatic mode.

## Running log

### 2026-06-30 22:34 America/Chicago

- Command run: `git status --short`
- What happened: working tree was clean.
- Output path: none.
- Result quality: safe to continue.
- Next action: confirm current branch.

### 2026-06-30 22:34 America/Chicago

- Command run: `git branch --show-current`
- What happened: current branch was `spike/labelme-polygon-plan`, not the requested research branch.
- Output path: none.
- Result quality: needed branch switch before research edits.
- Next action: create/switch to `spike/assisted-mask-creation-research`.

### 2026-06-30 22:34 America/Chicago

- Command run: `git switch -c spike/assisted-mask-creation-research`
- What happened: created and switched to the requested branch.
- Output path: none.
- Result quality: branch setup complete.
- Next action: inspect installed LabelMe AI features.

### 2026-06-30 22:34 America/Chicago

- Command run: `.venv/bin/labelme --help`
- Dependency installed: none.
- Model downloaded: none.
- What happened: LabelMe CLI help showed standard file/config/output options but no CLI automation flags.
- Output path: none.
- Result quality: AI features appear to be GUI-only, not exposed as a simple CLI command.
- Next action: search installed files for automation hooks.

### 2026-06-30 22:34 America/Chicago

- Command run: `grep -R "osam\|sam2\|automation\|point\|prompt" .venv/lib 2>/dev/null | head -120`
- Dependency installed: none.
- Model downloaded: none.
- What happened: broad search mostly returned unrelated package text; it was too noisy.
- Output path: none.
- Result quality: insufficient signal.
- Next action: narrow search to `labelme` and `osam` packages.

### 2026-06-30 22:34 America/Chicago

- Command run: `.venv/bin/python -m pip show labelme osam onnxruntime`
- Dependency installed: none.
- Model downloaded: none.
- What happened: confirmed `labelme` 6.3.1 requires `osam`; `osam` 0.5.0 requires `onnxruntime`; `onnxruntime` 1.27.0 is installed.
- Output path: none.
- Result quality: confirms the LabelMe install is not as lightweight as expected.
- Next action: inspect installed LabelMe AI widgets and canvas actions.

### 2026-06-30 22:34 America/Chicago

- Command run: inspected installed files under `.venv/lib/python3.14/site-packages/labelme`.
- Dependency installed: none.
- Model downloaded: none.
- What happened: found `labelme/_automation`, AI widget files, and icons for `ai-box.svg` and `ai-points.svg`.
- Output path: none.
- Result quality: strong evidence of built-in AI-assisted annotation.
- Next action: inspect widget code for available UI options.

### 2026-06-30 22:34 America/Chicago

- Command run: inspected `labelme/widgets/_ai_assisted_annotation_widget.py`, `_ai_text_to_annotation_widget.py`, `_automation/_osam_session.py`, `app.py`, and `canvas.py`.
- Dependency installed: none.
- Model downloaded: none.
- What happened: confirmed these UI options:
  - AI-Assisted Annotation panel.
  - AI-Points mode.
  - AI-Box mode.
  - AI Text-to-Annotation panel.
  - model selector for EfficientSAM, SAM, SAM2, and SAM3.
  - text model selector for SAM3 and YOLO-World.
  - output format selector for Polygon, Mask, Rectangle, Oriented Rectangle, and Circle.
  - point prompts with positive clicks and Shift+Click negative clicks.
  - box prompts by drawing a bounding box.
  - generated shapes are native LabelMe shapes, so correction/review should remain available.
- Output path: none.
- Result quality: LabelMe built-in AI is the best first candidate because it keeps output close to the proven importer.
- Next action: launch LabelMe and confirm it loads the target image.

### 2026-06-30 22:34 America/Chicago

- Command run: `.venv/bin/labelme input/reference_scene.png --output spikes/labelme_polygon/outputs`
- Dependency installed: none.
- Model downloaded: none.
- What happened: LabelMe 6.3.1 launched and loaded `input/reference_scene.png`; the process was stopped after confirming launch to avoid leaving a GUI session running.
- Output path: none.
- Result quality: launch path works. I did not produce a new assisted annotation because GUI interaction is required.
- Next action: inspect `osam` directly for headless/scriptable mask generation.

### 2026-06-30 22:36 America/Chicago

- Command run: `.venv/bin/python -m osam list`
- Dependency installed: none.
- Model downloaded: none.
- What happened: command failed because `osam` tried to write `/Users/scottsandvik/.cache/osam/osam.log`, outside the allowed spike area.
- Output path: none.
- Result quality: important sandbox finding; do not run osam model commands without redirecting cache/HOME into a spike-local folder.
- Next action: retry with `HOME` pointed at `spikes/assisted_mask_creation`.

### 2026-06-30 22:36 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/python -m osam list`
- Dependency installed: none.
- Model downloaded: none.
- What happened: osam ran with a spike-local cache and listed no downloaded models.
- Output path: `spikes/assisted_mask_creation/.cache/osam/osam.log`
- Result quality: confirms a spike-local cache pattern works, but no model is currently available.
- Next action: document that any LabelMe/osam assisted test should set `HOME` or equivalent to a spike-local cache before model download.

### 2026-06-30 22:42 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/osam --help`
- Dependency installed: none.
- Model downloaded: none.
- What happened: confirmed `osam` has `list`, `pull`, `rm`, `run`, and `serve` commands.
- Output path: none.
- Result quality: `osam` is scriptable from CLI.
- Next action: inspect `osam run`.

### 2026-06-30 22:42 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/osam run --help`
- Dependency installed: none.
- Model downloaded: none.
- What happened: confirmed `osam run` accepts `--image`, `--prompt`, and `--json`.
- Output path: none.
- Result quality: headless prompted mask generation is supported.
- Next action: inspect prompt schema and Python APIs.

### 2026-06-30 22:42 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/python -c "import osam, inspect; print(osam); print(dir(osam))"`
- Dependency installed: none.
- Model downloaded: none.
- What happened: confirmed `osam` exposes `apis` and `types` modules.
- Output path: none.
- Result quality: direct Python integration is available.
- Next action: inspect prompt/request/annotation types.

### 2026-06-30 22:43 America/Chicago

- Command run: searched installed `osam` package for scriptable APIs and inspected `osam/__main__.py`, `types/_prompt.py`, `types/_generate.py`, `types/_annotation.py`, `types/_bounding_box.py`, and `apis.py`.
- Dependency installed: none.
- Model downloaded: none.
- What happened: found a usable headless API:
  - `osam.apis.generate(request=osam.types.GenerateRequest(...))`
  - `Prompt(points=..., point_labels=...)`
  - point labels: `0` background, `1` foreground, `2` bbox top-left, `3` bbox bottom-right.
- Output path: none.
- Result quality: bbox and point prompts can be scripted. No automatic mask generation API was found in `osam` 0.5.0 for SAM-family models.
- Next action: pull a lightweight model into the spike-local cache.

### 2026-06-30 22:44 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/osam pull efficientsam:10m`
- Dependency installed: none.
- Model downloaded: initial attempt failed under sandbox DNS.
- What happened: pull attempted to download EfficientSAM ONNX blobs from GitHub into `spikes/assisted_mask_creation/.cache/osam/models/blobs/`.
- Output path: none from failed attempt.
- Result quality: network access is required for model download.
- Next action: rerun with network approval.

### 2026-06-30 22:44 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/osam pull efficientsam:10m`
- Dependency installed: none.
- Model downloaded: `efficientsam:10m`, 39.45 MB total, into ignored spike-local `.cache/osam/models/blobs/`.
- What happened: downloaded EfficientSAM encoder and decoder ONNX files.
- Output path: `spikes/assisted_mask_creation/.cache/osam/models/blobs/`
- Result quality: model cache isolation works.
- Next action: create and run a headless probe.

### 2026-06-30 22:45 America/Chicago

- Command run: `HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/python spikes/assisted_mask_creation/osam_headless_probe.py`
- Dependency installed: none.
- Model downloaded: none during this run; used already-pulled `efficientsam:10m`.
- What happened: generated two prompted mask candidates for `scene_process_tanks_iso_01` from `input/reference_scene.png`.
- Output path: `spikes/assisted_mask_creation/outputs/osam_probe/`
- Result quality:
  - `scene_process_tanks_box_00_mask.png`: localized the process/tank scene from a scripted bbox prompt. This is promising for candidate generation.
  - `scene_process_tanks_box_00_cutout.png`: transparent PNG candidate from the bbox mask.
  - `scene_process_tanks_points_00_mask.png`: not useful; the point prompt selected too much of the image/background.
  - `report.json`: includes prompt parameters, bbox, polygon points, `mask_file`, `final_output_file`, and VikVec field mapping.
- Next action: test generated or heuristic bbox prompts at scale, or move to SAM automatic mask generation if bbox seeding is insufficient.

## Current result

The primary pipeline should be automated:

automatic extractor backend -> candidate masks -> VikVec manifest -> transparent PNGs -> contact sheet -> human fixes only failures in LabelMe.

`osam` can be automated headlessly for prompted masks. It supports scriptable point and bbox prompts through both CLI (`osam run --image ... --prompt ...`) and Python (`osam.apis.generate`). The probe produced mask PNGs, transparent cutout PNGs, and a report that maps to VikVec fields.

`osam` 0.5.0 does not appear to expose SAM automatic mask generation. It is useful as a headless prompted-mask backend, especially with generated/heuristic bounding boxes. The bbox prompt was promising; the point prompt was not.

The main operational risk is cache placement: osam defaults to `~/.cache/osam`, so automated runs should set `HOME` or another documented cache override to a spike-local folder.

## Candidate recommendation

Most promising now: `osam` headless bbox-prompted mask generation.

Recommended next action: create a scriptable candidate-mask pipeline that generates multiple bbox prompts automatically, runs `osam` on each, filters/ranks masks by size/location/overlap, writes a VikVec-style candidate manifest, finalizes transparent PNGs, and produces a contact sheet. Keep LabelMe only as the correction tool for bad reviewed masks.
