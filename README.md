# Lid-Logic

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/Rohit11-OG/Lid-Logic/releases/tag/v1.0.0)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-3%20passing-brightgreen)](https://github.com/Rohit11-OG/Lid-Logic)

Real-time eye blink detection and session analytics using OpenCV + dlib facial landmarks.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for version history and release notes.

## What is improved

- Modular package structure instead of one long script
- Configurable CLI arguments for camera, threshold, frame width, and output directory
- Session summary and per-blink CSV logging through a dedicated logger
- Testable core blink logic (`BlinkTracker`) with unit tests
- Installable Python project via `pyproject.toml`

## Project layout

```text
blink_counter.py          # Backward-compatible runner
blinker/
  analytics.py            # EAR calculation and blink state machine
  app.py                  # Main runtime loop
  cli.py                  # Argument parser and app bootstrap
  config.py               # Runtime config + validation
  storage.py              # CSV event + summary writer
tests/
  test_analytics.py       # Unit tests for blink logic
```

## Setup

### 1) Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

or install as a package:

```bash
pip install -e .[dev]
```

### 3) Ensure predictor model exists

Required file:
- `shape_predictor_68_face_landmarks.dat`

If needed, download from:
- http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Extract the `.bz2` and keep the `.dat` file in the project root (or pass a custom path with `--predictor-path`).

## Run

### Simple

```bash
python blink_counter.py
```

### Advanced options

```bash
python blink_counter.py --camera-index 0 --ear-threshold 0.23 --min-consecutive-frames 3 --frame-width 500 --output-dir logs
```

Press `q` to quit.

## CLI options

- `--predictor-path`: Path to `shape_predictor_68_face_landmarks.dat`
- `--camera-index`: Webcam index (default: `0`)
- `--frame-width`: Resize width for processing speed (default: `450`)
- `--ear-threshold`: Lower = stricter blink detection (default: `0.25`)
- `--min-consecutive-frames`: Closed-eye frames needed for one blink (default: `3`)
- `--output-dir`: Where `blink_stats_*.csv` is written (default: current directory)
- `--no-fps`: Disable FPS overlay
- `--no-overlays`: Disable eye contour/face rectangle overlays

## Test

```bash
pytest
```

## Troubleshooting

### dlib install fails on Windows

- Install Visual Studio Build Tools with C++ workload
- Install CMake and add it to `PATH`
- Or use conda: `conda install -c conda-forge dlib`

### Camera not detected

- Try another index: `--camera-index 1`
- Confirm camera access permissions

### Predictor file error

- Validate path exists
- Pass custom model path explicitly using `--predictor-path`
