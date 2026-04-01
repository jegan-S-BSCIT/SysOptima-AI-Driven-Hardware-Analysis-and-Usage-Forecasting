# PyInstaller Configuration for SysOptima Desktop Application
# This creates a standalone EXE that runs without console window

[Settings]
name = SysOptima
description = Intelligent Computer Performance Analysis System
version = 1.0.0
author = B.Sc. IT Final Year Project

[PyInstaller]
# Main script
entry_point = main.py

# Hidden imports (required but not detected automatically)
hidden_imports = 
    psutil
    GPUtil
    matplotlib
    matplotlib.backends.backend_tkagg
    google.generativeai
    python-dotenv

# Data files to include
data_files = 
    core/
    data/
    .env

# Excludes
excludes = 
    tkinter.test
    unittest
    pydoc
    pip
    setuptools
    wheel
    tcl/demos

# Console settings
console = false
windowed = true
icon = assets/icon.ico (optional)

# Output
dist_path = dist/
build_path = build/
output_name = SysOptima.exe
