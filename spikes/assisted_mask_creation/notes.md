# Assisted mask creation notes

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
- Next action: run a supervised/manual UI test using AI-Box or AI-Points.

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

## Current result

LabelMe built-in AI-assisted annotation is viable enough to test first. It already exposes the exact interaction types needed for the next spike: AI-Points, AI-Box, AI Text-to-Annotation, model selection, and LabelMe-native Polygon/Mask outputs. This should map cleanly to VikVec's proven `labelme_polygon` importer path.

The main risk is operational, not architectural: osam defaults to `~/.cache/osam` for logs/models, while this research requires spike-local model/cache storage. A controlled UI test should launch LabelMe with a spike-local `HOME` or equivalent cache setup before downloading any EfficientSAM/SAM/SAM2 model.

## Candidate recommendation

Most promising now: LabelMe built-in AI-assisted annotation.

Recommended next action: run a supervised UI test using LabelMe AI-Box with output format `Polygon` and the lightest available model, with cache redirected to `spikes/assisted_mask_creation`, then save the resulting JSON under a spike output folder and import/finalize/review it through the already-proven VikVec commands.

