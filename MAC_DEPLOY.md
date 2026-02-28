# Deploy MP3 Tool on your Mac (MacBook)

This guide is for **Mac users** who want to build **MP3Tool.app** from this repository so they can run the app by double-clicking it (no Python or FFmpeg install needed for end users).

---

## What you need

- A Mac (macOS)
- **Python 3.10 or newer** (check with `python3 --version`)
- **Homebrew** (optional but recommended for installing FFmpeg and Python): [brew.sh](https://brew.sh)
- **Git** (to clone the repo): `xcode-select --install` if not already installed

---

## Step 1: Clone the repository

Open **Terminal** (Applications → Utilities → Terminal) and run:

```bash
git clone https://github.com/minanaguib90/Mp3Tool.git
cd Mp3Tool
```

You now have the project folder (e.g. `~/Mp3Tool` or wherever you cloned it).

---

## Step 2: Install FFmpeg (required for the build)

The build script needs `ffmpeg` and `ffprobe` to bundle them into the app. Install FFmpeg with Homebrew:

```bash
brew install ffmpeg
```

If you don't use Homebrew, install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or [evermeet.cx/ffmpeg](https://evermeet.cx/ffmpeg/) and ensure `ffmpeg` and `ffprobe` are on your PATH.

---

## Step 3: Run the Mac build script

In the same Terminal window, from the project folder (`Mp3Tool`):

```bash
chmod +x build_mac_app.sh
./build_mac_app.sh
```

The script will:

1. Copy `ffmpeg` and `ffprobe` into `build_resources/ffmpeg_mac/` (if not already there)
2. Install Python dependencies (PyQt6, pydub, pygame, PyInstaller, etc.)
3. Build **MP3Tool.app** with PyInstaller
4. Copy **MP3Tool.app** into the project folder
5. Create **MP3Tool-mac.zip** (optional one-file distribution)

Build time is usually a few minutes.

---

## Step 4: Run the app

After a successful build you will have:

- **MP3Tool.app** – double-click to run.
- **MP3Tool-mac.zip** – contains the same app; useful for sharing one file.

**First time only:** If macOS says the app is from an "unidentified developer":

1. Right-click **MP3Tool.app**
2. Choose **Open**
3. Click **Open** in the dialog

After that, you can start the app by double-clicking **MP3Tool.app** as usual.

---

## Optional: Move the app

You can drag **MP3Tool.app** to **Applications** or keep it in the project folder. The app is self-contained (it includes FFmpeg); you can copy or share **MP3Tool.app** alone.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `python3: command not found` | Install Python from [python.org](https://www.python.org/downloads/) or run `brew install python` |
| `brew: command not found` | Install Homebrew from [brew.sh](https://brew.sh) |
| `FFmpeg not found` / script says "Install FFmpeg first" | Run `brew install ffmpeg` and try again |
| `Permission denied` when running the script | Run `chmod +x build_mac_app.sh` then `./build_mac_app.sh` again |
| Build fails with "No module named ..." | Run `pip3 install -r requirements.txt -r requirements-build.txt` then `./build_mac_app.sh` again |

For more details (e.g. Windows build, FFmpeg manual setup), see **[BUILD.md](BUILD.md)**.
