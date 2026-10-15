# Contributing

Bug reports, documentation improvements, and focused pull requests are welcome.

## Development setup

Follow the [README](README.md) to create an environment and install dependencies. Use Python 3.11 for development. Keep videos, weights, generated output, and virtual environments out of commits.

Run the tests from the repository root:

```sh
python -m unittest discover -s tests -v
```

On Windows without environment activation, use `.\.venv\Scripts\python.exe` instead of `python`.

The unit tests use mocked video and model interfaces to exercise argument validation, cleanup, failure handling, and playback controls. They do not measure detection accuracy or require downloaded weights. CI runs these tests on Windows and Linux; inference and desktop compatibility require separate checks.

For changes to detection or tracking, also run a short inference check using a video you have permission to use:

```sh
python main.py --source /path/to/video.mp4 --no-display --max-frames 10
```

For display changes, check Q, Escape, closing the window, and the video's aspect ratio in a desktop session.

## Pull requests and issues

- Describe the problem, what changed, and how you checked it.
- Include your operating system, Python/package versions, command, and error text when reporting a bug.
- Avoid posting private footage, personal paths, credentials, or unlicensed media.
- Keep contributions focused and compatible with the project's AGPL-3.0 license.

By submitting a contribution, you agree to license it under the project's license.
