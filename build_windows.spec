# -*- mode: python ; coding: utf-8 -*-
# Build on Windows to produce a folder containing MP3Tool.exe and bundled ffmpeg.
# Run: pyinstaller build_windows.spec
# Output: dist/MP3Tool/MP3Tool.exe (and ffmpeg_win with ffmpeg.exe, ffprobe.exe)

import sys

block_cipher = None

ffmpeg_win = 'build_resources/ffmpeg_win'
import os
if not os.path.isdir(ffmpeg_win):
    raise SystemExit('Missing build_resources/ffmpeg_win/ with ffmpeg.exe and ffprobe.exe. See build_resources/ffmpeg_win/README.txt')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (ffmpeg_win, 'ffmpeg_win'),
    ],
    hiddenimports=['audioop'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MP3Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
