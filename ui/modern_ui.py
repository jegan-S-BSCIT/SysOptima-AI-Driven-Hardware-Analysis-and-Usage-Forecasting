"""
SysOptima - Modern Professional UI
Main application window with professional enterprise-grade design
"""

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkProgressBar, CTkScrollableFrame
import tkinter as tk
from typing import Optional, Callable
import sys
import os

from ui.theme import theme, SysOptimaTheme
from core.hardware_detector import HardwareDetector
from core.system_metrics import SystemMetrics, HealthCalculator
from core.hardware_info import get_all_hardware_info
from core.performance_analyzer import PerformanceAnalyzer
from ui.live_monitor import LiveMonitorPanel
from ui.performance_reports import PerformanceReportsPanel

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")


class HeaderBar(CTkFrame):
    """Professional header bar with logo and navigation"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_dark, **kwargs)
        
        # Left section - Logo and title
        left_frame = CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", padx=theme.spacing.lg, pady=theme.spacing.md)
        
        # Logo/Icon placeholder
        logo_label = CTkLabel(
            left_frame,
            text="⚙️",
            font=(theme.typography.font_primary, 24),
            text_color=theme.colors.accent_cyan
        )
        logo_label.pack(side="left", padx=(0, theme.spacing.md))
        
        # Title
        title_label = CTkLabel(
            left_frame,
            text="SysOptima",
            font=(theme.typography.font_primary, theme.typography.size_xl, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(side="left")
        
        # Subtitle
        subtitle_label = CTkLabel(
            left_frame,
            text="System Intelligence Platform",
            font=(theme.typography.font_primary, theme.typography.size_sm),
            text_color=theme.colors.text_secondary
        )
        subtitle_label.pack(side="left", padx=(theme.spacing.lg, 0))
        
        # Right section - Status indicators
        right_frame = CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", padx=theme.spacing.lg, pady=theme.spacing.md)
        
        # Status indicator (will be updated dynamically)
        self.status_dot = CTkLabel(
            right_frame,
            text="●",
            font=(theme.typography.font_primary, 12),
            text_color=theme.colors.success
        )
        self.status_dot.pack(side="left", padx=(0, theme.spacing.sm))
        
        self.status_label = CTkLabel(
            right_frame,
            text="System Healthy",
            font=(theme.typography.font_primary, theme.typography.size_sm),
            text_color=theme.colors.text_secondary
        )
        self.status_label.pack(side="left")
    
    def update_status(self, status_text: str, color: str):
        """Update the status indicator dynamically"""
        self.status_label.configure(text=status_text)
        self.status_dot.configure(text_color=color)


class StatCard(CTkFrame):
    """Professional stat card with icon, title, value, and trend"""
    
    def __init__(self, parent, icon: str, title: str, value: str, unit: str = "", 
                 color: str = "#3B82F6", trend: Optional[str] = None, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Store for updates
        self.unit = unit
        self.icon_color = color
        
        # Content frame
        content = CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Header row - Icon and title
        header = CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, theme.spacing.md))
        
        icon_label = CTkLabel(
            header,
            text=icon,
            font=(theme.typography.font_primary, 20),
            text_color=color
        )
        icon_label.pack(side="left", padx=(0, theme.spacing.md))
        
        title_label = CTkLabel(
            header,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=theme.colors.text_secondary
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Value display (store reference)
        self.value_label = CTkLabel(
            content,
            text=f"{value}{unit}",
            font=(theme.typography.font_primary, theme.typography.size_lg, "bold"),
            text_color=theme.colors.text_primary
        )
        self.value_label.pack(anchor="w", pady=(0, theme.spacing.sm))
        
        # Trend indicator (store reference)
        self.trend_label = CTkLabel(
            content,
            text=trend or "",
            font=(theme.typography.font_primary, theme.typography.size_xs),
            text_color=theme.colors.text_tertiary
        )
        self.trend_label.pack(anchor="w")
    
    def update_value(self, value: str, trend: str = ""):
        """Update the stat card value and trend dynamically"""
        self.value_label.configure(text=f"{value}{self.unit}")
        if trend:
            self.trend_label.configure(text=trend)


class HealthBar(CTkFrame):
    """Professional health indicator bar"""
    
    def __init__(self, parent, label: str, percentage: float, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Label row
        label_row = CTkFrame(self, fg_color="transparent")
        label_row.pack(fill="x", pady=(0, theme.spacing.sm))
        
        label_widget = CTkLabel(
            label_row,
            text=label,
            font=(theme.typography.font_primary, theme.typography.size_base),
            text_color=theme.colors.text_primary
        )
        label_widget.pack(side="left")
        
        self.percentage_label = CTkLabel(
            label_row,
            text=f"{percentage:.1f}%",
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.get_status_color(percentage)
        )
        self.percentage_label.pack(side="right")
        
        # Progress bar (store reference)
        self.progress_bar = CTkProgressBar(
            self,
            fg_color=theme.colors.border_medium,
            progress_color=theme.get_status_color(percentage),
            height=8
        )
        self.progress_bar.set(percentage / 100)
        self.progress_bar.pack(fill="x")
    
    def update_health(self, percentage: float):
        """Update the health bar percentage and color dynamically"""
        self.percentage_label.configure(text=f"{percentage:.1f}%")
        color = theme.get_status_color(percentage)
        self.percentage_label.configure(text_color=color)
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(percentage / 100)


class DashboardPanel(CTkFrame):
    """Main dashboard with real-time stats and health overview"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_bg, **kwargs)
        
        # Initialize metrics system
        self.metrics = SystemMetrics()
        self.health_calc = HealthCalculator()
        self.previous_metrics = {"cpu": 0, "memory": 0, "disk": 0, "gpu": 0}
        
        # Title section
        title_frame = CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        title = CTkLabel(
            title_frame,
            text="System Overview",
            font=(theme.typography.font_primary, theme.typography.size_lg, "bold"),
            text_color=theme.colors.text_primary
        )
        title.pack(anchor="w")
        
        subtitle = CTkLabel(
            title_frame,
            text="Real-time system health and performance metrics",
            font=(theme.typography.font_primary, theme.typography.size_sm),
            text_color=theme.colors.text_tertiary
        )
        subtitle.pack(anchor="w", pady=(theme.spacing.sm, 0))
        
        # Stats grid
        stats_frame = CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Create stat cards and store references
        self.cpu_card = StatCard(
            stats_frame,
            icon="🔧",
            title="CPU Usage",
            value="0",
            unit="%",
            color=theme.colors.chart_blue,
            trend="→ Stable"
        )
        self.cpu_card.grid(row=0, column=0, sticky="ew", padx=theme.spacing.md, pady=theme.spacing.md)
        
        self.mem_card = StatCard(
            stats_frame,
            icon="💾",
            title="Memory Usage",
            value="0",
            unit="%",
            color=theme.colors.chart_cyan,
            trend="→ Stable"
        )
        self.mem_card.grid(row=0, column=1, sticky="ew", padx=theme.spacing.md, pady=theme.spacing.md)
        
        self.disk_card = StatCard(
            stats_frame,
            icon="💿",
            title="Disk Usage",
            value="0",
            unit="%",
            color=theme.colors.chart_indigo,
            trend="→ Stable"
        )
        self.disk_card.grid(row=0, column=2, sticky="ew", padx=theme.spacing.md, pady=theme.spacing.md)
        
        self.gpu_card = StatCard(
            stats_frame,
            icon="🎮",
            title="GPU Usage",
            value="0",
            unit="%",
            color=theme.colors.chart_pink,
            trend="→ Stable"
        )
        self.gpu_card.grid(row=0, column=3, sticky="ew", padx=theme.spacing.md, pady=theme.spacing.md)
        
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Health Section
        health_frame = CTkFrame(self, fg_color="transparent")
        health_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=(0, theme.spacing.lg))
        
        health_title = CTkLabel(
            health_frame,
            text="System Health",
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        health_title.pack(anchor="w", pady=(0, theme.spacing.lg))
        
        # Create health bars and store references
        self.cpu_health_bar = HealthBar(health_frame, "CPU Health", 0)
        self.cpu_health_bar.pack(fill="x", pady=theme.spacing.md)
        
        self.mem_health_bar = HealthBar(health_frame, "Memory Health", 0)
        self.mem_health_bar.pack(fill="x", pady=theme.spacing.md)
        
        self.disk_health_bar = HealthBar(health_frame, "Disk Health", 0)
        self.disk_health_bar.pack(fill="x", pady=theme.spacing.md)
        
        self.overall_health_bar = HealthBar(health_frame, "System Overall", 0)
        self.overall_health_bar.pack(fill="x", pady=theme.spacing.md)
        
        # Start auto-refresh
        self.refresh_dashboard()
    
    def refresh_dashboard(self):
        """Update dashboard with real-time data"""
        try:
            # Get current metrics
            data = self.metrics.get_metrics()
            temp = self.metrics.get_cpu_temperature()
            
            # Calculate health scores
            cpu_health = self.health_calc.calculate_component_health(data['cpu'], 'cpu')
            mem_health = self.health_calc.calculate_component_health(data['memory'], 'memory')
            disk_health = self.health_calc.calculate_component_health(data['disk'], 'disk')
            gpu_health = self.health_calc.calculate_component_health(data['gpu'], 'gpu')
            temp_health = self.health_calc.calculate_temp_health(temp)
            
            # Calculate overall health
            overall_health = self.health_calc.calculate_overall_health(
                cpu_health, mem_health, disk_health, gpu_health
            )
            
            # Get trend indicators
            cpu_trend = self.health_calc.get_trend_indicator(data['cpu'], self.previous_metrics['cpu'])
            mem_trend = self.health_calc.get_trend_indicator(data['memory'], self.previous_metrics['memory'])
            disk_trend = self.health_calc.get_trend_indicator(data['disk'], self.previous_metrics['disk'])
            gpu_trend = self.health_calc.get_trend_indicator(data['gpu'], self.previous_metrics['gpu'])
            
            # Update stat cards
            self.cpu_card.update_value(str(int(data['cpu'])), cpu_trend)
            self.mem_card.update_value(str(int(data['memory'])), mem_trend)
            self.disk_card.update_value(str(int(data['disk'])), disk_trend)
            self.gpu_card.update_value(str(int(data['gpu'])), gpu_trend)
            
            # Update health bars
            self.cpu_health_bar.update_health(cpu_health)
            self.mem_health_bar.update_health(mem_health)
            self.disk_health_bar.update_health(disk_health)
            self.overall_health_bar.update_health(overall_health)
            
            # Update header status if accessible
            status_text, status_color = self.health_calc.get_status_info(overall_health)
            if hasattr(self, 'main_window_header'):
                self.main_window_header.update_status(status_text, status_color)
            
            # Store current as previous for next comparison
            self.previous_metrics = data.copy()
            
        except Exception as e:
            print(f"Dashboard refresh error: {e}")
        
        # Schedule next refresh (3000ms = 3 seconds for smoother UI)
        self.after(3000, self.refresh_dashboard)


class DetailPanel(CTkFrame):
    """Detailed information panel with categories"""
    
    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Header
        header = CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=theme.spacing.lg, pady=(theme.spacing.lg, theme.spacing.md))
        
        header_label = CTkLabel(
            header,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        header_label.pack(anchor="w")
    
    def add_info_row(self, label: str, value: str):
        """Add information row to panel"""
        row_frame = CTkFrame(self, fg_color="transparent")
        row_frame.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.sm)
        
        label_widget = CTkLabel(
            row_frame,
            text=label,
            font=(theme.typography.font_primary, theme.typography.size_sm),
            text_color=theme.colors.text_secondary,
            width=200
        )
        label_widget.pack(side="left")
        
        value_widget = CTkLabel(
            row_frame,
            text=value,
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=theme.colors.text_primary
        )
        value_widget.pack(side="left", padx=theme.spacing.lg)


