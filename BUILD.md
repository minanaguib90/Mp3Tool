# Building distributable packages

You get **two packages** in the **project folder**:

- **Windows**: `MP3Tool.exe` – single executable. Build on Windows; the script downloads FFmpeg and copies the exe into the project folder.
- **Mac**: `MP3Tool.app` – application bundle. Build on macOS; the script copies the app into the project folder. **This is a single runnable file**: it contains the app and FFmpeg; distributing **MP3Tool.app** alone is sufficient for Mac users (double-click to run; no extra installs).

Build each package on the **same OS** (Windows exe on Windows, Mac app on Mac). The **.app cannot be built on Windows** (PyInstaller does not cross-compile).

**First time running (for end users):** On Windows, if SmartScreen or antivirus blocks the .exe, use "More info" then "Run anyway". On Mac, if the app is blocked as "unidentified developer", right-click the app and choose **Open** once, then "Open" in the dialog; after that, double-click is enough.

---

## Prerequisites

- Python 3.10+ with the project dependencies installed (`pip install -r requirements.txt`).
- **PyInstaller** (for building only): `pip install -r requirements-build.txt` or `pip install pyinstaller`
- **FFmpeg binaries** placed in the build resources folders (see below).

---

## 1. Bundle FFmpeg

The app needs `ffmpeg` and `ffprobe` inside the package so users don't have to install FFmpeg.

### Windows

1. Download a static Windows build that includes `ffmpeg.exe` and `ffprobe.exe`, e.g.:
   - https://www.gyan.dev/ffmpeg/builds/ → **ffmpeg-release-essentials.zip**
2. Unzip and open the `bin` folder inside.
3. Copy **ffmpeg.exe** and **ffprobe.exe** into:
   ```
   build_resources/ffmpeg_win/
   ```
   That folder must contain exactly these two files (see `build_resources/ffmpeg_win/README.txt`).

### Mac

1. Install FFmpeg (e.g. `brew install ffmpeg`).
2. Copy the binaries into the Mac build resources folder:
   ```bash
   cd /path/to/Mp3Tool
   mkdir -p build_resources/ffmpeg_mac
   cp $(which ffmpeg) build_resources/ffmpeg_mac/
   cp $(which ffprobe) build_resources/ffmpeg_mac/
   ```
   Or use static builds from https://evermeet.cx/ffmpeg/ and put `ffmpeg` and `ffprobe` (no extension) in `build_resources/ffmpeg_mac/`.

---

## 2. Build the Windows .exe (one command)

Run on **Windows** in the project folder:

```bash
cd /path/to/Mp3Tool
python build_windows_exe.py
```

This script will:
- Download FFmpeg Windows binaries (if not already in `build_resources/ffmpeg_win/`)
- Run PyInstaller to build the exe
- Copy **dist/MP3Tool.exe** to the project folder as **MP3Tool.exe**

So after a successful run, **MP3Tool.exe** is in the project folder.

---

## 3. Build the Mac .app (one command, on macOS only)

Run on **macOS** in the project folder:

```bash
cd /path/to/Mp3Tool
chmod +x build_mac_app.sh
./build_mac_app.sh
```

To rebuild with the latest fixes (e.g. audioop-lts for Python 3.13), run the same script on macOS; it installs dependencies and builds **MP3Tool.app** and **MP3Tool-mac.zip**.

The script will:
- Copy `ffmpeg` and `ffprobe` from your Mac (e.g. from `brew install ffmpeg`) into `build_resources/ffmpeg_mac/` if needed
- Run PyInstaller to build the app
- Copy **dist/MP3Tool.app** to the project folder as **MP3Tool.app**

So after a successful run, **MP3Tool.app** is in the project folder. Drag it to Applications or run it from anywhere. No Python or FFmpeg installation required for end users. **MP3Tool.app** is the single file Mac users need; you can distribute it as-is. The script also creates **MP3Tool-mac.zip** (one downloadable file containing the .app) in the project folder.

Optional: create a .dmg for distribution (e.g. using "Disk Utility" → New Image → drag MP3Tool.app into it, or use a tool like create-dmg).

---

## Summary

| Package   | Build on | Command / script           | Result in project folder   |
|----------|----------|----------------------------|-----------------------------|
| Windows  | Windows  | `python build_windows_exe.py` | **MP3Tool.exe**             |
| Mac      | Mac      | `./build_mac_app.sh`       | **MP3Tool.app**, **MP3Tool-mac.zip** |

Each package includes FFmpeg; end users do not need to install it. On Mac, **MP3Tool.app** is the single runnable file; **MP3Tool-mac.zip** is an optional one-file download containing it. The .app **must** be built on a Mac; it cannot be produced on Windows.
