# -*- mode: python ; coding: utf-8 -*-
# Build on macOS to produce MP3Tool.app with bundled ffmpeg.
# Run: pyinstaller build_mac.spec
# Output: dist/MP3Tool.app

import os

ffmpeg_mac = 'build_resources/ffmpeg_mac'
if not os.path.isdir(ffmpeg_mac):
    raise SystemExit('Missing build_resources/ffmpeg_mac/ with ffmpeg and ffprobe. See build_resources/ffmpeg_mac/README.txt')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (ffmpeg_mac, 'ffmpeg_mac'),
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
    [],
    exclude_binaries=True,
    name='MP3Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MP3Tool',
)

app = BUNDLE(
    coll,
    name='MP3Tool.app',
    icon=None,
    bundle_identifier='com.mp3tool.app',
    info_plist={
        'CFBundleName': 'MP3Tool',
        'CFBundleDisplayName': 'MP3 Tool',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
    },
)
