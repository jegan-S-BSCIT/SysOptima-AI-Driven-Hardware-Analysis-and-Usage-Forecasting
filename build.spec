# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Build Specification for SysOptima Desktop Application

Usage:
    pyinstaller build.spec

This will create a standalone executable:
    dist/SysOptima/SysOptima.exe
"""

import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core', 'core'),
        ('data', 'data'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'psutil',
        'GPUtil',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'google.generativeai',
        'dotenv',
        'tkinter',
        'tkinter.ttk',
    ] + collect_submodules('matplotlib'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        'tkinter.test',
        'unittest',
        'pydoc',
        'pip',
        'setuptools',
        'wheel',
    ],
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
    name='SysOptima',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Optional: add icon path here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SysOptima'
)
