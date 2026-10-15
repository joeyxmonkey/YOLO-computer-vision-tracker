# YOLO Video Tracker

A local video viewer that detects objects with **Ultralytics YOLO26m** and follows them across frames with **ByteTrack**. OpenCV displays bounding boxes, class names, tracking IDs, confidence scores, and a center marker for each tracked object.

This repository contains the original tracker, maintained separately from Inspection Desk in `video-tracker`.

## Quick start

The local `.venv` is already set up. Open PowerShell in **video-tracker-yolo** and run:

```powershell
.\.venv\Scripts\python.exe main.py
```

The viewer opens `sample.mp4` using `yolo26m.pt`. Keep the video window focused while watching. Playback ends at the end of the video; to stop early, press **Ctrl+C** in the terminal. There is currently no Q or Escape shortcut, and closing the video window alone may not stop the program.

Run from the project folder because video and model paths are relative to the current working directory. Environment activation is optional when using the command above.

## Features

- Object detection using the pretrained YOLO26m model.
- Persistent ByteTrack IDs across video frames.
- Overlays showing the object class, tracking ID, confidence percentage, bounding box, and center point.
- Local video playback in an OpenCV window.
- Automatic GPU use when a supported GPU and CUDA-enabled PyTorch are available; CPU execution otherwise.

For example, `car #4 87%` identifies a car detection with track ID 4 and a model confidence score of 87%. IDs describe tracks within the current run and may change when an object disappears or tracking is lost.

## Set up a new environment

Use **64-bit Python 3.11**. The existing environment uses Python **3.11.9**.

From PowerShell in the project folder:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt "lap==0.5.13"
.\.venv\Scripts\python.exe -m pip check
```

Check that `python --version` reports Python 3.11 before creating the environment. If the Windows Python launcher is configured, `py -3.11 -m venv .venv` is another option. If neither command finds Python, run the installed Python 3.11 executable by its full path.

`requirements.txt` pins OpenCV and Ultralytics. The separate `lap` installation provides ByteTrack's assignment dependency, avoiding an automatic installation when tracking first starts. PyTorch and other dependencies are installed through Ultralytics; GPU support requires the appropriate PyTorch build below.

### NVIDIA GPU setup

The local environment was verified on an **NVIDIA GeForce RTX 3080 Ti** with:

| Component | Installed version |
| --- | --- |
| Python | 3.11.9 |
| OpenCV (`opencv-python`) | 5.0.0.93 |
| Ultralytics | 8.4.173 |
| PyTorch | 2.11.0+cu128 |
| Torchvision | 0.26.0+cu128 |
| LAP | 0.5.13 |

To reproduce the tested GPU build after creating `.venv`, install PyTorch before the remaining requirements:

```powershell
.\.venv\Scripts\python.exe -m pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements.txt "lap==0.5.13"
```

If replacing an existing CPU-only PyTorch installation, add `--force-reinstall` to the PyTorch command. A compatible NVIDIA driver is required. See the [official PyTorch installation instructions](https://pytorch.org/get-started/previous-versions/) for other hardware or builds.

Check GPU availability:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

### Optional activation

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Use `deactivate` when finished. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe main.py` directly.

## Choose a video or model

Settings currently live in `main.py`; there are no command-line options or settings screen.

| Setting | Current value | How to change it |
| --- | --- | --- |
| Video source | `sample.mp4` | Change the path in `cv2.VideoCapture(...)`. |
| Model | `yolo26m.pt` | Change the filename in `YOLO(...)`; `yolo26n.pt` is also available locally. |
| Tracker | `bytetrack.yaml` | Change `tracker` in `model.track(...)`. This name uses Ultralytics' bundled configuration. |
| Detection confidence threshold | `0.1` | Change `conf` in `model.track(...)`. |
| Track persistence | `True` | Keeps tracker state between successive frames. |
| Display size | `1920 x 1080` | Change the dimensions in `cv2.resize(...)`. |
| Display wait | `30` milliseconds | Change `cv2.waitKey(30)`. Processing time also affects playback speed. |

For example, to open another local video:

```python
video = cv2.VideoCapture("sample2.mp4")
```

Use an absolute path or a path relative to the folder where you launch the program. For Windows absolute paths in Python, use a raw string such as `r"C:\Videos\clip.mp4"`.

The confidence threshold filters detections before tracking. ByteTrack has its own association thresholds, so a detection may not immediately receive an ID. The viewer draws overlays only for detections with tracking IDs. Confidence scores are model scores, not calibrated probabilities of correctness.

## Project files

```text
video-tracker-yolo/
|-- main.py             # Video decoding, detection, tracking, and display
|-- requirements.txt    # Pinned OpenCV and Ultralytics versions
|-- README.md
|-- .gitignore
|-- .venv/              # Local Python environment (ignored by Git)
|-- sample.mp4          # Default input video (local, ignored by Git)
|-- sample2.mp4         # Additional local sample, when present
|-- yolo26m.pt          # Default model weights (local, ignored by Git)
`-- yolo26n.pt          # Smaller model weights, when present
```

Model weights, video files, and `.venv` are local assets and are not included in a new clone. Supply a video named `sample.mp4` or update the input path. Ultralytics can download supported missing pretrained weights on first use when internet access is available. For offline use, place the required weights in the folder beforehand.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `ModuleNotFoundError` for `cv2`, `ultralytics`, or `lap` | Use `.\.venv\Scripts\python.exe` and reinstall the requirements plus `lap` using the setup commands above. Select this same interpreter in your editor. |
| Program exits without showing a video | Confirm the input file exists, the path is correct, and you started from the project folder. The current script exits when a frame cannot be read. |
| Missing model or failed download | Place `yolo26m.pt` in the project folder, or allow the initial pretrained-weight download. |
| CUDA reports `False` | Check the NVIDIA driver and that this environment has a CUDA-enabled PyTorch build. CPU execution remains available. |
| Playback is slow | Verify GPU availability or try `yolo26n.pt`. Playback speed includes inference time and the display wait. |
| Boxes or IDs appear late, or IDs change | Tracking depends on detection quality, association thresholds, occlusion, and motion. IDs are not permanent object identities. |
| Video looks stretched | The display resizes every frame to 1920 x 1080. Adjust those dimensions to match the video's aspect ratio. |
| OpenCV cannot open a display window | Use the desktop `opencv-python` package from the requirements, rather than a headless build, and run in a graphical desktop session. |

## Current scope

This is a viewing prototype. It does not save annotated video, tracking records, inspection decisions, or CSV reports. It uses a pretrained general object detector; it has not been validated as a food-defect inspection system. There are no pause, seek, or playback-speed controls.

The environment was checked by decoding the local sample video and running YOLO26m with ByteTrack on the RTX 3080 Ti. A tracking ID was produced on frame 6, and the package dependency check passed. This is a setup check, not an accuracy benchmark.

## References

- [Ultralytics setup and installation](https://docs.ultralytics.com/quickstart/)
- [PyTorch installation builds](https://pytorch.org/get-started/previous-versions/)
