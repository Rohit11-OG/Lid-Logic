import argparse
from pathlib import Path

from .app import BlinkCounterApp
from .config import RuntimeConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Real-time eye blink counter using OpenCV + dlib.")
    parser.add_argument(
        "--predictor-path",
        type=Path,
        default=Path("shape_predictor_68_face_landmarks.dat"),
        help="Path to shape_predictor_68_face_landmarks.dat",
    )
    parser.add_argument("--camera-index", type=int, default=0, help="Webcam index for cv2.VideoCapture.")
    parser.add_argument("--frame-width", type=int, default=450, help="Frame width for resize processing.")
    parser.add_argument("--ear-threshold", type=float, default=0.25, help="EAR threshold for closed eyes.")
    parser.add_argument(
        "--min-consecutive-frames",
        type=int,
        default=3,
        help="Minimum consecutive closed-eye frames to count as one blink.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory to write blink_stats_*.csv output files.",
    )
    parser.add_argument(
        "--no-fps",
        action="store_true",
        help="Disable FPS text overlay.",
    )
    parser.add_argument(
        "--no-overlays",
        action="store_true",
        help="Disable eye contour and face rectangle overlays.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = RuntimeConfig(
        predictor_path=args.predictor_path,
        camera_index=args.camera_index,
        frame_width=args.frame_width,
        ear_threshold=args.ear_threshold,
        min_consecutive_frames=args.min_consecutive_frames,
        output_dir=args.output_dir,
        show_fps=not args.no_fps,
        draw_overlays=not args.no_overlays,
    )

    app = BlinkCounterApp(config)
    summary = app.run()
    print(f"Total blinks detected: {summary.total_blinks}")
    print(f"Session duration (seconds): {summary.duration_seconds:.2f}")
    print(f"Stats saved to: {summary.csv_file}")
    return 0
