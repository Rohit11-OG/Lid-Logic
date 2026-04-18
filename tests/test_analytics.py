from datetime import datetime

import numpy as np

from blinker.analytics import BlinkTracker, eye_aspect_ratio


def test_eye_aspect_ratio_computation() -> None:
    eye = np.array(
        [
            [0.0, 0.0],
            [1.0, 2.0],
            [2.0, 2.0],
            [4.0, 0.0],
            [2.0, -2.0],
            [1.0, -2.0],
        ]
    )
    assert eye_aspect_ratio(eye) == 1.0


def test_blink_tracker_emits_event_after_min_consecutive_frames() -> None:
    tracker = BlinkTracker(ear_threshold=0.25, min_consecutive_frames=3)
    now = datetime(2026, 1, 1, 12, 0, 0)

    assert tracker.update(0.2, 0.2, 0.2, now) is None
    assert tracker.update(0.18, 0.18, 0.18, now) is None
    assert tracker.update(0.19, 0.19, 0.19, now) is None
    event = tracker.update(0.3, 0.3, 0.3, now)

    assert event is not None
    assert event.blink_number == 1
    assert tracker.total_blinks == 1


def test_blink_tracker_ignores_short_eye_closures() -> None:
    tracker = BlinkTracker(ear_threshold=0.25, min_consecutive_frames=3)
    now = datetime(2026, 1, 1, 12, 0, 0)

    assert tracker.update(0.2, 0.2, 0.2, now) is None
    assert tracker.update(0.2, 0.2, 0.2, now) is None
    assert tracker.update(0.3, 0.3, 0.3, now) is None
    assert tracker.total_blinks == 0