class SidebarTab(CTkFrame):
    """Sidebar navigation tab"""
    
    def __init__(self, parent, icon: str, label: str, command: Callable = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.is_active = False
        self.command = command
        
        # Create clickable frame
        self.tab_frame = CTkFrame(self, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.md)
        self.tab_frame.pack(fill="x", pady=theme.spacing.sm)
        self.tab_frame.bind("<Button-1>", self._on_click)
        
        content = CTkFrame(self.tab_frame, fg_color="transparent")
        content.pack(fill="x", padx=theme.spacing.md, pady=theme.spacing.md)
        content.bind("<Button-1>", self._on_click)
        
        icon_label = CTkLabel(
            content,
            text=icon,
            font=(theme.typography.font_primary, 18),
            text_color=theme.colors.accent_cyan,
            width=40
        )
        icon_label.pack(side="left", padx=(0, theme.spacing.md))
        icon_label.bind("<Button-1>", self._on_click)
        
        label_widget = CTkLabel(
            content,
            text=label,
            font=(theme.typography.font_primary, theme.typography.size_base),
            text_color=theme.colors.text_primary
        )
        label_widget.pack(side="left", expand=True, fill="x")
        label_widget.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def set_active(self, active: bool):
        """Set tab as active/inactive"""
        self.is_active = active
        if active:
            self.tab_frame.configure(fg_color=theme.colors.primary_accent)
        else:
            self.tab_frame.configure(fg_color=theme.colors.card_bg)


class Sidebar(CTkFrame):
    """Professional sidebar navigation"""
    
    def __init__(self, parent, on_tab_change: Callable = None, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_dark, width=280, **kwargs)
        self.pack_propagate(False)
        
        self.on_tab_change = on_tab_change
        self.tabs = {}
        
        # Title
        title = CTkLabel(
            self,
            text="Navigation",
            font=(theme.typography.font_primary, theme.typography.size_md, "bold"),
            text_color=theme.colors.text_primary
        )
        title.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, theme.spacing.md))
        
        # Navigation items
        nav_frame = CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)
        
        # Add tabs
        self._add_tab("📊 Dashboard", "dashboard", nav_frame)
        self._add_tab("🔍 Hardware Info", "hardware", nav_frame)
        self._add_tab("📈 Performance", "performance", nav_frame)
        self._add_tab("🤖 AI Diagnostics", "diagnostics", nav_frame)
        self._add_tab("📡 Live Monitor", "monitor", nav_frame)
        self._add_tab("🔧 Benchmarks", "benchmarks", nav_frame)
        
        # Divider
        divider = CTkFrame(self, fg_color=theme.colors.border_medium, height=1)
        divider.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Settings section
        settings_label = CTkLabel(
            self,
            text="Settings",
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=theme.colors.text_tertiary
        )
        settings_label.pack(padx=theme.spacing.lg, pady=(0, theme.spacing.md))
        
        settings_frame = CTkFrame(self, fg_color="transparent")
        settings_frame.pack(fill="x", padx=theme.spacing.md)
        
        self._add_tab("⚙️ Settings", "settings", settings_frame)
        self._add_tab("ℹ️ About", "about", settings_frame)
    
    def _add_tab(self, label: str, key: str, parent: CTkFrame):
        """Add navigation tab"""
        def on_select():
            # Deselect all
            for tab in self.tabs.values():
                tab.set_active(False)
            # Select current
            self.tabs[key].set_active(True)
            if self.on_tab_change:
                self.on_tab_change(key)
        
        tab = SidebarTab(parent, label.split()[0], label.split()[1], command=on_select)
        tab.pack(fill="x", pady=theme.spacing.sm)
        self.tabs[key] = tab
        
        # Select first tab by default
        if key == "dashboard":
            tab.set_active(True)


