# Commands log

```sh
git status --short
git branch --show-current
git switch -c spike/assisted-mask-creation-research
.venv/bin/labelme --help
grep -R "osam\|sam2\|automation\|point\|prompt" .venv/lib 2>/dev/null | head -120
rg -n "osam|sam2|automation|point|prompt|Auto|Segment|mask" .venv/lib/python3.14/site-packages/labelme .venv/lib/python3.14/site-packages/osam* 2>/dev/null
.venv/bin/python -m pip show labelme osam onnxruntime
find .venv/lib/python3.14/site-packages/labelme -maxdepth 3 -type f | sort | sed -n '1,200p'
curl -s "https://api.github.com/search/repositories?q=segment-anything-annotator"
curl -s "https://api.github.com/search/repositories?q=labelme-with-segment-anything"
curl -s "https://api.github.com/search/repositories?q=SAM-remove-background"
curl -s "https://api.github.com/search/repositories?q=sam2vec"
sed -n '1,260p' .venv/lib/python3.14/site-packages/labelme/widgets/_ai_assisted_annotation_widget.py
sed -n '1,260p' .venv/lib/python3.14/site-packages/labelme/widgets/_ai_text_to_annotation_widget.py
sed -n '1,280p' .venv/lib/python3.14/site-packages/labelme/_automation/_osam_session.py
rg -n "AI|ai|automation|_automation|create.*AI|SAM|osam|points|box" .venv/lib/python3.14/site-packages/labelme/app.py .venv/lib/python3.14/site-packages/labelme/widgets/canvas.py
.venv/bin/labelme input/reference_scene.png --output spikes/labelme_polygon/outputs
pgrep -fl "labelme input/reference_scene.png"
sed -n '1,240p' .venv/lib/python3.14/site-packages/labelme/widgets/download.py
find .venv/lib/python3.14/site-packages/osam -maxdepth 3 -type f | sort | sed -n '1,180p'
rg -n "download|cache|model_dir|HOME|OSAM|onnx|sam2" .venv/lib/python3.14/site-packages/osam .venv/lib/python3.14/site-packages/labelme/widgets/download.py
sed -n '1,260p' .venv/lib/python3.14/site-packages/osam/types/_blob.py
sed -n '1,220p' .venv/lib/python3.14/site-packages/osam/_models/sam2/_models.py
sed -n '1,220p' .venv/lib/python3.14/site-packages/osam/_models/efficientsam/_models.py
.venv/bin/python -m osam list
mkdir -p spikes/assisted_mask_creation/outputs external_reference
HOME=/Users/scottsandvik/Documents/GitHub/VikVec/VikVec/spikes/assisted_mask_creation .venv/bin/python -m osam list
curl -s https://api.github.com/repos/haochenheheda/segment-anything-annotator
curl -s https://api.github.com/repos/MrSyee/SAM-remove-background
curl -s https://api.github.com/repos/IDEA-Research/Grounded-Segment-Anything
curl -s https://api.github.com/repos/geekyutao/Inpaint-Anything
curl -s "https://api.github.com/search/repositories?q=Grounded-SAM-2"
```

