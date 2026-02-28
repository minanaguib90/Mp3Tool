"""
Download FFmpeg Windows binaries, then build MP3Tool.exe and place it in the project folder.
Run on Windows: python build_windows_exe.py
"""
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
FFMPEG_WIN_DIR = PROJECT_DIR / "build_resources" / "ffmpeg_win"
FFMPEG_ZIP_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_ZIP = PROJECT_DIR / "ffmpeg-download.zip"
EXTRACT_DIR = PROJECT_DIR / "ffmpeg-extract"


def download_ffmpeg() -> None:
    FFMPEG_WIN_DIR.mkdir(parents=True, exist_ok=True)
    if (FFMPEG_WIN_DIR / "ffmpeg.exe").exists() and (FFMPEG_WIN_DIR / "ffprobe.exe").exists():
        print("FFmpeg binaries already present in build_resources/ffmpeg_win/")
        return
    print("Downloading FFmpeg Windows build...")
    urllib.request.urlretrieve(FFMPEG_ZIP_URL, FFMPEG_ZIP)
    print("Extracting...")
    with zipfile.ZipFile(FFMPEG_ZIP, "r") as z:
        z.extractall(EXTRACT_DIR)
    # Find bin/ containing ffmpeg.exe (BtbN zip: ffmpeg-master-latest-win64-gpl/bin/)
    bin_dir = None
    for root, dirs, files in os.walk(EXTRACT_DIR):
        if "ffmpeg.exe" in files and "ffprobe.exe" in files:
            bin_dir = Path(root)
            break
    if not bin_dir:
        raise FileNotFoundError("Could not find ffmpeg.exe and ffprobe.exe in extracted archive")
    for name in ("ffmpeg.exe", "ffprobe.exe"):
        src = bin_dir / name
        shutil.copy2(src, FFMPEG_WIN_DIR / name)
    shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
    FFMPEG_ZIP.unlink(missing_ok=True)
    print("FFmpeg binaries ready in build_resources/ffmpeg_win/")


def build_exe() -> None:
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--noconfirm", "build_windows.spec"],
        cwd=PROJECT_DIR,
        check=True,
    )
    exe_src = PROJECT_DIR / "dist" / "MP3Tool.exe"
    exe_dest = PROJECT_DIR / "MP3Tool.exe"
    if exe_src.exists():
        shutil.copy2(exe_src, exe_dest)
        print(f"Built: {exe_dest}")
    else:
        print("Build completed but MP3Tool.exe not found in dist/")


def main() -> None:
    if sys.platform != "win32":
        print("This script is for Windows. Use build_mac_app.sh on macOS for the .app.")
        sys.exit(1)
    os.chdir(PROJECT_DIR)
    download_ffmpeg()
    build_exe()


if __name__ == "__main__":
    main()