class MainWindow(ctk.CTk):
    """Professional main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("SysOptima - System Intelligence Platform")
        self.geometry("1600x900")
        self.configure(fg_color=theme.colors.primary_dark)
        
        # Set window icon (optional)
        try:
            self.iconbitmap('assets/icon.ico')
        except:
            pass
        
        self.detector = HardwareDetector()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup main UI structure"""
        
        # Header (store reference)
        self.header = HeaderBar(self, height=70)
        self.header.pack(fill="x", side="top")
        
        # Main content area
        content_frame = CTkFrame(self, fg_color=theme.colors.primary_bg)
        content_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(content_frame, on_tab_change=self._on_tab_change)
        self.sidebar.pack(fill="both", expand=False, side="left", padx=0)
        
        # Content area
        self.content_area = CTkFrame(content_frame, fg_color=theme.colors.primary_bg)
        self.content_area.pack(fill="both", expand=True, side="left")
        
        # Show dashboard by default
        self._show_dashboard()
    
    def _on_tab_change(self, tab_key: str):
        """Handle tab change"""
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if tab_key == "dashboard":
            self._show_dashboard()
        elif tab_key == "hardware":
            self._show_hardware()
        elif tab_key == "performance":
            self._show_performance()
        elif tab_key == "diagnostics":
            self._show_diagnostics()
        elif tab_key == "monitor":
            self._show_monitor()
        elif tab_key == "benchmarks":
            self._show_benchmarks()
        else:
            self._show_placeholder(tab_key)
    
    def _show_dashboard(self):
        """Show dashboard view"""
        dashboard = DashboardPanel(self.content_area)
        dashboard.pack(fill="both", expand=True)
        # Pass header reference to dashboard for status updates
        dashboard.main_window_header = self.header
    
    def _show_hardware(self):
        """Show hardware information - REAL system data, static on load"""
        scroll_frame = CTkScrollableFrame(
            self.content_area,
            fg_color=theme.colors.primary_bg,
            label_text="Hardware Information"
        )
        scroll_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Get REAL hardware information
        hw_info = get_all_hardware_info()
        cpu = hw_info["cpu"]
        memory = hw_info["memory"]
        storage = hw_info["storage"]
        gpu = hw_info["gpu"]
        os_info = hw_info["os"]
        
        # CPU Info (REAL DATA)
        cpu_panel = DetailPanel(scroll_frame, "🔧 CPU Information")
        cpu_panel.pack(fill="x", pady=theme.spacing.md)
        cpu_panel.add_info_row("Processor", cpu["name"])
        
        # Format core count display
        if cpu["physical_cores"] != cpu["logical_cores"]:
            cores_text = f'{cpu["logical_cores"]} threads ({cpu["physical_cores"]} physical cores)'
        else:
            cores_text = f'{cpu["physical_cores"]} cores'
        cpu_panel.add_info_row("Cores", cores_text)
        
        if cpu["base_freq"] > 0:
            cpu_panel.add_info_row("Base Frequency", f'{cpu["base_freq"]} GHz')
        if cpu["max_freq"] > 0:
            cpu_panel.add_info_row("Max Frequency", f'{cpu["max_freq"]} GHz')
        
        # Memory Info (REAL DATA)
        mem_panel = DetailPanel(scroll_frame, "💾 Memory Information")
        mem_panel.pack(fill="x", pady=theme.spacing.md)
        mem_panel.add_info_row("Total RAM", f'{memory["total_gb"]} GB')
        mem_panel.add_info_row("Available", f'{memory["available_gb"]} GB')
        mem_panel.add_info_row("Used", f'{memory["used_gb"]} GB')
        mem_panel.add_info_row("Usage", f'{memory["percent"]}%')
        mem_panel.add_info_row("Type", memory["type"] + " (Python cannot detect DDR generation)")
        
        # Storage Info (REAL DATA)
        disk_panel = DetailPanel(scroll_frame, "💿 Storage Information")
        disk_panel.pack(fill="x", pady=theme.spacing.md)
        disk_panel.add_info_row("Drive", storage["path"])
        disk_panel.add_info_row("Total Capacity", f'{storage["total_gb"]} GB')
        disk_panel.add_info_row("Used Space", f'{storage["used_gb"]} GB')
        disk_panel.add_info_row("Available Space", f'{storage["free_gb"]} GB')
        disk_panel.add_info_row("Usage", f'{storage["percent"]}%')
        
        # GPU Info (REAL DATA - best effort)
        gpu_panel = DetailPanel(scroll_frame, "🎮 GPU Information")
        gpu_panel.pack(fill="x", pady=theme.spacing.md)
        gpu_panel.add_info_row("Graphics Card", gpu["name"])
        if gpu["available"]:
            gpu_panel.add_info_row("Video Memory", f'{gpu["memory_total_mb"]} MB')
            gpu_panel.add_info_row("Driver Version", gpu["driver"])
        
        # OS Info (REAL DATA)
        os_panel = DetailPanel(scroll_frame, "💻 Operating System")
        os_panel.pack(fill="x", pady=theme.spacing.md)
        os_panel.add_info_row("System", f'{os_info["system"]} {os_info["release"]}')
        os_panel.add_info_row("Architecture", os_info["architecture"])
        os_panel.add_info_row("Platform", os_info["platform"])
    
    def _show_diagnostics(self):
        """Show AI diagnostics"""
        scroll_frame = CTkScrollableFrame(
            self.content_area,
            fg_color=theme.colors.primary_bg,
            label_text="AI-Powered System Diagnostics"
        )
        scroll_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Analysis results
        analysis_panel = DetailPanel(scroll_frame, "🤖 System Analysis Results")
        analysis_panel.pack(fill="x", pady=theme.spacing.md)
        analysis_panel.add_info_row("Overall Health Score", "85/100 - Excellent")
        analysis_panel.add_info_row("Last Analysis", "2 minutes ago")
        analysis_panel.add_info_row("Issues Detected", "2 minor")
        
        # Recommendations
        rec_panel = DetailPanel(scroll_frame, "💡 Recommendations")
        rec_panel.pack(fill="x", pady=theme.spacing.md)
        rec_panel.add_info_row("Priority 1", "Clear cache files (~2.3 GB)")
        rec_panel.add_info_row("Priority 2", "Update GPU drivers")
        rec_panel.add_info_row("Priority 3", "Optimize startup programs")
    
    def _show_performance(self):
        """Show Performance Reports interface"""
        PerformanceReportsPanel(self.content_area).pack(fill="both", expand=True)
    
    def _show_monitor(self):
        """Show Live Monitor with real-time charts"""
        LiveMonitorPanel(self.content_area).pack(fill="both", expand=True)
    
    def _show_benchmarks(self):
        """Show Live Monitor with real-time charts"""
        LiveMonitorPanel(self.content_area).pack(fill="both", expand=True)
    
    def _show_placeholder(self, tab_key: str):
        """Show placeholder for unimplemented tabs"""
        frame = CTkFrame(self.content_area, fg_color="transparent")
        frame.pack(fill="both", expand=True)
        
        label = CTkLabel(
            frame,
            text=f"Coming Soon: {tab_key.upper()}",
            font=(theme.typography.font_primary, theme.typography.size_lg, "bold"),
            text_color=theme.colors.text_secondary
        )
        label.pack(expand=True)


def main():
    """Main entry point"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
