# YOLO Video Tracker

Detect and track objects in local videos using **Ultralytics YOLO26** and **ByteTrack**. The OpenCV viewer displays bounding boxes, class names, tracking IDs, confidence scores, and object centers.

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue)

## Features

- Pretrained YOLO26 object detection with persistent ByteTrack tracking.
- Configurable video source, model, confidence threshold, and inference device.
- Resizable video display that preserves the input aspect ratio.
- Q, Escape, and window-close controls.
- Processing without a display window for batch checks.
- CPU execution and optional NVIDIA GPU acceleration.

## Requirements

- **64-bit Python 3.11** and Git.
- A local video you have permission to use.
- A graphical desktop for the viewer; use `--no-display` without a desktop.
- Internet access to install packages and download pretrained weights on first use.

Windows is the primary tested desktop platform. Commands for macOS and Linux are also provided; their desktop and inference behavior has not yet been independently verified.

## Installation

Clone the repository:

```sh
git clone https://github.com/joeyxmonkey/YOLO-computer-vision-tracker.git
cd YOLO-computer-vision-tracker
```

Create your own virtual environment and install the dependencies.

**Windows (PowerShell)**

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Check that `python --version` reports Python 3.11. If your Python launcher is configured, you can use `py -3.11 -m venv .venv` instead.

**macOS / Linux**

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

The commands below use the Windows environment path. On macOS or Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

Virtual environments, input videos, and downloaded model weights are excluded from Git. They are not included when you clone this repository.

### Optional NVIDIA GPU setup

For CUDA acceleration, install the appropriate PyTorch and Torchvision builds for your operating system and NVIDIA driver, following the [official PyTorch instructions](https://pytorch.org/get-started/locally/). Run the installation through this project's virtual-environment Python, then install `requirements.txt`.

Check whether the environment can use CUDA:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

The tracker selects a device automatically unless you specify `--device`. Use `--device cpu` to force CPU execution or `--device 0` for the first CUDA GPU. GPU support depends on your hardware, driver, and PyTorch installation.

## Usage

Supply a video path:

```powershell
.\.venv\Scripts\python.exe main.py --source "C:\Videos\clip.mp4"
```

Replace the example path with your own video. Relative paths are resolved from the directory where you run the command. If `--source` is omitted, the tracker looks for `sample.mp4` in that directory; no sample video is distributed with the repository.

The default model is `yolo26m.pt`. Ultralytics downloads supported pretrained weights if they are missing. For offline use, download the weights beforehand and pass their local path with `--model`.

**Use the smaller model:**

```powershell
.\.venv\Scripts\python.exe main.py --source "C:\Videos\clip.mp4" --model yolo26n.pt
```

**Choose a confidence threshold and GPU:**

```powershell
.\.venv\Scripts\python.exe main.py --source "C:\Videos\clip.mp4" --conf 0.25 --device 0
```

**Process a short clip without opening a window:**

```powershell
.\.venv\Scripts\python.exe main.py --source "C:\Videos\clip.mp4" --no-display --max-frames 30
```

**Show all options:**

```powershell
.\.venv\Scripts\python.exe main.py --help
```

| Option | Default | Description |
| --- | --- | --- |
| `--source` | `sample.mp4` | Local input video path. |
| `--model` | `yolo26m.pt` | Supported model name or local weights path. |
| `--conf` | `0.1` | Detection confidence threshold between 0 and 1. |
| `--device` | Automatic | Inference device, such as `cpu` or `0`. |
| `--width` | `1280` | Display width in pixels; preserves aspect ratio. |
| `--no-display` | Off | Run inference without a video window. |
| `--max-frames` | Entire video | Stop after the specified positive number of frames. |

### Playback controls

With the video window focused, press **Q** or **Escape** to stop. Closing the window also ends playback. **Ctrl+C** in the terminal interrupts processing. Playback ends automatically at the end of the video.

Playback speed includes inference time and a 30 ms display wait per frame; it is not synchronized to the video's original frame rate. There are no pause or seek controls.

### Reading the overlays

A label such as `car #4 87%` shows the detected class, tracking ID, and model confidence score. The center marker and bounding box indicate the object's position.

Only detections with assigned tracking IDs receive overlays. ByteTrack applies its own association thresholds, so a detection may not immediately receive an ID. IDs can change after occlusion or lost tracking and are not permanent object identities. Confidence scores are not calibrated probabilities of correctness.

## Troubleshooting

| Problem | Suggested fix |
| --- | --- |
| Python or an import is missing | Install Python 3.11, create `.venv`, and install `requirements.txt`. Use that environment's interpreter in your terminal or editor. |
| Video not found or cannot be opened | Check `--source`, file permissions, and whether OpenCV supports the video's codec. |
| Model download fails | Check internet access, or download supported weights separately and pass a local path with `--model`. |
| CUDA is unavailable | Check the NVIDIA driver and PyTorch build, or use `--device cpu`. |
| Playback is slow | Try `--model yolo26n.pt` or a compatible GPU. `--width` changes the display size, not inference resolution. |
| OpenCV cannot open a window | Run in a desktop session with `opencv-python`, or use `--no-display`. Avoid installing conflicting OpenCV variants in the same environment. |
| IDs change or objects are missed | Try a different model or threshold and inspect the footage. Motion, lighting, occlusion, and detection quality affect tracking. |

## Development

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests exercise failure handling, resource cleanup, playback controls, and argument validation using mocked video/model interfaces. Automated checks run them on Windows and Linux without downloading weights or requiring a GPU. They do not measure tracking accuracy or replace a desktop/inference check.

See [CONTRIBUTING.md](CONTRIBUTING.md) for reporting bugs and submitting changes.

## Project structure

```text
YOLO-computer-vision-tracker/
|-- .github/workflows/checks.yml  # Automated checks
|-- tests/test_tracker.py        # Control-flow tests
|-- main.py                      # Command-line entry point and viewer
|-- requirements.txt             # Application dependencies
|-- CONTRIBUTING.md
|-- LICENSE
`-- README.md
```

## Limitations

This application processes local video files and displays general object detections. It does not save annotated video, tracking records, or reports. It does not include a webcam interface, training pipeline, or accuracy benchmark. Detection and tracking quality depend on the model and input footage.

## License and acknowledgments

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0-only)**. See [LICENSE](LICENSE) for the full terms.

Built with [Ultralytics YOLO](https://github.com/ultralytics/ultralytics), [OpenCV](https://opencv.org/), and [PyTorch](https://pytorch.org/). Tracking uses Ultralytics' ByteTrack integration. Third-party libraries and pretrained weights retain their respective licenses; see [Ultralytics licensing](https://www.ultralytics.com/license) for its code and models.
