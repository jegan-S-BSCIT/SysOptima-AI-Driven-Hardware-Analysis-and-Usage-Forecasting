"""
Main Window - SysOptima
Design: Enterprise Sidebar Layout (Stitch Level)
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.dashboard import DashboardView
from ui.hardware_info import HardwareInfoView
from ui.performance_reports import PerformanceReportsPanel
from ui.realtime_monitor import RealtimeMonitorView
from ui.diagnostics import DiagnosticsView
from core.hardware_detector import HardwareDetector

class MainWindow:
    """
    Main Application Entry Point with Professional Sidebar Layout.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SysOptima – System Optimization & Benchmarking")
        self.root.geometry("1280x800")
        self.root.configure(bg="#F8F9FA")

        self.detector = HardwareDetector()
        
        self.current_view = None
        self.nav_buttons = {}
        
        self._setup_layout()
        self._show_section("Dashboard") # Default

    def _setup_layout(self):
        # 1. Sidebar (Fixed Left)
        self.sidebar = tk.Frame(self.root, bg="#FFFFFF", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Sidebar Border
        tk.Frame(self.root, bg="#E2E8F0", width=1).pack(side="left", fill="y")

        # 2. Main Content Area
        self.content_area = tk.Frame(self.root, bg="#F8F9FA")
        self.content_area.pack(side="left", fill="both", expand=True)

        # --- Sidebar Content ---
        # Title/Logo Area
        brand_frame = tk.Frame(self.sidebar, bg="#FFFFFF", height=80)
        brand_frame.pack(fill="x")
        tk.Label(brand_frame, text="SysOptima", bg="#FFFFFF", fg="#0F172A", 
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=(20, 10), pady=20)
        
        # Navigation Menu
        self.nav_frame = tk.Frame(self.sidebar, bg="#FFFFFF")
        self.nav_frame.pack(fill="both", expand=True, pady=10)
        
        self._add_nav_item("Dashboard", "□")
        self._add_nav_item("Hardware Info", "□")
        self._add_nav_item("Performance", "□") # The Report Page
        self._add_nav_item("Real-time Monitor", "□")
        self._add_nav_item("Diagnostics", "□")
        self._add_nav_item("Benchmarks", "□")
        self._add_nav_item("Settings", "□")

        # Copyright / User info at bottom
        footer = tk.Frame(self.sidebar, bg="#FFFFFF", height=50)
        footer.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Label(footer, text="v1.0.0 Enterprise", bg="#FFFFFF", fg="#94A3B8", font=("Segoe UI", 9)).pack(anchor="w")

    def _add_nav_item(self, name, icon_char):
        """Create a styled navigation button"""
        # Using Frame + Label to simulate a rich button
        btn_frame = tk.Frame(self.nav_frame, bg="#FFFFFF", cursor="hand2", padx=20, pady=12)
        btn_frame.pack(fill="x", pady=2)
        
        # visual indicator container
        # icon = tk.Label(btn_frame, text=icon_char, bg="#FFFFFF", fg="#64748B", font=("Segoe UI", 12))
        # icon.pack(side="left", padx=(0, 12))
        
        lbl = tk.Label(btn_frame, text=name, bg="#FFFFFF", fg="#64748B", font=("Segoe UI", 11, "bold"))
        lbl.pack(side="left")
        
        # Bind events
        for widget in (btn_frame, lbl):
            widget.bind("<Button-1>", lambda e, n=name: self._show_section(n))
            widget.bind("<Enter>", lambda e, f=btn_frame: self._on_hover(f, True))
            widget.bind("<Leave>", lambda e, f=btn_frame: self._on_hover(f, False))
            
        self.nav_buttons[name] = {'frame': btn_frame, 'label': lbl, 'active': False}

    def _on_hover(self, frame, is_hover):
        # Only highlight if not active
        name = [k for k, v in self.nav_buttons.items() if v['frame'] == frame][0]
        if not self.nav_buttons[name]['active']:
            bg = "#F1F5F9" if is_hover else "#FFFFFF"
            frame.config(bg=bg)
            for child in frame.winfo_children():
                child.config(bg=bg)

    def _show_section(self, name):
        # Update Nav State
        for n, widgets in self.nav_buttons.items():
            is_active = (n == name)
            widgets['active'] = is_active
            
            # Style update
            bg_color = "#E0F2FE" if is_active else "#FFFFFF" # Soft Blue for active
            fg_color = "#0284C7" if is_active else "#64748B" # Blue text vs Gray
            
            widgets['frame'].config(bg=bg_color)
            widgets['label'].config(bg=bg_color, fg=fg_color)
            
            # Indicator logic (optional blue bar)
            # Remove old Left Bar if exists
            for child in widgets['frame'].winfo_children():
                if getattr(child, 'is_bar', False):
                    child.destroy()
            
            if is_active:
                bar = tk.Frame(widgets['frame'], bg="#0284C7", width=4)
                bar.is_bar = True
                bar.place(relx=0, rely=0, relheight=1.0)

        # Switch Content
        if self.current_view:
            self.current_view.destroy()
        
        if name == "Dashboard":
            self.current_view = DashboardView(self.content_area)
        elif name == "Hardware Info":
            self.current_view = HardwareInfoView(self.content_area, on_detect=self.detector.detect_all)
        elif name == "Performance":
            self.current_view = PerformanceReportsPanel(self.content_area)
        elif name == "Real-time Monitor":
            self.current_view = RealtimeMonitorView(self.content_area)
        elif name == "Diagnostics":
            self.current_view = DiagnosticsView(self.content_area)
            # You might need to wire up on_run here if you have logic
        elif name == "Benchmarks":
             # Placeholder
             f = tk.Frame(self.content_area, bg="#F8F9FA")
             tk.Label(f, text="Benchmarks Coming Soon", bg="#F8F9FA", font=("Segoe UI", 20)).pack(pady=50)
             self.current_view = f
        elif name == "Settings":
             # Placeholder
             f = tk.Frame(self.content_area, bg="#F8F9FA")
             tk.Label(f, text="Settings", bg="#F8F9FA", font=("Segoe UI", 20)).pack(pady=50)
             self.current_view = f
             
        if self.current_view:
            self.current_view.pack(fill="both", expand=True)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
