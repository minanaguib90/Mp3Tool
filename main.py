"""
MP3 Tool – main window: player, volume boost export, sample export.
"""
import os
import sys
from pathlib import Path

# When built with PyInstaller, add bundled ffmpeg to PATH so processor and pydub find it
if getattr(sys, "frozen", False):
    _base = getattr(sys, "_MEIPASS", None) or Path(__file__).resolve().parent
    if _base:
        _ffmpeg_dir = Path(_base) / ("ffmpeg_win" if sys.platform == "win32" else "ffmpeg_mac")
        if _ffmpeg_dir.exists():
            os.environ["PATH"] = str(_ffmpeg_dir) + os.pathsep + os.environ.get("PATH", "")

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSlider,
    QWidget,
)

from player import Player
from processor import (
    check_ffmpeg,
    export_sample,
    export_volume_boost,
    load as load_audio,
    parse_mm_ss,
)


def ms_to_mm_ss(ms: int) -> str:
    """Convert milliseconds to M:SS or MM:SS."""
    total_secs = max(0, ms // 1000)
    m = total_secs // 60
    s = total_secs % 60
    return f"{m}:{s:02d}"


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MP3 Tool")
        self.setAcceptDrops(True)
        self.setMinimumWidth(420)

        self._player = Player()
        self._audio: object | None = None  # pydub AudioSegment
        self._current_path: Path | None = None
        self._duration_ms = 0
        self._ffmpeg_ok = check_ffmpeg()
        self._slider_dragging = False

        layout = QGridLayout(self)

        # File section
        row = 0
        self._open_btn = QPushButton("Open MP3")
        self._open_btn.clicked.connect(self._on_open)
        layout.addWidget(self._open_btn, row, 0, 1, 2)

        row += 1
        self._file_label = QLabel("No file loaded")
        self._file_label.setStyleSheet("color: gray;")
        layout.addWidget(self._file_label, row, 0, 1, 2)

        # Playback
        row += 1
        self._play_btn = QPushButton("Play")
        self._play_btn.clicked.connect(self._on_play)
        self._pause_btn = QPushButton("Pause")
        self._pause_btn.clicked.connect(self._on_pause)
        self._stop_btn = QPushButton("Stop")
        self._stop_btn.clicked.connect(self._on_stop)
        layout.addWidget(self._play_btn, row, 0)
        layout.addWidget(self._pause_btn, row, 1)

        row += 1
        layout.addWidget(self._stop_btn, row, 0, 1, 2)

        row += 1
        self._position_slider = QSlider(Qt.Orientation.Horizontal)
        self._position_slider.setMinimum(0)
        self._position_slider.setMaximum(1000)
        self._position_slider.setValue(0)
        self._position_slider.sliderPressed.connect(lambda: setattr(self, "_slider_dragging", True))
        self._position_slider.sliderReleased.connect(self._on_slider_released)
        self._position_slider.valueChanged.connect(self._on_slider_value_changed)
        layout.addWidget(self._position_slider, row, 0, 1, 2)

        row += 1
        self._time_label = QLabel("0:00 / 0:00")
        self._time_label.setStyleSheet("color: gray;")
        layout.addWidget(self._time_label, row, 0, 1, 2)

        # Volume increase
        row += 1
        layout.addWidget(QLabel("Volume % (100–1000):"), row, 0)
        self._volume_input = QLineEdit()
        self._volume_input.setPlaceholderText("e.g. 101 = +1%")
        layout.addWidget(self._volume_input, row, 1)

        row += 1
        self._export_volume_btn = QPushButton("Export with increased volume")
        self._export_volume_btn.clicked.connect(self._on_export_volume)
        layout.addWidget(self._export_volume_btn, row, 0, 1, 2)

        # Cut sample
        row += 1
        layout.addWidget(QLabel("Start (MM:SS):"), row, 0)
        self._start_input = QLineEdit()
        self._start_input.setPlaceholderText("0:00")
        layout.addWidget(self._start_input, row, 1)

        row += 1
        layout.addWidget(QLabel("End (MM:SS):"), row, 0)
        self._end_input = QLineEdit()
        self._end_input.setPlaceholderText("0:00")
        layout.addWidget(self._end_input, row, 1)

        row += 1
        self._export_sample_btn = QPushButton("Export sample")
        self._export_sample_btn.clicked.connect(self._on_export_sample)
        layout.addWidget(self._export_sample_btn, row, 0, 1, 2)

        if not self._ffmpeg_ok:
            QMessageBox.warning(
                self,
                "FFmpeg not found",
                "FFmpeg is not installed or not on PATH. Export (volume boost and sample) will not work until FFmpeg is installed.",
            )
            self._export_volume_btn.setEnabled(False)
            self._export_sample_btn.setEnabled(False)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_position)
        self._timer.start(200)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and Path(urls[0].toLocalFile()).suffix.lower() == ".mp3":
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if not urls:
            return
        path = Path(urls[0].toLocalFile())
        if path.suffix.lower() != ".mp3" or not path.exists():
            QMessageBox.warning(self, "Invalid file", "Please drop a valid MP3 file.")
            return
        self._load_file(path)

    def _load_file(self, path: Path) -> None:
        try:
            self._audio = load_audio(path)
            self._duration_ms = len(self._audio)
            self._player.load(path)
            self._current_path = path
            self._file_label.setText(path.name)
            self._file_label.setStyleSheet("")
            self._position_slider.setMaximum(max(1, self._duration_ms))
            self._position_slider.setValue(0)
            self._time_label.setText(f"0:00 / {ms_to_mm_ss(self._duration_ms)}")
            if self._ffmpeg_ok:
                self._export_volume_btn.setEnabled(True)
                self._export_sample_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load file:\n{e}")

    def _on_open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open MP3", "", "MP3 files (*.mp3);;All files (*)"
        )
        if path:
            self._load_file(Path(path))

    def _on_play(self) -> None:
        if self._current_path is None:
            QMessageBox.information(self, "No file", "Open an MP3 file first.")
            return
        if self._player.is_paused():
            self._player.unpause()
        else:
            self._player.play()

    def _on_pause(self) -> None:
        if self._current_path is None:
            return
        self._player.pause()

    def _on_stop(self) -> None:
        if self._current_path is None:
            return
        self._player.stop()
        self._position_slider.setValue(0)
        self._time_label.setText(f"0:00 / {ms_to_mm_ss(self._duration_ms)}")

    def _on_slider_released(self) -> None:
        if self._slider_dragging and self._current_path is not None:
            ms = self._position_slider.value()
            self._player.seek(ms)
        self._slider_dragging = False

    def _on_slider_value_changed(self, value: int) -> None:
        if self._slider_dragging:
            return
        self._time_label.setText(f"{ms_to_mm_ss(value)} / {ms_to_mm_ss(self._duration_ms)}")

    def _update_position(self) -> None:
        if self._current_path is None or self._slider_dragging:
            return
        pos = self._player.get_position_ms()
        if pos != self._position_slider.value():
            self._position_slider.blockSignals(True)
            self._position_slider.setValue(min(pos, self._duration_ms))
            self._position_slider.blockSignals(False)
            self._time_label.setText(f"{ms_to_mm_ss(pos)} / {ms_to_mm_ss(self._duration_ms)}")
        if not self._player.is_playing() and not self._player.is_paused() and pos >= self._duration_ms > 0:
            self._position_slider.setValue(0)
            self._time_label.setText(f"0:00 / {ms_to_mm_ss(self._duration_ms)}")

    def _on_export_volume(self) -> None:
        if self._audio is None or self._current_path is None:
            QMessageBox.information(self, "No file", "Open an MP3 file first.")
            return
        if not self._ffmpeg_ok:
            return
        raw = self._volume_input.text().strip()
        if not raw:
            QMessageBox.warning(self, "Invalid input", "Enter a volume percentage (100–1000).")
            return
        try:
            pct = int(raw)
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Volume must be a number between 100 and 1000.")
            return
        if pct < 100 or pct > 1000:
            QMessageBox.warning(self, "Invalid input", "Volume must be between 100 and 1000.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save as", str(self._current_path.parent), "MP3 files (*.mp3);;All files (*)"
        )
        if not path:
            return
        if not path.lower().endswith(".mp3"):
            path += ".mp3"
        try:
            factor = pct / 100.0
            export_volume_boost(self._audio, factor, path, source_path=self._current_path)
            QMessageBox.information(self, "Done", f"Exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))

    def _on_export_sample(self) -> None:
        if self._audio is None or self._current_path is None:
            QMessageBox.information(self, "No file", "Open an MP3 file first.")
            return
        if not self._ffmpeg_ok:
            return
        start_str = self._start_input.text().strip()
        end_str = self._end_input.text().strip()
        if not start_str or not end_str:
            QMessageBox.warning(self, "Invalid input", "Enter start and end time as MM:SS.")
            return
        try:
            start_secs = parse_mm_ss(start_str)
            end_secs = parse_mm_ss(end_str)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid time", str(e))
            return
        start_ms = start_secs * 1000
        end_ms = end_secs * 1000
        if start_ms >= end_ms:
            QMessageBox.warning(self, "Invalid range", "Start must be before end.")
            return
        if end_ms > self._duration_ms:
            QMessageBox.warning(
                self,
                "Invalid range",
                f"End time exceeds track length ({ms_to_mm_ss(self._duration_ms)}).",
            )
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save sample as", str(self._current_path.parent), "MP3 files (*.mp3);;All files (*)"
        )
        if not path:
            return
        if not path.lower().endswith(".mp3"):
            path += ".mp3"
        try:
            export_sample(self._audio, start_ms, end_ms, path, source_path=self._current_path)
            QMessageBox.information(self, "Done", f"Exported sample to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))


def main() -> None:
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
