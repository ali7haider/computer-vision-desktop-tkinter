"""Build on Windows for a portable EXE, or on macOS for an app bundle."""

import sys
from pathlib import Path


if sys.platform not in ("win32", "darwin"):
    raise SystemExit("Build this package on Windows or macOS, for that same OS.")

project = Path(SPECPATH)
is_mac = sys.platform == "darwin"
app_name = "ComputerVisionTool"

# PyInstaller's built-in hooks collect Tkinter, NumPy, and OpenCV dependencies.
analysis = Analysis(
    [str(project / "main.py")],
    pathex=[str(project)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
python_archive = PYZ(analysis.pure)

# Windows packs dependencies into one EXE. macOS keeps them inside the app bundle.
executable = EXE(
    python_archive,
    analysis.scripts,
    [] if is_mac else analysis.binaries,
    [] if is_mac else analysis.datas,
    [],
    name=app_name,
    exclude_binaries=is_mac,
    console=False,
    debug=False,
    strip=False,
    upx=False,
)

if is_mac:
    folder = COLLECT(
        executable, analysis.binaries, analysis.datas,
        name=app_name, strip=False, upx=False,
    )
    app = BUNDLE(
        folder,
        name=f"{app_name}.app",
        bundle_identifier="org.student.computervisiontool",
        info_plist={
            "CFBundleDisplayName": "Computer Vision Tool",
            "NSHighResolutionCapable": True,
            "NSCameraUsageDescription": "Use the webcam to preview images and take snapshots for processing.",
        },
    )
