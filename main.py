"""
SysOptima - Intelligent Computer Performance Analysis and Guidance System
Main Desktop Application Entry Point

B.Sc. IT Final Year Project
Pure desktop application using Tkinter (NO web components)
Web backend removed to enforce desktop-only execution.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from desktop_ui.main_window import MainWindow


def main():
    """Initialize and run the desktop application"""
    
    # Create root Tkinter window
    root = tk.Tk()
    root.title("Intelligent Computer Performance Analysis System")
    root.geometry("1200x800")
    root.resizable(True, True)
    
    # Set minimum window size
    root.minsize(1000, 700)
    
    # Create main application
    app = MainWindow(root)
    
    # Handle window close event
    def on_closing():
        """Gracefully shutdown application"""
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
