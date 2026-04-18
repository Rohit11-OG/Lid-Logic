from dataclasses import dataclass
from datetime import datetime

import numpy as np
from scipy.spatial import distance as dist


def eye_aspect_ratio(eye: np.ndarray) -> float:
    """Compute EAR from six eye landmark points."""
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])
    c = dist.euclidean(eye[0], eye[3])
    if c == 0:
        return 0.0
    return (a + b) / (2.0 * c)


@dataclass(slots=True)
class BlinkEvent:
    timestamp: datetime
    blink_number: int
    ear: float
    left_ear: float
    right_ear: float


class BlinkTracker:
    def __init__(self, ear_threshold: float, min_consecutive_frames: int) -> None:
        self.ear_threshold = ear_threshold
        self.min_consecutive_frames = min_consecutive_frames
        self.closed_frame_count = 0
        self.total_blinks = 0

    def update(
        self,
        ear: float,
        left_ear: float,
        right_ear: float,
        timestamp: datetime | None = None,
    ) -> BlinkEvent | None:
        if ear < self.ear_threshold:
            self.closed_frame_count += 1
            return None

        event = None
        if self.closed_frame_count >= self.min_consecutive_frames:
            self.total_blinks += 1
            event = BlinkEvent(
                timestamp=timestamp or datetime.now(),
                blink_number=self.total_blinks,
                ear=ear,
                left_ear=left_ear,
                right_ear=right_ear,
            )

        self.closed_frame_count = 0
        return event
