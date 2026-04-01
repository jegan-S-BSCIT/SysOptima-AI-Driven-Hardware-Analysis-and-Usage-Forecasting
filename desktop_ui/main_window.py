"""
Main Window - System Intelligence Platform
Orchestrator for the Dark Sidebar Layout

Architecture:
- Sidebar: Navigation
- Header: Page title and status
- View Container: Main content area (FULL WIDTH - no right panel)
- NOTE: AI Assistant is now the ONLY AI interface (centered and full-width on its tab)
"""

import tkinter as tk
from tkinter import ttk
from desktop_ui.styles import COLORS, FONTS, SPACING

# Views
from desktop_ui.views.dashboard_view import DashboardView
from desktop_ui.views.benchmarks_view import BenchmarksView
from desktop_ui.views.live_view import LiveView
from desktop_ui.views.performance_view import PerformanceView
from desktop_ui.views.hardware_view import HardwareView 
from desktop_ui.ai_chat_tab import AIChatTab 

class MainWindow:
    """Main application window with Modern Dark Sidebar layout"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SysOptima - System Intelligence Platform")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.geometry("1400x900")
        
        # --- Layout ---
        # 1. Sidebar (Left, Fixed)
        self.sidebar = tk.Frame(root, bg=COLORS["bg_sidebar"], width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # 2. Main Content Wrapper (Right, Expands - NO SPLIT)
        self.main_wrapper = tk.Frame(root, bg=COLORS["bg_main"])
        self.main_wrapper.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 2a. Header (Top)
        self.create_header()
        
        # 2b. Body (Below Header, FULL WIDTH)
        # View Container is now FULL WIDTH (no right panel)
        self.body_frame = tk.Frame(self.main_wrapper, bg=COLORS["bg_main"])
        self.body_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # View Container (takes all available space)
        self.view_container = tk.Frame(self.body_frame, bg=COLORS["bg_main"])
        self.view_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        
        # Initialize Views
        self.views = {}
        self.current_view = None
        
        # Create Views
        self.views["dashboard"] = DashboardView(self.view_container)
        self.views["performance"] = PerformanceView(self.view_container) 
        self.views["live"] = LiveView(self.view_container)
        self.views["benchmarks"] = BenchmarksView(self.view_container)
        self.views["ai"] = AIChatTab(self.view_container) 
        self.views["hardware"] = HardwareView(self.view_container) 
        
        # Default View
        self.switch_view("dashboard")
        
    def create_sidebar(self):
        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"], height=100)
        logo_frame.pack(fill=tk.X, pady=(SPACING["xl"], SPACING["xl"]))
        
        logo = tk.Label(logo_frame, text="SysOptima", bg=COLORS["bg_sidebar"], fg=COLORS["text_main"], font=("Segoe UI", 22, "bold"))
        logo.pack()
        
        desc = tk.Label(logo_frame, text="System Intelligence Platform", bg=COLORS["bg_sidebar"], fg=COLORS["text_dim"], font=FONTS["small"])
        desc.pack()
        
        # Nav Title
        tk.Label(self.sidebar, text="Navigation", bg=COLORS["bg_sidebar"], fg=COLORS["text_dim"],
             font=("Segoe UI", 10, "bold")).pack(fill=tk.X, padx=SPACING["xl"], pady=(0, SPACING["lg"]))
        
        # Buttons
        self.nav_btns = {}
        self.add_nav_btn("Dashboard", "dashboard", "📊")
        self.add_nav_btn("Hardware", "hardware", "🔍")
        self.add_nav_btn("Performance", "performance", "📈") 
        self.add_nav_btn("AI Expert", "ai", "🤖")
        self.add_nav_btn("Live", "live", "⚡")
        self.add_nav_btn("Benchmarks", "benchmarks", "🔧")
        
        # Bottom
        tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"]).pack(fill=tk.BOTH, expand=True)
        self.add_nav_btn("Settings", "settings", "⚙")

    def add_nav_btn(self, text, key, icon):
        btn = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"], cursor="hand2")
        btn.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["xs"])
        
        # Store for highlighting
        self.nav_btns[key] = btn
        
        # Bind click
        def on_click(e): self.switch_view(key)
            
        icon_lbl = tk.Label(btn, text=icon, bg=COLORS["bg_sidebar"], fg=COLORS["text_dim"], font=("Segoe UI", 12), width=3)
        icon_lbl.pack(side=tk.LEFT, padx=(SPACING["md"], SPACING["sm"]), pady=SPACING["md"])
        
        text_lbl = tk.Label(btn, text=text, bg=COLORS["bg_sidebar"], fg=COLORS["text_main"], font=("Segoe UI", 10, "bold"))
        text_lbl.pack(side=tk.LEFT, pady=SPACING["md"])
        
        # Bind child widgets too
        for w in (btn, icon_lbl, text_lbl):
            w.bind("<Button-1>", on_click)

    def create_header(self):
        header = tk.Frame(self.main_wrapper, bg=COLORS["bg_sidebar"], height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        
        self.header_title = tk.Label(header, text="Dashboard", bg=COLORS["bg_sidebar"], fg=COLORS["text_main"], font=FONTS["h2"])
        self.header_title.pack(side=tk.LEFT, padx=SPACING["xl"], pady=SPACING["md"])
        
        status = tk.Frame(header, bg=COLORS["bg_sidebar"])
        status.pack(side=tk.RIGHT, padx=SPACING["xl"])
        tk.Label(status, text="● System Healthy", bg=COLORS["bg_sidebar"], fg=COLORS["success"], font=FONTS["small"]).pack()

    def switch_view(self, key):
        if key == "settings": return
        
        # Highlight logic
        for k, btn in self.nav_btns.items():
            if k == key:
                bg = COLORS["bg_card"]
                fg = COLORS["text_main"]
            else:
                bg = COLORS["bg_sidebar"]
                fg = COLORS["text_dim"]
            
            btn.config(bg=bg)
            for child in btn.winfo_children():
                child.config(bg=bg)
                if k == key:
                    child.config(fg=COLORS["text_main"])
                else:
                     child.config(fg=COLORS["text_dim"] if "width" in child.keys() else COLORS["text_main"])

        # Title
        titles = {
            "dashboard": "System Overview",
            "performance": "Real-time Metrics",
            "live": "Live Monitor",
            "benchmarks": "System Benchmark",
            "ai": "AI Assistant Main Terminal",
            "hardware": "Hardware Diagnostics"
        }
        self.header_title.config(text=titles.get(key, "SysOptima"))

        # Swap View (now full-width, no panel considerations)
        if self.current_view:
            self.current_view.pack_forget()
        
        if key in self.views:
            view = self.views[key]
            # Handle different view types (some might be Frame, some objects with .frame)
            if hasattr(view, 'frame'): 
                view.frame.pack(fill=tk.BOTH, expand=True)
                self.current_view = view.frame
            else:
                view.pack(fill=tk.BOTH, expand=True)
                self.current_view = view

    def cleanup(self):
        for v in self.views.values():
            if hasattr(v, 'cleanup'): v.cleanup()
