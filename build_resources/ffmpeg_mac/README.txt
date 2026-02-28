Place FFmpeg macOS binaries here before building the Mac .app.

1. Install FFmpeg on your Mac (e.g. run: brew install ffmpeg).

2. Copy the binaries into this folder:
   cp $(which ffmpeg) build_resources/ffmpeg_mac/
   cp $(which ffprobe) build_resources/ffmpeg_mac/

   Or use a static build from https://evermeet.cx/ffmpeg/ (download ffmpeg and ffprobe).

3. Ensure the two files are named exactly: ffmpeg and ffprobe (no .exe).

4. Run the Mac build (see BUILD.md in the project root).
