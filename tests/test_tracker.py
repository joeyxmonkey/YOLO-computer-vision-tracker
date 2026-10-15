# SPDX-License-Identifier: AGPL-3.0-only
"""Control-flow tests; no model download, video assets, or GPU required."""

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import main


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "video.mp4"
        self.source.touch()
        self.cv2 = MagicMock()
        self.video = self.cv2.VideoCapture.return_value
        self.video.isOpened.return_value = True
        self.frame = SimpleNamespace(shape=(720, 1280, 3))
        self.video.read.side_effect = [(True, self.frame), (False, None)]
        self.ultralytics = MagicMock()
        self.model = self.ultralytics.YOLO.return_value
        self.model.track.return_value = [SimpleNamespace(boxes=None)]
        self.modules = patch.dict("sys.modules", {
            "cv2": self.cv2, "ultralytics": self.ultralytics,
        })
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.stdout = redirect_stdout(io.StringIO())
        self.stdout.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)

    def args(self, *extra):
        return main.parse_args(["--source", str(self.source), *extra])

    def test_frame_limit_preserves_tracking_and_releases_video(self):
        self.assertEqual(main.run(self.args("--no-display", "--max-frames", "1")), 1)
        self.model.track.assert_called_once_with(
            self.frame, persist=True, tracker="bytetrack.yaml", conf=0.1,
            device=None, verbose=False,
        )
        self.video.read.assert_called_once()
        self.video.release.assert_called_once()
        self.cv2.imshow.assert_not_called()
        self.cv2.destroyAllWindows.assert_not_called()

    def test_unreadable_video_releases_capture_before_loading_model(self):
        self.video.isOpened.return_value = False
        with self.assertRaisesRegex(RuntimeError, "Cannot open video"):
            main.run(self.args("--no-display"))
        self.video.release.assert_called_once()
        self.ultralytics.YOLO.assert_not_called()

    def test_empty_video_reports_error(self):
        self.video.read.side_effect = [(False, None)]
        with self.assertRaisesRegex(RuntimeError, "Cannot read any frames"):
            main.run(self.args("--no-display"))
        self.video.release.assert_called_once()

    def test_inference_failure_still_cleans_up(self):
        self.model.track.side_effect = RuntimeError("inference failed")
        with self.assertRaisesRegex(RuntimeError, "inference failed"):
            main.run(self.args())
        self.video.release.assert_called_once()
        self.cv2.destroyAllWindows.assert_called_once()

    def test_quit_key_preserves_aspect_ratio_and_cleans_up(self):
        self.cv2.waitKey.return_value = ord("q")
        self.assertEqual(main.run(self.args("--width", "640")), 1)
        self.cv2.resize.assert_called_once_with(self.frame, (640, 360))
        self.video.release.assert_called_once()
        self.cv2.destroyAllWindows.assert_called_once()

    def test_closing_window_stops_playback(self):
        self.cv2.waitKey.return_value = -1
        self.cv2.getWindowProperty.return_value = 0
        self.assertEqual(main.run(self.args()), 1)
        self.video.release.assert_called_once()
        self.cv2.destroyAllWindows.assert_called_once()

    def test_missing_file_returns_failure_without_loading_dependencies(self):
        with redirect_stderr(io.StringIO()) as errors:
            code = main.main(["--source", str(self.source.with_name("missing.mp4"))])
        self.assertEqual(code, 1)
        self.assertIn("--source", errors.getvalue())
        self.cv2.VideoCapture.assert_not_called()

    def test_invalid_options_fail_before_inference(self):
        for options in [("--conf", "1.1"), ("--conf", "nan"),
                        ("--width", "0"), ("--max-frames", "-1")]:
            with self.subTest(options=options), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    self.args(*options)
                self.assertEqual(error.exception.code, 2)
        self.ultralytics.YOLO.assert_not_called()


if __name__ == "__main__":
    unittest.main()
