"""
MP3 processing: load, volume boost export, trim export.
Uses pydub (requires ffmpeg on PATH). Preserves source bitrate when exporting.
"""
import math
import shutil
import subprocess
from pathlib import Path

from pydub import AudioSegment


def check_ffmpeg() -> bool:
    """Return True if ffmpeg is available on PATH."""
    return shutil.which("ffmpeg") is not None


def _get_bitrate_kbps(path: Path) -> str | None:
    """Get audio bitrate of file in kbps (e.g. '192') using ffprobe, or None on failure."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    try:
        out = subprocess.run(
            [
                ffprobe,
                "-v", "error",
                "-select_streams", "a:0",
                "-show_entries", "format=bit_rate",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode != 0 or not out.stdout.strip():
            return None
        bit_rate_bps = int(out.stdout.strip())
        return str(max(1, bit_rate_bps // 1000))
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def load(path: str | Path) -> AudioSegment:
    """Load an MP3 file and return the AudioSegment."""
    path = Path(path)
    if not path.suffix.lower() == ".mp3":
        raise ValueError("File must be an MP3")
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return AudioSegment.from_mp3(str(path))


def export_volume_boost(
    audio: AudioSegment,
    factor: float,
    out_path: str | Path,
    source_path: str | Path | None = None,
) -> None:
    """
    Apply volume boost by factor (e.g. 1.01 for +1%), export as MP3.
    If source_path is given, tries to preserve source bitrate.
    """
    out_path = Path(out_path)
    gain_db = 20 * math.log10(factor)
    boosted = audio + gain_db

    bitrate = None
    if source_path:
        bitrate = _get_bitrate_kbps(Path(source_path))
    if bitrate:
        boosted.export(str(out_path), format="mp3", bitrate=f"{bitrate}k")
    else:
        boosted.export(str(out_path), format="mp3")


def export_sample(
    audio: AudioSegment,
    start_ms: int,
    end_ms: int,
    out_path: str | Path,
    source_path: str | Path | None = None,
) -> None:
    """
    Export the segment [start_ms, end_ms) as a new MP3.
    If source_path is given, tries to preserve source bitrate.
    """
    out_path = Path(out_path)
    segment = audio[start_ms:end_ms]

    bitrate = None
    if source_path:
        bitrate = _get_bitrate_kbps(Path(source_path))
    if bitrate:
        segment.export(str(out_path), format="mp3", bitrate=f"{bitrate}k")
    else:
        segment.export(str(out_path), format="mp3")


def parse_mm_ss(s: str) -> int:
    """
    Parse a string 'M:SS' or 'MM:SS' to seconds.
    Raises ValueError if invalid.
    """
    s = s.strip()
    if ":" not in s:
        raise ValueError("Expected MM:SS or M:SS")
    parts = s.split(":")
    if len(parts) != 2:
        raise ValueError("Expected MM:SS or M:SS")
    try:
        minutes = int(parts[0].strip())
        seconds = int(parts[1].strip())
    except ValueError:
        raise ValueError("Minutes and seconds must be numbers")
    if minutes < 0 or seconds < 0 or seconds >= 60:
        raise ValueError("Invalid time (seconds must be 0-59)")
    return minutes * 60 + seconds
