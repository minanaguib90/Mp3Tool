#!/bin/bash
# Build MP3Tool.app on macOS and place it in the project folder.
# Run on Mac: chmod +x build_mac_app.sh && ./build_mac_app.sh

set -e
cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

# 1. Ensure ffmpeg_mac has ffmpeg and ffprobe
FFMPEG_MAC="$PROJECT_DIR/build_resources/ffmpeg_mac"
mkdir -p "$FFMPEG_MAC"
if [ ! -f "$FFMPEG_MAC/ffmpeg" ] || [ ! -f "$FFMPEG_MAC/ffprobe" ]; then
  if command -v ffmpeg >/dev/null 2>&1; then
    cp "$(which ffmpeg)" "$FFMPEG_MAC/ffmpeg"
    cp "$(which ffprobe)" "$FFMPEG_MAC/ffprobe"
    echo "Copied ffmpeg and ffprobe into build_resources/ffmpeg_mac/"
  else
    echo "Install FFmpeg first: brew install ffmpeg"
    exit 1
  fi
fi

# 2. Install deps if needed
pip install -q -r requirements.txt -r requirements-build.txt

# 3. Build .app
python -m PyInstaller --noconfirm build_mac.spec

# 4. Copy .app into project folder
APP_SRC="$PROJECT_DIR/dist/MP3Tool.app"
APP_DEST="$PROJECT_DIR/MP3Tool.app"
if [ -d "$APP_SRC" ]; then
  rm -rf "$APP_DEST"
  cp -R "$APP_SRC" "$APP_DEST"
  echo "Built: $APP_DEST"
else
  echo "Build completed but MP3Tool.app not found in dist/"
  exit 1
fi

# 5. Create MP3Tool-mac.zip (one downloadable file containing the .app)
ZIP_DEST="$PROJECT_DIR/MP3Tool-mac.zip"
rm -f "$ZIP_DEST"
(cd "$PROJECT_DIR" && zip -r "MP3Tool-mac.zip" "MP3Tool.app")
echo "Created: $ZIP_DEST"
