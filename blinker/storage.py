import csv
from datetime import datetime
from pathlib import Path

from .analytics import BlinkEvent


class BlinkCsvLogger:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.output_dir / f"blink_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self._file = None
        self._writer = None

    def __enter__(self) -> "BlinkCsvLogger":
        self._file = self.file_path.open("w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        self._writer.writerow(["Timestamp", "Blink_Number", "EAR", "Left_EAR", "Right_EAR"])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._file:
            self._file.close()

    def log_event(self, event: BlinkEvent) -> None:
        if not self._writer or not self._file:
            raise RuntimeError("BlinkCsvLogger must be used as a context manager")
        self._writer.writerow(
            [
                event.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                event.blink_number,
                f"{event.ear:.4f}",
                f"{event.left_ear:.4f}",
                f"{event.right_ear:.4f}",
            ]
        )
        self._file.flush()

    def write_summary(self, session_start: datetime, session_end: datetime, total_blinks: int) -> None:
        if not self._writer:
            raise RuntimeError("BlinkCsvLogger must be used as a context manager")

        duration_seconds = (session_end - session_start).total_seconds()
        self._writer.writerow([])
        self._writer.writerow(["Session Summary"])
        self._writer.writerow(["Start Time", session_start.strftime("%Y-%m-%d %H:%M:%S")])
        self._writer.writerow(["End Time", session_end.strftime("%Y-%m-%d %H:%M:%S")])
        self._writer.writerow(["Duration (seconds)", f"{duration_seconds:.2f}"])
        self._writer.writerow(["Total Blinks", total_blinks])
        if duration_seconds > 0:
            self._writer.writerow(["Blinks Per Minute", f"{(total_blinks / duration_seconds) * 60:.2f}"])
