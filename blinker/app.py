from dataclasses import dataclass
from datetime import datetime
from time import perf_counter

import cv2
import dlib
import imutils
from imutils import face_utils

from .analytics import BlinkTracker, eye_aspect_ratio
from .config import RuntimeConfig
from .storage import BlinkCsvLogger


@dataclass(slots=True)
class SessionSummary:
    total_blinks: int
    started_at: datetime
    ended_at: datetime
    csv_file: str

    @property
    def duration_seconds(self) -> float:
        return (self.ended_at - self.started_at).total_seconds()


class BlinkCounterApp:
    def __init__(self, config: RuntimeConfig) -> None:
        self.config = config
        self.config.validate()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(str(self.config.predictor_path))
        self.left_start, self.left_end = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.right_start, self.right_end = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        self.tracker = BlinkTracker(
            ear_threshold=self.config.ear_threshold,
            min_consecutive_frames=self.config.min_consecutive_frames,
        )

    def run(self) -> SessionSummary:
        started_at = datetime.now()
        frame_count = 0
        t0 = perf_counter()
        cap = cv2.VideoCapture(self.config.camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Unable to open camera index {self.config.camera_index}")

        with BlinkCsvLogger(self.config.output_dir) as csv_logger:
            try:
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break

                    frame_count += 1
                    frame = imutils.resize(frame, width=self.config.frame_width)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.detector(gray, 0)

                    for face in faces:
                        shape = self.predictor(gray, face)
                        shape = face_utils.shape_to_np(shape)
                        left_eye = shape[self.left_start : self.left_end]
                        right_eye = shape[self.right_start : self.right_end]

                        left_ear = eye_aspect_ratio(left_eye)
                        right_ear = eye_aspect_ratio(right_eye)
                        ear = (left_ear + right_ear) / 2.0

                        event = self.tracker.update(
                            ear=ear,
                            left_ear=left_ear,
                            right_ear=right_ear,
                        )
                        if event:
                            csv_logger.log_event(event)

                        if self.config.draw_overlays:
                            left_hull = cv2.convexHull(left_eye)
                            right_hull = cv2.convexHull(right_eye)
                            cv2.drawContours(frame, [left_hull], -1, (0, 255, 0), 1)
                            cv2.drawContours(frame, [right_hull], -1, (0, 255, 0), 1)
                            x, y, w, h = face_utils.rect_to_bb(face)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(
                                frame,
                                f"EAR: {ear:.2f}",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 0, 255),
                                2,
                            )

                    cv2.putText(
                        frame,
                        f"Blinks: {self.tracker.total_blinks}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2,
                    )
                    if self.config.show_fps:
                        elapsed = max(perf_counter() - t0, 1e-6)
                        fps = frame_count / elapsed
                        cv2.putText(
                            frame,
                            f"FPS: {fps:.1f}",
                            (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2,
                        )

                    cv2.imshow(self.config.window_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
            finally:
                cap.release()
                cv2.destroyAllWindows()

            ended_at = datetime.now()
            csv_logger.write_summary(started_at, ended_at, self.tracker.total_blinks)
            return SessionSummary(
                total_blinks=self.tracker.total_blinks,
                started_at=started_at,
                ended_at=ended_at,
                csv_file=str(csv_logger.file_path),
            )
