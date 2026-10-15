# SPDX-License-Identifier: AGPL-3.0-only
"""Detect and track objects in a local video with YOLO and ByteTrack."""

import argparse
from pathlib import Path
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("sample.mp4"),
                        help="input video path (default: sample.mp4)")
    parser.add_argument("--model", default="yolo26m.pt",
                        help="Ultralytics model name or weights path (default: yolo26m.pt)")
    parser.add_argument("--conf", type=float, default=0.1,
                        help="detection confidence threshold, from 0 to 1 (default: 0.1)")
    parser.add_argument("--device", default=None,
                        help="inference device, e.g. cpu or 0 for the first CUDA GPU (default: auto)")
    parser.add_argument("--width", type=int, default=1280,
                        help="display width in pixels; aspect ratio is preserved (default: 1280)")
    parser.add_argument("--no-display", action="store_true",
                        help="process the video without opening a window")
    parser.add_argument("--max-frames", type=int, default=None,
                        help="stop after this many frames (default: entire video)")
    args = parser.parse_args(argv)
    if not 0 <= args.conf <= 1:
        parser.error("--conf must be between 0 and 1")
    if args.width <= 0:
        parser.error("--width must be positive")
    if args.max_frames is not None and args.max_frames <= 0:
        parser.error("--max-frames must be positive")
    return args


def draw_tracks(cv2, frame, result, names):
    """Draw labels only for detections assigned a tracking ID."""
    boxes = result.boxes
    if boxes is None or boxes.id is None:
        return
    for coords, track_id, class_id, confidence in zip(
        boxes.xyxy, boxes.id, boxes.cls, boxes.conf
    ):
        x1, y1, x2, y2 = map(int, coords.tolist())
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        label = f"{names[int(class_id.item())]} #{int(track_id.item())} {float(confidence.item()):.0%}"
        cv2.circle(frame, center, 12, (0, 255, 0), 3)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 120, 50), 3)
        cv2.putText(frame, label, (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)


def run(args):
    source = args.source.expanduser()
    if not source.is_file():
        raise FileNotFoundError(
            f"Video not found: {source}. Provide a local video with --source PATH."
        )

    # Import heavy dependencies only when running inference, so --help is lightweight.
    import cv2
    from ultralytics import YOLO

    video = cv2.VideoCapture(str(source))
    processed = 0
    window = "YOLO Video Tracker"
    try:
        if not video.isOpened():
            raise RuntimeError(f"Cannot open video: {source}. Check the file and video codec.")
        model = YOLO(args.model)
        if not args.no_display:
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        while args.max_frames is None or processed < args.max_frames:
            success, frame = video.read()
            if not success:
                if processed == 0:
                    raise RuntimeError(f"Cannot read any frames from video: {source}")
                break
            results = model.track(
                frame, persist=True, tracker="bytetrack.yaml", conf=args.conf,
                device=args.device, verbose=False,
            )
            processed += 1
            if args.no_display:
                continue
            draw_tracks(cv2, frame, results[0], model.names)
            height = max(1, round(frame.shape[0] * args.width / frame.shape[1]))
            display = cv2.resize(frame, (args.width, height))
            cv2.imshow(window, display)
            if cv2.waitKey(30) & 0xFF in (ord("q"), ord("Q"), 27):
                break
            if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        video.release()
        if not args.no_display:
            cv2.destroyAllWindows()
    print(f"Processed {processed} frame(s).")
    return processed


def main(argv=None):
    args = parse_args(argv)
    try:
        run(args)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
