# YOLO Video Tracker

The original Ultralytics YOLO26m + ByteTrack viewer, preserved separately from Inspection Desk. `main.py` is unchanged from source commit `6fc2902f98002f96e26cc6c20051ef3a18f389f7` in video-tracker. This repository retains the original tracker Git history and has no GitHub remote configured.

## Run on Windows

Use Python 3.11 and run PowerShell in this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

The viewer reads `sample.mp4` and loads `yolo26m.pt` from this folder. Copies of the existing sample and weights are provided locally and ignored by Git. If absent, provide a video named `sample.mp4`; Ultralytics can download missing model weights when internet access is available. Video playback shows detections and persistent tracking IDs; it does not save inspection records. Other sample videos and the smaller YOLO model were also copied when available.

To connect your new GitHub repository later:

```powershell
git remote add origin YOUR_NEW_GITHUB_REPOSITORY_URL
git push -u origin main
```
