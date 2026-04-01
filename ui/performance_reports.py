"""
SysOptima Performance Reports
Design: Google Stitch-inspired Master-Detail Layout
Theme: Light, Professional, clean
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
from core.performance_report import PerformanceReportManager
from core.performance_analyzer import PerformanceAnalyzer

# --- Local Light Theme Theme Definition ---
class LightTheme:
    # Backgrounds
    bg_base = "#F8F9FA"         # Main background (very light gray)
    bg_card = "#FFFFFF"         # Card background (white)
    bg_sidebar = "#F1F5F9"      # Sidebar background (slate-50)
    bg_hover = "#E2E8F0"        # Hover state (slate-200)
    bg_selected = "#FFFFFF"     # Sidebar selected item
    
    # Text
    text_primary = "#0F172A"    # Slate-900
    text_secondary = "#64748B"  # Slate-500
    text_tertiary = "#94A3B8"   # Slate-400
    
    # Accents & Status
    accent = "#2563EB"          # Blue-600
    success = "#10B981"         # Emerald-500
    warning = "#F59E0B"         # Amber-500
    danger = "#EF4444"          # Red-500
    
    # UI Elements
    border = "#E2E8F0"          # Slate-200
    separator = "#CBD5E1"       # Slate-300
    
    font_family = "Segoe UI"

theme = LightTheme()

class SidebarItem(tk.Frame):
    """
    Styled sidebar item representing a report.
    Has normal, hover, and selected states.
    """
    def __init__(self, parent, report, is_selected=False, command=None):
        self.is_selected = is_selected
        self.command = command
        self.report = report
        
        # Colors
        bg_color = theme.bg_selected if is_selected else theme.bg_sidebar
        fg_title = theme.accent if is_selected else theme.text_primary
        
        # Border for separation
        super().__init__(parent, bg=bg_color, relief="flat", padx=12, pady=12)
        
        if is_selected:
            # Add a left accent bar for selected state
            self.indicator = tk.Frame(self, bg=theme.accent, width=4)
            self.indicator.pack(side="left", fill="y", padx=(0, 10))
        
        content = tk.Frame(self, bg=bg_color)
        content.pack(side="left", fill="both", expand=True)
        
        # Title
        title_font = (theme.font_family, 10, "bold")
        self.title_lbl = tk.Label(content, text=report.label, bg=bg_color, fg=fg_title, 
                                  font=title_font, anchor="w")
        self.title_lbl.pack(fill="x")
        
        # Metadata Row
        meta_row = tk.Frame(content, bg=bg_color)
        meta_row.pack(fill="x", pady=(4, 0))
        
        # Date
        date_str = report.timestamp.strftime("%b %d")
        tk.Label(meta_row, text=date_str, bg=bg_color, fg=theme.text_tertiary, 
                 font=(theme.font_family, 9)).pack(side="left")
        
        # Status Dot
        status_color = theme.text_tertiary
        if report.status in ["Excellent", "Good"]: status_color = theme.success
        elif report.status == "Moderate": status_color = theme.warning
        elif report.status in ["Needs Attention", "Poor"]: status_color = theme.danger
        
        dot_canvas = tk.Canvas(meta_row, width=10, height=10, bg=bg_color, bd=0, highlightthickness=0)
        dot_canvas.pack(side="right")
        dot_canvas.create_oval(2, 2, 8, 8, fill=status_color, outline=status_color)

        # Event Binding
        self.bind("<Button-1>", self._on_click)
        content.bind("<Button-1>", self._on_click)
        self.title_lbl.bind("<Button-1>", self._on_click)
        
        # Hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        if self.command:
            self.command(self.report)

    def _on_enter(self, event):
        if not self.is_selected:
            self.configure(bg=theme.bg_hover)
            for child in self.winfo_children():
                if isinstance(child, tk.Frame) and child != getattr(self, 'indicator', None):
                   child.configure(bg=theme.bg_hover) 
                   for sub in child.winfo_children():
                       sub.configure(bg=theme.bg_hover)

    def _on_leave(self, event):
        if not self.is_selected:
            self.configure(bg=theme.bg_sidebar)
            for child in self.winfo_children():
                if isinstance(child, tk.Frame) and child != getattr(self, 'indicator', None):
                    child.configure(bg=theme.bg_sidebar)
                    for sub in child.winfo_children():
                       sub.configure(bg=theme.bg_sidebar)


class MetricCard(tk.Frame):
    """
    A unified card for a single metric with a modern progress bar.
    """
    def __init__(self, parent, title, score, width=180):
        super().__init__(parent, bg=theme.bg_card, highlightbackground=theme.border, highlightthickness=1)
        self.pack_propagate(False)
        self.configure(width=width, height=130)
        
        content = tk.Frame(self, bg=theme.bg_card, padx=15, pady=15)
        content.pack(fill="both", expand=True)
        
        # Title
        tk.Label(content, text=title.upper(), bg=theme.bg_card, fg=theme.text_secondary, 
                 font=(theme.font_family, 9, "bold")).pack(anchor="w")
        
        # Score Value
        color = theme.success if score >= 75 else (theme.warning if score >= 55 else theme.danger)
        tk.Label(content, text=f"{int(score)}", bg=theme.bg_card, fg=color, 
                 font=(theme.font_family, 32, "bold")).pack(anchor="w", pady=(5, 10))
        
        # Progress Bar
        self.canvas = tk.Canvas(content, height=6, bg=theme.border, bd=0, highlightthickness=0)
        self.canvas.pack(fill="x")
        
        # Draw filled part
        # Note: Canvas width isn't known until packed. 
        # We assume a reasonable width or bind configure.
        # For simplicity in this layout, we'll draw based on the container frame width assumption
        
        # Using a frame for the bar is easier for responsiveness
        bar_bg = tk.Frame(content, bg=theme.border, height=6)
        bar_bg.place(relx=0, rely=0.85, relwidth=1.0, anchor="nw")
        
        bar_fill = tk.Frame(content, bg=color, height=6)
        bar_fill.place(relx=0, rely=0.85, relwidth=(score/100.0), anchor="nw")


class ReportDetailView(tk.Frame):
    """
    Detailed view with "white paper" aesthetic.
    """
    def __init__(self, parent, report):
        super().__init__(parent, bg=theme.bg_base)
        self.report = report
        self.data = report.data or {}
        
        # Scrollable possible? For now, fixed layout fits constraints.
        container = tk.Frame(self, bg=theme.bg_base, padx=40, pady=30)
        container.pack(fill="both", expand=True)
        
        # 1. Header
        header = tk.Frame(container, bg=theme.bg_base)
        header.pack(fill="x", pady=(0, 30))
        
        tk.Label(header, text=report.label, bg=theme.bg_base, fg=theme.text_primary, 
                 font=(theme.font_family, 24, "bold")).pack(anchor="w")
        
        meta_text = f"Evaluated on {report.timestamp.strftime('%B %d, %Y')} at {report.timestamp.strftime('%I:%M %p')}"
        tk.Label(header, text=meta_text, bg=theme.bg_base, fg=theme.text_secondary, 
                 font=(theme.font_family, 11)).pack(anchor="w")

        # 2. Metrics Row
        scores_frame = tk.Frame(container, bg=theme.bg_base)
        scores_frame.pack(fill="x", pady=(0, 30))
        
        # Create 4 equal cards using grid
        scores_frame.grid_columnconfigure(0, weight=1)
        scores_frame.grid_columnconfigure(1, weight=1)
        scores_frame.grid_columnconfigure(2, weight=1)
        scores_frame.grid_columnconfigure(3, weight=1)
        
        MetricCard(scores_frame, "Overall Score", self.data.get('overall_score', 0)).grid(row=0, column=0, padx=(0, 15), sticky="ew")
        MetricCard(scores_frame, "CPU Score", self.data.get('cpu_score', 0)).grid(row=0, column=1, padx=(0, 15), sticky="ew")
        MetricCard(scores_frame, "Memory Score", self.data.get('memory_score', 0)).grid(row=0, column=2, padx=(0, 15), sticky="ew")
        MetricCard(scores_frame, "Disk Score", self.data.get('disk_score', 0)).grid(row=0, column=3, padx=(0, 0), sticky="ew")

        # 3. Analysis & Forecast (Side by Side)
        bottom_frame = tk.Frame(container, bg=theme.bg_base)
        bottom_frame.pack(fill="both", expand=True)
        bottom_frame.columnconfigure(0, weight=3) # Analysis 60%
        bottom_frame.columnconfigure(1, weight=2) # Forecast 40%
        
        # Analysis Panel
        analysis_card = tk.Frame(bottom_frame, bg=theme.bg_card, padx=25, pady=25, 
                                 highlightbackground=theme.border, highlightthickness=1)
        analysis_card.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        tk.Label(analysis_card, text="Diagnostic Analysis", bg=theme.bg_card, fg=theme.text_primary, 
                 font=(theme.font_family, 14, "bold")).pack(anchor="w", pady=(0, 15))
        
        interpretation = self.data.get('interpretation', "No analysis available.")
        # Wrap text nicely
        lbl = tk.Label(analysis_card, text=interpretation, bg=theme.bg_card, fg=theme.text_secondary,
                 font=(theme.font_family, 11), wraplength=450, justify="left", anchor="w")
        lbl.pack(fill="x")
        
        # Optimization Hints
        from core.performance_report import get_optimization_hints
        hints = get_optimization_hints(self.data.get('cpu_score', 0), 
                                     self.data.get('memory_score', 0), 
                                     self.data.get('disk_score', 0))
        
        if hints:
            tk.Label(analysis_card, text="Recommendations:", bg=theme.bg_card, fg=theme.text_primary, 
                     font=(theme.font_family, 11, "bold")).pack(anchor="w", pady=(20, 10))
            for hint in hints:
                row = tk.Frame(analysis_card, bg=theme.bg_card)
                row.pack(fill="x", pady=2)
                tk.Label(row, text="•", bg=theme.bg_card, fg=theme.accent, font=("Arial", 12)).pack(side="left", anchor="n")
                tk.Label(row, text=hint, bg=theme.bg_card, fg=theme.text_secondary, 
                         font=(theme.font_family, 10), wraplength=420, justify="left").pack(side="left")

        # Forecast Panel
        forecast_card = tk.Frame(bottom_frame, bg=theme.bg_card, padx=25, pady=25,
                                 highlightbackground=theme.border, highlightthickness=1)
        forecast_card.grid(row=0, column=1, sticky="nsew")
        
        tk.Label(forecast_card, text="Capability Forecast", bg=theme.bg_card, fg=theme.text_primary, 
                 font=(theme.font_family, 14, "bold")).pack(anchor="w", pady=(0, 15))
                 
        from core.performance_report import get_usage_capability_forecast
        forecast = get_usage_capability_forecast(
            self.data.get('cpu_score', 0),
            self.data.get('memory_score', 0),
            self.data.get('disk_score', 0),
            self.data.get('overall_score', 0)
        )
        
        # Table-like layout
        i = 0
        for task, suit in forecast.items():
            bg_row = theme.bg_base if i % 2 == 0 else theme.bg_card
            row = tk.Frame(forecast_card, bg=bg_row, pady=8, padx=10)
            row.pack(fill="x")
            
            tk.Label(row, text=task, bg=bg_row, fg=theme.text_secondary, 
                     font=(theme.font_family, 10)).pack(side="left")
            
            fg_suit = theme.text_secondary
            if suit == "Excellent": fg_suit = theme.success
            elif suit == "Good": fg_suit = theme.accent
            elif suit == "Moderate": fg_suit = theme.warning
            elif suit == "Not Recommended": fg_suit = theme.danger
            
            tk.Label(row, text=suit, bg=bg_row, fg=fg_suit, 
                     font=(theme.font_family, 10, "bold")).pack(side="right")
            i += 1


class PerformanceReportsPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg=theme.bg_base, *args, **kwargs)
        
        # Structure: Sidebar | Separator | Main Content
        self.sidebar = tk.Frame(self, bg=theme.bg_sidebar, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Separator Line
        tk.Frame(self, bg=theme.border, width=1).pack(side="left", fill="y")
        
        # Main Content
        self.content_area = tk.Frame(self, bg=theme.bg_base)
        self.content_area.pack(side="left", fill="both", expand=True)
        
        # --- Sidebar Content ---
        # Header
        sb_header = tk.Frame(self.sidebar, bg=theme.bg_sidebar, height=80)
        sb_header.pack(fill="x", pady=(20, 10))
        
        tk.Label(sb_header, text="Reports", bg=theme.bg_sidebar, fg=theme.text_primary, 
                 font=(theme.font_family, 20, "bold"), padx=20).pack(anchor="w")
        
        tk.Label(sb_header, text="History & Analysis", bg=theme.bg_sidebar, fg=theme.text_secondary,
                 font=(theme.font_family, 10), padx=20).pack(anchor="w")

        # List
        self.report_list_frame = tk.Frame(self.sidebar, bg=theme.bg_sidebar)
        self.report_list_frame.pack(fill="both", expand=True)

        self.detail_view = None
        self.manager = None
        
        # Show loading message
        self._show_loading()
        
        # Generate reports in background thread
        threading.Thread(target=self._load_reports_async, daemon=True).start()
    
    def _show_loading(self):
        """Show loading indicator"""
        loading_frame = tk.Frame(self.content_area, bg=theme.bg_base)
        loading_frame.pack(fill="both", expand=True)
        
        tk.Label(loading_frame, text="⚙️", bg=theme.bg_base, fg=theme.accent,
                 font=(theme.font_family, 48)).pack(expand=True, pady=(100, 20))
        tk.Label(loading_frame, text="Analyzing System Performance...", bg=theme.bg_base,
                 fg=theme.text_primary, font=(theme.font_family, 14)).pack()
        tk.Label(loading_frame, text="This may take a few seconds", bg=theme.bg_base,
                 fg=theme.text_secondary, font=(theme.font_family, 11)).pack(pady=(5, 0))
    
    def _load_reports_async(self):
        """Load reports in background thread"""
        self.manager = PerformanceReportManager()
        
        # Schedule UI update on main thread
        self.after(0, self._on_reports_loaded)
    
    def _on_reports_loaded(self):
        """Called when reports are loaded"""
        self._populate_report_list()
        
        if self.manager.reports:
            self._select_report(self.manager.reports[0])

    def _populate_report_list(self):
        # Check if widget still exists
        if not self.report_list_frame.winfo_exists():
            return
            
        for widget in self.report_list_frame.winfo_children():
            widget.destroy()
        
        if not self.manager:
            return
            
        reports = self.manager.get_reports()
        for r in reports:
            SidebarItem(self.report_list_frame, r, 
                        is_selected=(getattr(self, 'selected_report', None) == r),
                        command=self._select_report).pack(fill="x")

    def _select_report(self, report):
        self.selected_report = report
        self._populate_report_list()
        
        if self.detail_view:
            self.detail_view.destroy()
            
        self.detail_view = ReportDetailView(self.content_area, report)
        self.detail_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x700")
    PerformanceReportsPanel(root).pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x700")
    PerformanceReportsPanel(root).pack(fill="both", expand=True)
    root.mainloop()
