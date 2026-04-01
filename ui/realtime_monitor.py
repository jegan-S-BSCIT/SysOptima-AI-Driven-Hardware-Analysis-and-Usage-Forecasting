"""
Real-Time Performance Monitor UI - Tkinter + Matplotlib
========================================================
Professional live performance dashboard with embedded charts.

Features:
- 4 live charts (CPU, RAM, GPU, Disk I/O)
- 60-second sliding window display
- Real-time diagnostic flags
- Non-blocking UI updates
- Clean academic design

For B.Sc. IT Project: "Intelligent Computer Performance Analysis and Guidance System"
========================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import psutil
import time

# GPUtil is optional; we fall back to 0 when unavailable
try:
    import GPUtil
except Exception:  # pragma: no cover - optional dependency
    GPUtil = None


class RealtimeMonitorView(ttk.Frame):
    """
    Real-time performance monitor UI component.
    
    Displays live metrics in 4 charts with automatic updates every 1 second.
    Integrates Matplotlib charts directly into Tkinter.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the Real-Time Monitor View.
        
        Args:
            parent: Tkinter parent widget
        """
        super().__init__(parent, *args, **kwargs)
        
        # Configuration
        self.buffer_size = 60  # 60-second rolling window
        self.update_interval_ms = 1000  # 1 second

        # Rolling buffers
        self.cpu_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.ram_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.gpu_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.disk_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)

        # Disk delta tracking
        self._prev_disk_io = psutil.disk_io_counters()
        self._prev_time = time.time()

        # UI state
        self.monitoring = False
        self.after_job = None
        
        # Build UI
        self._build_header()
        self._build_charts()
        self._build_diagnostics_panel()
        
        # Initial layout
        self.pack(fill="both", expand=True)

    def _build_header(self):
        """Build the header section with title and control buttons."""
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=15)
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="Real-Time Performance Monitor",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(side="left", anchor="w")

        # Controls (start/stop above charts for clarity)
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side="right", anchor="e", padx=(0, 10))

        self.start_button = ttk.Button(
            controls_frame,
            text="▶ Start Monitoring",
            command=self._start_monitoring
        )
        self.start_button.pack(side="left", padx=4)
        
        self.stop_button = ttk.Button(
            controls_frame,
            text="⏹ Stop Monitoring",
            command=self._stop_monitoring,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=4)
        
        # Status indicator
        self.status_label = ttk.Label(
            header_frame,
            text="● Idle",
            font=("Segoe UI", 12),
            foreground="gray"
        )
        self.status_label.pack(side="right", anchor="e")

    def _build_charts(self):
        """Build the 4-chart monitoring dashboard."""
        charts_frame = ttk.Frame(self)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create figure with 2x2 subplots
        self.figure = Figure(figsize=(14, 8), dpi=100)
        self.figure.patch.set_facecolor("#F8F9FA")

        # Axes for each metric
        self.ax_cpu = self.figure.add_subplot(2, 2, 1)
        self.ax_ram = self.figure.add_subplot(2, 2, 2)
        self.ax_gpu = self.figure.add_subplot(2, 2, 3)
        self.ax_disk = self.figure.add_subplot(2, 2, 4)

        # Configure axes styling
        self._configure_axis_style(self.ax_cpu, "CPU Usage (%)", 0, 100)
        self._configure_axis_style(self.ax_ram, "RAM Usage (%)", 0, 100)
        self._configure_axis_style(self.ax_gpu, "GPU Usage (%)", 0, 100)
        self._configure_axis_style(self.ax_disk, "Disk Activity (MB/s)", 0, 200)

        # Pre-create line objects for efficient updates
        x_axis = list(range(-self.buffer_size + 1, 1))
        (self.cpu_line,) = self.ax_cpu.plot(x_axis, list(self.cpu_data), color="#3B82F6", linewidth=2)
        (self.ram_line,) = self.ax_ram.plot(x_axis, list(self.ram_data), color="#10B981", linewidth=2)
        (self.gpu_line,) = self.ax_gpu.plot(x_axis, list(self.gpu_data), color="#F59E0B", linewidth=2)
        (self.disk_line,) = self.ax_disk.plot(x_axis, list(self.disk_data), color="#EF4444", linewidth=2)
        self.ax_disk.legend([self.disk_line], ["Total I/O"], loc="upper left", fontsize=8)

        self.figure.tight_layout()

        # Embed in Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=charts_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Reset button stays near charts for convenience
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.reset_button = ttk.Button(
            button_frame,
            text="🔄 Reset Data",
            command=self._reset_data
        )
        self.reset_button.pack(side="left", padx=5)

    def _build_diagnostics_panel(self):
        """Build the diagnostic indicators panel."""
        diag_frame = ttk.LabelFrame(
            self,
            text="System Diagnostics",
            padding=15
        )
        diag_frame.pack(fill="x", padx=20, pady=10)
        
        # Create indicator labels
        self.diag_labels = {
            'high_cpu_load': ttk.Label(
                diag_frame,
                text="⚠ High CPU Load: —",
                font=("Segoe UI", 10)
            ),
            'memory_pressure': ttk.Label(
                diag_frame,
                text="⚠ Memory Pressure: —",
                font=("Segoe UI", 10)
            ),
            'disk_bottleneck': ttk.Label(
                diag_frame,
                text="⚠ Disk Bottleneck: —",
                font=("Segoe UI", 10)
            ),
            'gpu_unavailable': ttk.Label(
                diag_frame,
                text="ℹ GPU Unavailable: —",
                font=("Segoe UI", 10)
            ),
        }
        
        for label in self.diag_labels.values():
            label.pack(anchor="w", pady=3)

    def _configure_axis_style(self, ax, title, y_min, y_max):
        """
        Configure matplotlib axis styling.
        
        Args:
            ax: Matplotlib axis object
            title: Chart title
            y_min: Minimum Y-axis value
            y_max: Maximum Y-axis value
        """
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
        ax.set_xlabel("Time (seconds ago)", fontsize=9)
        ax.set_ylabel("Value", fontsize=9)
        ax.set_ylim(y_min, y_max)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.set_facecolor("#FFFFFF")

    def _start_monitoring(self):
        """Start the monitoring engine and UI updates."""
        if self.monitoring:
            return
        
        self.monitoring = True
        
        # Update UI button states
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="● Monitoring", foreground="green")

        # Begin after-loop updates (no threads)
        self._schedule_next_update()

        print("[Monitor UI] Monitoring started")

    def _stop_monitoring(self):
        """Stop the monitoring engine and UI updates."""
        if not self.monitoring:
            return
        
        self.monitoring = False
        
        # Cancel scheduled update if any
        if self.after_job is not None:
            self.after_cancel(self.after_job)
            self.after_job = None

        # Update UI button states
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="● Stopped", foreground="red")

        print("[Monitor UI] Monitoring stopped")

    def _reset_data(self):
        """Clear all collected data and restart monitoring."""
        was_monitoring = self.monitoring
        
        # Stop if running
        if was_monitoring:
            self._stop_monitoring()

        # Clear buffers
        self.cpu_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.ram_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.gpu_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.disk_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)

        # Reset lines
        self._refresh_lines()

        # Restart if was monitoring
        if was_monitoring:
            self._start_monitoring()

        print("[Monitor UI] Data reset")

    def _schedule_next_update(self):
        """Schedule the next monitor refresh using Tkinter's after."""
        # after keeps updates on the Tk event loop, avoiding threads and UI freezes
        if self.monitoring:
            self.after_job = self.after(self.update_interval_ms, self._update_monitor)

    def _update_monitor(self):
        """Collect metrics, refresh buffers, redraw lines, and reschedule."""
        try:
            snapshot = self._collect_snapshot()
            self.cpu_data.append(snapshot["cpu_percent"])
            self.ram_data.append(snapshot["ram_percent"])
            self.gpu_data.append(snapshot["gpu_percent"])
            self.disk_data.append(snapshot["disk_total_mb"])

            diagnostics = self._compute_diagnostics()
            self._refresh_lines(diagnostics)
        finally:
            self._schedule_next_update()

    def _collect_snapshot(self):
        """Gather one set of metrics (CPU, RAM, GPU, Disk)."""
        cpu_percent = psutil.cpu_percent(interval=0)
        ram_percent = psutil.virtual_memory().percent

        # GPU percent with graceful fallback
        gpu_percent = 0.0
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_percent = float(gpus[0].load * 100)
            except Exception:
                gpu_percent = 0.0

        disk_io = psutil.disk_io_counters()
        now = time.time()
        elapsed = max(now - self._prev_time, 0.001)
        # Convert read/write byte deltas into MB/s for a smoother disk line
        disk_total_mb = (
            (disk_io.read_bytes - self._prev_disk_io.read_bytes)
            + (disk_io.write_bytes - self._prev_disk_io.write_bytes)
        ) / (1024 ** 2 * elapsed)

        self._prev_disk_io = disk_io
        self._prev_time = now

        return {
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "gpu_percent": gpu_percent,
            "disk_total_mb": disk_total_mb,
        }

    def _compute_diagnostics(self):
        """Compute simple diagnostics for viva-ready explanation."""
        diag = {
            "high_cpu_load": False,
            "memory_pressure": False,
            "disk_bottleneck": False,
            "gpu_unavailable": False,
        }

        # High CPU if last 10 seconds mostly above 85%
        recent_cpu = list(self.cpu_data)[-10:]
        if recent_cpu and sum(1 for v in recent_cpu if v > 85) >= 7:
            diag["high_cpu_load"] = True

        # Memory pressure if current sample above 80%
        if self.ram_data:
            diag["memory_pressure"] = self.ram_data[-1] > 80

        # Disk bottleneck: average of last 5 samples above ~50 MB/s
        recent_disk = list(self.disk_data)[-5:]
        if recent_disk:
            avg_disk = sum(recent_disk) / len(recent_disk)
            diag["disk_bottleneck"] = avg_disk > 50

        # GPU unavailable if GPUtil missing or reports none
        if GPUtil is None:
            diag["gpu_unavailable"] = True
        else:
            try:
                diag["gpu_unavailable"] = len(GPUtil.getGPUs()) == 0
            except Exception:
                diag["gpu_unavailable"] = True

        return diag

    def _refresh_lines(self, diagnostics=None):
        """Update line data, axes, and diagnostics display."""
        x_axis = list(range(-len(self.cpu_data) + 1, 1))

        # Update line data
        self.cpu_line.set_data(x_axis, list(self.cpu_data))
        self.ram_line.set_data(x_axis, list(self.ram_data))
        self.gpu_line.set_data(x_axis, list(self.gpu_data))
        self.disk_line.set_data(x_axis, list(self.disk_data))

        # Axes limits
        for ax in [self.ax_cpu, self.ax_ram, self.ax_gpu]:
            ax.set_xlim(-self.buffer_size + 1, 0)
            ax.set_ylim(0, 100)
            ax.set_xticks([-60, -45, -30, -15, 0])
            ax.set_xticklabels(["60s", "45s", "30s", "15s", "0s"])

        # Disk axis scales dynamically
        self.ax_disk.set_xlim(-self.buffer_size + 1, 0)
        disk_max = max(max(self.disk_data), 10)
        self.ax_disk.set_ylim(0, disk_max * 1.1)
        self.ax_disk.set_xticks([-60, -45, -30, -15, 0])
        self.ax_disk.set_xticklabels(["60s", "45s", "30s", "15s", "0s"])

        # Redraw
        self.figure.tight_layout()
        self.canvas.draw_idle()

        if diagnostics:
            self._update_diagnostics_display(diagnostics)

    def _update_diagnostics_display(self, diagnostics):
        """
        Update diagnostic indicator labels.
        
        Args:
            diagnostics: Dictionary of diagnostic flags
        """
        # High CPU Load
        status = "🔴 YES" if diagnostics['high_cpu_load'] else "🟢 NO"
        self.diag_labels['high_cpu_load'].config(
            text=f"⚠ High CPU Load (>85% recent): {status}"
        )

        # Memory Pressure
        status = "🔴 YES" if diagnostics['memory_pressure'] else "🟢 NO"
        self.diag_labels['memory_pressure'].config(
            text=f"⚠ Memory Pressure (>80% current): {status}"
        )

        # Disk Bottleneck
        status = "🔴 YES" if diagnostics['disk_bottleneck'] else "🟢 NO"
        self.diag_labels['disk_bottleneck'].config(
            text=f"⚠ Disk Bottleneck (>50 MB/s growth): {status}"
        )
        
        # GPU Unavailable
        status = "⚠ N/A" if diagnostics['gpu_unavailable'] else "✓ Available"
        self.diag_labels['gpu_unavailable'].config(
            text=f"ℹ GPU Status: {status}"
        )

    def on_closing(self):
        """Clean up when the view is closing."""
        if self.monitoring:
            self._stop_monitoring()
        if self.after_job is not None:
            self.after_cancel(self.after_job)
            self.after_job = None
