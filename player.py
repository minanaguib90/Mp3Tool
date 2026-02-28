"""
Simple MP3 playback using pygame.mixer.
Supports load, play, pause, stop, seek, and get_position_ms.
"""
from pathlib import Path

import pygame


class Player:
    def __init__(self) -> None:
        self._path: Path | None = None
        self._base_secs: float = 0.0
        self._paused: bool = False
        self._initialized = False

    def _ensure_init(self) -> None:
        if not self._initialized:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._initialized = True

    def load(self, path: str | Path) -> None:
        """Load an MP3 file for playback."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        self._ensure_init()
        pygame.mixer.music.load(str(path))
        self._path = path
        self._base_secs = 0.0
        self._paused = False

    def play(self) -> None:
        """Start or resume playback."""
        if self._path is None:
            return
        self._ensure_init()
        if self._paused:
            pygame.mixer.music.play(start=self._base_secs)
            self._paused = False
        else:
            pygame.mixer.music.play(start=self._base_secs)

    def pause(self) -> None:
        """Pause playback and remember position."""
        if self._path is None:
            return
        if self._paused:
            return
        self._base_secs = self._base_secs + pygame.mixer.music.get_pos()
        pygame.mixer.music.pause()
        self._paused = True

    def unpause(self) -> None:
        """Resume from paused state."""
        if self._path is None:
            return
        if not self._paused:
            return
        pygame.mixer.music.unpause()
        self._paused = False

    def stop(self) -> None:
        """Stop playback and reset position to start."""
        if self._path is None:
            return
        pygame.mixer.music.stop()
        self._base_secs = 0.0
        self._paused = False

    def seek(self, position_ms: int) -> None:
        """Seek to position in milliseconds."""
        if self._path is None:
            return
        position_secs = max(0, position_ms / 1000.0)
        self._base_secs = position_secs
        self._paused = False
        pygame.mixer.music.play(start=position_secs)

    def get_position_ms(self) -> int:
        """Current playback position in milliseconds."""
        if self._path is None:
            return 0
        if self._paused:
            return int(self._base_secs * 1000)
        return int((self._base_secs + pygame.mixer.music.get_pos()) * 1000)

    def is_playing(self) -> bool:
        """True if currently playing (not paused and not stopped)."""
        if self._path is None:
            return False
        return not self._paused and pygame.mixer.music.get_busy()

    def is_paused(self) -> bool:
        return self._paused

    @property
    def path(self) -> Path | None:
        return self._path
