"""
SysOptima - Modern Professional System Analysis & Optimization Tool
Main application entry point with enhanced professional UI

A state-of-the-art system intelligence platform providing:
- Real-time hardware monitoring
- AI-powered diagnostics
- Professional performance analytics
- Enterprise-grade visualization
- Comprehensive system insights
"""

import customtkinter as ctk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.modern_ui import MainWindow


def main():
    """Launch SysOptima application"""
    
    # Initialize appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create and run main window
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
