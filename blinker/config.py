from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RuntimeConfig:
    predictor_path: Path
    camera_index: int = 0
    frame_width: int = 450
    ear_threshold: float = 0.25
    min_consecutive_frames: int = 3
    output_dir: Path = Path(".")
    window_name: str = "Blink Counter"
    draw_overlays: bool = True
    show_fps: bool = True

    def validate(self) -> None:
        if not self.predictor_path.exists():
            raise FileNotFoundError(
                f"Predictor file not found: {self.predictor_path}. "
                "Download shape_predictor_68_face_landmarks.dat and place it in the project root."
            )
        if self.frame_width <= 0:
            raise ValueError("frame_width must be positive")
        if self.ear_threshold <= 0:
            raise ValueError("ear_threshold must be positive")
        if self.min_consecutive_frames <= 0:
            raise ValueError("min_consecutive_frames must be positive")
