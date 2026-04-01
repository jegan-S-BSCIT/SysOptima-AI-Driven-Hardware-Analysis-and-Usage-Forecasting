#!/bin/bash
# SysOptima Desktop Application Launcher (Linux/macOS)
# Pure desktop application - NO web components

echo "============================================================"
echo "    SysOptima - Desktop Application Launcher"
echo "    Intelligent Computer Performance Analysis System"
echo "============================================================"
echo

# Get Python interpreter
PYTHON_EXE=".venv/bin/python"

# Check if venv exists
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Error: Python virtual environment not found!"
    echo "Please run: python3 -m venv .venv"
    echo "Then run: pip install -r requirements.txt"
    exit 1
fi

echo "Starting SysOptima Desktop Application..."
echo

# Run main application
"$PYTHON_EXE" main.py

if [ $? -ne 0 ]; then
    echo
    echo "Error: Application failed to start"
    echo
fi
