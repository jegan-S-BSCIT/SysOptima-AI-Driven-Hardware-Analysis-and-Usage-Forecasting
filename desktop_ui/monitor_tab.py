"""
System Monitor Tab - Real-time Hardware Monitoring with Charts
Displays CPU, RAM, GPU, and Disk metrics with matplotlib visualization
"""

import tkinter as tk
from tkinter import ttk
import psutil
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os
from desktop_ui.styles import COLORS, FONTS, SPACING

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import GPUtil
    HAS_GPUTIL = True
except ImportError:
    HAS_GPUTIL = False


class MonitorTab:
    """Real-time system monitoring with live charts"""
    
    def __init__(self, parent):
        """Initialize monitor tab"""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Data history (last 60 seconds)
        self.history_size = 60
        self.cpu_history = deque(maxlen=self.history_size)
        self.ram_history = deque(maxlen=self.history_size)
        self.gpu_history = deque(maxlen=self.history_size)
        self.disk_history = deque(maxlen=self.history_size)
        
        # UI state
        self.metrics_labels = {}
        self.health_label = None
        self.health_status = None

        # Create layout
        self.create_widgets()
        self.update_metrics()
    
    def create_widgets(self):
        """Create UI widgets"""

        # Background container
        container = tk.Frame(self.frame, bg=COLORS["bg_main"])
        container.pack(fill=tk.BOTH, expand=True)

        # Top: Summary cards
        summary_frame = tk.LabelFrame(
            container,
            text="System Summary",
            bg=COLORS["bg_main"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
            padx=SPACING["md"],
            pady=SPACING["md"]
        )
        summary_frame.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["md"])

        # Card grid
        cards_frame = tk.Frame(summary_frame, bg=COLORS["bg_main"])
        cards_frame.pack(fill=tk.X)

        for i in range(5):
            cards_frame.grid_columnconfigure(i, weight=1, uniform="card")

        self._create_metric_card(cards_frame, 0, "CPU Usage", "cpu")
        self._create_metric_card(cards_frame, 1, "RAM Usage", "ram")
        self._create_metric_card(cards_frame, 2, "GPU Usage", "gpu")
        self._create_metric_card(cards_frame, 3, "Disk Usage", "disk")
        self._create_health_card(cards_frame, 4, "System Health")

        # Middle: Charts (Tabbed)
        charts_frame = tk.LabelFrame(
            container,
            text="Performance Charts (Last 60 seconds)",
            bg=COLORS["bg_main"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
            padx=SPACING["md"],
            pady=SPACING["md"]
        )
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING["lg"], pady=SPACING["md"])

        self.charts_notebook = ttk.Notebook(charts_frame)
        self.charts_notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: CPU + RAM
        tab_cpu_ram = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(tab_cpu_ram, text="CPU + RAM")
        self.figure_cpu_ram = Figure(figsize=(8, 3.5), dpi=100)
        self.figure_cpu_ram.patch.set_facecolor(COLORS["bg_card"])
        self.ax_cpu = self.figure_cpu_ram.add_subplot(121)
        self.ax_ram = self.figure_cpu_ram.add_subplot(122)
        self._configure_axis(self.ax_cpu, "CPU Usage (%)")
        self._configure_axis(self.ax_ram, "RAM Usage (%)")
        self.canvas_cpu_ram = FigureCanvasTkAgg(self.figure_cpu_ram, master=tab_cpu_ram)
        self.canvas_cpu_ram.draw()
        self.canvas_cpu_ram.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=SPACING["sm"], pady=SPACING["sm"])

        # Tab 2: GPU + Disk
        tab_gpu_disk = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(tab_gpu_disk, text="GPU + Disk")
        self.figure_gpu_disk = Figure(figsize=(8, 3.5), dpi=100)
        self.figure_gpu_disk.patch.set_facecolor(COLORS["bg_card"])
        self.ax_gpu = self.figure_gpu_disk.add_subplot(121)
        self.ax_disk = self.figure_gpu_disk.add_subplot(122)
        self._configure_axis(self.ax_gpu, "GPU Usage (%)")
        self._configure_axis(self.ax_disk, "Disk Usage (%)")
        self.canvas_gpu_disk = FigureCanvasTkAgg(self.figure_gpu_disk, master=tab_gpu_disk)
        self.canvas_gpu_disk.draw()
        self.canvas_gpu_disk.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=SPACING["sm"], pady=SPACING["sm"])

    def _configure_axis(self, ax, title):
        ax.set_title(title, fontsize=10, fontweight="bold", color=COLORS["text_main"])
        ax.set_ylim(0, 100)
        ax.set_facecolor(COLORS["bg_card"])
        ax.set_xlabel("Time (s)", fontsize=8, color=COLORS["text_muted"])
        ax.set_ylabel("Usage %", fontsize=8, color=COLORS["text_muted"])
        ax.tick_params(labelsize=8, colors=COLORS["text_muted"])
        ax.grid(True, alpha=0.25, color=COLORS["chart_grid"])

    def _create_metric_card(self, parent, column, title, key):
        card = tk.Frame(parent, bg=COLORS["bg_card"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.grid(row=0, column=column, padx=6, pady=6, sticky="nsew")

        title_label = tk.Label(card, text=title, bg=COLORS["bg_card"], fg=COLORS["text_dim"], font=FONTS["small"])
        title_label.pack(anchor="w", padx=SPACING["md"], pady=(SPACING["sm"], 0))

        value_label = tk.Label(card, text="0%", bg=COLORS["bg_card"], fg=COLORS["text_main"], font=("Segoe UI", 18, "bold"))
        value_label.pack(anchor="w", padx=SPACING["md"], pady=(2, 0))

        status_label = tk.Label(card, text="Optimal", bg=COLORS["bg_card"], fg=COLORS["success"], font=FONTS["small"])
        status_label.pack(anchor="w", padx=SPACING["md"], pady=(0, SPACING["sm"]))

        self.metrics_labels[key] = {
            "value": value_label,
            "status": status_label
        }

    def _create_health_card(self, parent, column, title):
        card = tk.Frame(parent, bg=COLORS["bg_card"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.grid(row=0, column=column, padx=6, pady=6, sticky="nsew")

        title_label = tk.Label(card, text=title, bg=COLORS["bg_card"], fg=COLORS["text_dim"], font=FONTS["small"])
        title_label.pack(anchor="w", padx=SPACING["md"], pady=(SPACING["sm"], 0))

        self.health_label = tk.Label(card, text="100%", bg=COLORS["bg_card"], fg=COLORS["text_main"], font=("Segoe UI", 18, "bold"))
        self.health_label.pack(anchor="w", padx=SPACING["md"], pady=(2, 0))

        self.health_status = tk.Label(card, text="Optimal", bg=COLORS["bg_card"], fg=COLORS["success"], font=FONTS["small"])
        self.health_status.pack(anchor="w", padx=SPACING["md"], pady=(0, SPACING["sm"]))
    
    def update_metrics(self):
        """Update system metrics and refresh display"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_history.append(cpu_percent)
            self._update_card("cpu", cpu_percent)
            
            # Get RAM usage
            ram_info = psutil.virtual_memory()
            ram_percent = ram_info.percent
            self.ram_history.append(ram_percent)
            self._update_card("ram", ram_percent)
            
            # Get Disk usage
            disk_info = psutil.disk_usage('/')
            disk_percent = disk_info.percent
            self.disk_history.append(disk_percent)
            self._update_card("disk", disk_percent)
            
            # Get GPU usage (if available)
            gpu_percent = None
            if HAS_GPUTIL:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu_percent = gpus[0].load * 100
                        self.gpu_history.append(gpu_percent)
                        self._update_card("gpu", gpu_percent)
                except:
                    self._set_card_na("gpu")
            else:
                self._set_card_na("gpu")

            # Update overall health
            health = self._calculate_health(cpu_percent, ram_percent, disk_percent, gpu_percent)
            self._update_health(health)
            
            # Update charts
            self.update_charts()
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
    
    def update_charts(self):
        """Update matplotlib charts with new data"""
        try:
            # Clear previous plots
            self.ax_cpu.clear()
            self.ax_ram.clear()
            self.ax_gpu.clear()
            self.ax_disk.clear()

            # Plot data
            x = list(range(len(self.cpu_history)))

            self._configure_axis(self.ax_cpu, "CPU Usage (%)")
            self._configure_axis(self.ax_ram, "RAM Usage (%)")
            self._configure_axis(self.ax_gpu, "GPU Usage (%)")
            self._configure_axis(self.ax_disk, "Disk Usage (%)")

            self.ax_cpu.plot(x, list(self.cpu_history), color=COLORS["accent"], linewidth=2)
            self.ax_cpu.fill_between(x, self.cpu_history, color=COLORS["accent_hover"], alpha=0.35)

            self.ax_ram.plot(x, list(self.ram_history), color=COLORS["success"], linewidth=2)
            self.ax_ram.fill_between(x, self.ram_history, color=COLORS["success"], alpha=0.25)

            if self.gpu_history:
                self.ax_gpu.plot(x, list(self.gpu_history), color=COLORS["warning"], linewidth=2)
                self.ax_gpu.fill_between(x, self.gpu_history, color=COLORS["warning"], alpha=0.25)

            self.ax_disk.plot(x, list(self.disk_history), color=COLORS["info"], linewidth=2)
            self.ax_disk.fill_between(x, self.disk_history, color=COLORS["info"], alpha=0.25)

            # Adjust layout and redraw
            self.figure_cpu_ram.tight_layout()
            self.figure_gpu_disk.tight_layout()
            self.canvas_cpu_ram.draw_idle()
            self.canvas_gpu_disk.draw_idle()
            
        except Exception as e:
            print(f"Error updating charts: {e}")

    def _update_card(self, key, value):
        status_text, status_color = self._status_from_value(value)
        if key in self.metrics_labels:
            self.metrics_labels[key]["value"].config(text=f"{value:.0f}%")
            self.metrics_labels[key]["status"].config(text=status_text, fg=status_color)

    def _set_card_na(self, key):
        if key in self.metrics_labels:
            self.metrics_labels[key]["value"].config(text="N/A")
            self.metrics_labels[key]["status"].config(text="Unavailable", fg=COLORS["text_muted"])

    def _status_from_value(self, value):
        if value >= 85:
            return "Critical", COLORS["danger"]
        if value >= 70:
            return "High", COLORS["warning"]
        return "Optimal", COLORS["success"]

    def _calculate_health(self, cpu, ram, disk, gpu):
        values = [cpu, ram, disk]
        if gpu is not None:
            values.append(gpu)
        avg = sum(values) / len(values)
        health = max(0, min(100, 100 - avg))
        return health

    def _update_health(self, health):
        status_text, status_color = self._status_from_value(100 - health)
        if self.health_label and self.health_status:
            self.health_label.config(text=f"{health:.0f}%")
            self.health_status.config(text=status_text, fg=status_color)
    
    def cleanup(self):
        """Cleanup resources"""
        pass
