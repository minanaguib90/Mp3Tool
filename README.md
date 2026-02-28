# MP3 Tool – Player, Volume Boost & Sample Export

A simple cross-platform (Windows and Mac) desktop app to load one MP3, play it, increase volume (100–1000%), or cut a sample and export as new MP3 files.

**Repository:** [github.com/minanaguib90/Mp3Tool](https://github.com/minanaguib90/Mp3Tool)

## Mac users: build and run the app on your MacBook

See **[MAC_DEPLOY.md](MAC_DEPLOY.md)** for step-by-step instructions to clone this repo and build **MP3Tool.app** on your Mac. You get a single app you can double-click to run (no Python or FFmpeg install required for end users).

---

## Requirements

- **Python 3.10+**
- **FFmpeg** – must be installed and available on your PATH (used for reading/writing MP3).

### Install FFmpeg

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install ffmpeg`, then ensure the `ffmpeg` binary is on your PATH.
- **Mac**: `brew install ffmpeg`

## Setup

1. Create a virtual environment (recommended):

   ```bash
   cd /path/to/Mp3Tool   # or your project folder
   python -m venv venv
   ```

2. Activate it:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

From the project folder with the virtual environment activated:

```bash
python main.py
```

If FFmpeg is not found, the app will show a message and export features will be disabled until FFmpeg is installed and in PATH.

## Usage

- **Open MP3**: Click "Open MP3" or drag and drop an MP3 file onto the window.
- **Playback**: Use Play / Pause / Stop. Use the position slider to seek; the label shows current time / total duration.
- **Volume increase**: Enter a value between 100 and 1000 (e.g. 101 = +1%, 200 = +100%). Click "Export with increased volume" and choose location with Save as.
- **Cut sample**: Enter start and end as `MM:SS MM:SS` (or in two fields). Click "Export sample" and choose location with Save as.

## Distributable packages (Windows .exe and Mac .app)

To build a Windows `.exe` or a Mac `.app` so users can run the tool without installing Python or FFmpeg, see **[BUILD.md](BUILD.md)**.

### Mac: single file for users

On Mac, **MP3Tool.app** is the only file users need. It contains the app and FFmpeg; no separate Python or FFmpeg install is required. Users double-click **MP3Tool.app** to run the program. You can distribute that one file (or **MP3Tool-mac.zip** containing it; see BUILD.md).

### First time running (for end users)

- **Windows**: Double-click **MP3Tool.exe** to run. No installer. If Windows SmartScreen or your antivirus blocks it, choose "More info" then "Run anyway" (or add an exception for the file).
- **Mac**: Double-click **MP3Tool.app** to run. If macOS says the app is from an "unidentified developer", right-click **MP3Tool.app** and choose **Open** once; click **Open** in the dialog. After that, double-clicking is enough.
