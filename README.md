# Video Object Tracker

Object detection and basic tracking in local videos using Python, OpenCV, and Ultralytics YOLO.

## Features

- Video frame processing with OpenCV
- YOLO object detection
- Bounding boxes, class labels, and confidence scores
- Object center visualization
- Basic nearest-neighbor tracking with object IDs

The tracker matches detections by the distance between their centers. IDs can change or be shared when objects cross paths; this is a simple tracking prototype.

## Requirements

- Windows and PowerShell for the commands below
- [Git](https://git-scm.com/downloads/win)
- [Python 3.11](https://www.python.org/downloads/windows/) (64-bit), matching the existing development environment; include the Python launcher when installing
- Internet access to install packages and download the model on the first run
- A local video file to process

## Setup

### 1. Get the project

```powershell
git clone https://github.com/Hitogai/video-tracker.git
cd video-tracker
```

If you already have the project, open PowerShell in that folder and skip cloning. Run the remaining commands from the folder containing `main.py` and `requirements.txt`.

### 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

This creates an isolated place for the project's Python packages. If this project already has a working `.venv`, reuse it and skip this command.

### 3. Install the Python packages

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` comes with the repository and lists the package versions. Cloning the repository does **not** install them. The second command downloads and installs the listed packages, including OpenCV, Ultralytics, and PyTorch, along with their required dependencies. The initial installation may take several minutes.

These commands use the virtual environment's Python directly, so activation is optional. See the [pip requirements-file documentation](https://pip.pypa.io/en/stable/user_guide/#requirements-files) for details.

### 4. Add a video

Place your video in the project folder and name it `Sample.mp4`, matching the current code:

```python
video = cv2.VideoCapture("Sample.mp4")
```

Alternatively, edit that line in `main.py` to use your filename or full path. Match the filename's capitalization when running on a case-sensitive filesystem.

Sample videos are ignored by Git and are not included when cloning the repository. Each person needs to supply their own video or get a copy separately.

### 5. Run the tracker

```powershell
.\.venv\Scripts\python.exe main.py
```

The program opens an OpenCV window displaying the video with bounding boxes, class labels, confidence scores, and object IDs. It finishes when the video ends. To interrupt it, focus the PowerShell window and press `Ctrl+C`.

The code loads this pretrained model:

```python
model = YOLO("yolo26m.pt")
```

Ultralytics automatically downloads the model weights if they are missing. Allow the download to finish on the first run. Model weights are ignored by Git; you do not need to commit them. If downloading is unavailable, place a copy of the official `yolo26m.pt` weights in the project folder before running.

For a smaller model, change that line to `YOLO("yolo26n.pt")`. See the [Ultralytics YOLO26 documentation](https://docs.ultralytics.com/models/yolo26/) for the model options.

## Running again later

Open PowerShell in the project folder and run:

```powershell
.\.venv\Scripts\python.exe main.py
```

You do not need to recreate the virtual environment or reinstall packages every time. Rerun the requirements installation command after pulling changes that update `requirements.txt`.

If you prefer to activate the environment, use:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Run `deactivate` when finished. If PowerShell blocks `Activate.ps1`, use the direct `.\.venv\Scripts\python.exe` commands above; activation is not required.

## Troubleshooting

- **`py` is not recognized or Python 3.11 is missing:** Install Python 3.11 with its launcher, reopen PowerShell, and retry. If `python --version` already reports Python 3.11, you can use `python -m venv .venv` instead.
- **`ModuleNotFoundError`:** Run the requirements installation command again and launch with `.\.venv\Scripts\python.exe main.py` so installation and execution use the same environment.
- **The program exits without showing a video:** Confirm that the video exists, its filename matches the `cv2.VideoCapture(...)` line, and PowerShell is in the project folder. The current code exits when it cannot read a frame.
- **A model download fails:** Check internet access and retry, or provide the official weights file locally.
- **Processing is slow:** Try `yolo26n.pt` in place of `yolo26m.pt`. Speed depends on your hardware and video.

## Files kept out of Git

The `.gitignore` excludes virtual environments, Python caches, model weights, local videos, and local `.env` secrets. Keep `main.py`, `README.md`, `requirements.txt`, and `.gitignore` in the repository so others can recreate the setup.
