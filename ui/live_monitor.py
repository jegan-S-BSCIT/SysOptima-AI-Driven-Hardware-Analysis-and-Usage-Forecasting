"""
Live System Monitor with AI Integration
Redesigned: 2-Panel Layout (Hardware + AI Log), No Chatbot
"""

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkProgressBar, CTkScrollableFrame, CTkButton
import threading
import time
from datetime import datetime

from ui.theme import theme
from core.system_metrics import SystemMetrics

class LiveMonitorPanel(CTkFrame):
    """
    Split-view Live Monitor:
    Left: Hardware Monitor (Real-time)
    Right: Live AI Insights (Read-Only Log)
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_bg, **kwargs)

        # Logic
        self.metrics = SystemMetrics()
        self.monitoring = False
        
        # State Tracking for AI Triggers
        self.previous_state = {
            "cpu": 0, "memory": 0, "disk": 0, "gpu": 0
        }
        # Track active alerts to prevent repetition
        self.triggers_active = {
            "cpu_high": False, 
            "memory_crit": False, 
            "temp_high": False,
            "gpu_high": False
        }
        
        # Layout
        self.grid_columnconfigure(0, weight=4) # Left Panel (Metrics)
        self.grid_columnconfigure(1, weight=5) # Right Panel (Insights)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL: HARDWARE MONITOR ---
        self.left_panel = CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Header
        CTkLabel(
            self.left_panel, 
            text="📡 Live Hardware Monitor", 
            font=(theme.typography.font_primary, 20, "bold"), 
            text_color=theme.colors.text_primary
        ).pack(anchor="w", pady=(0, 5))
        
        # Subtitle / Status
        self.status_lbl = CTkLabel(
            self.left_panel, 
            text="● Monitoring Active", 
            font=(theme.typography.font_primary, 12), 
            text_color=theme.colors.success
        )
        self.status_lbl.pack(anchor="w", pady=(0, 20))

        # Metrics Container
        self.metrics_container = CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.metrics_container.pack(fill="both", expand=True)
        
        # Hardware Cards (CPU, RAM, Disk, GPU)
        self.cpu_card = LiveMetricCard(self.metrics_container, "CPU Usage", "⚡")
        self.cpu_card.pack(fill="x", pady=6)
        
        self.ram_card = LiveMetricCard(self.metrics_container, "RAM Usage", "💾")
        self.ram_card.pack(fill="x", pady=6)
        
        self.disk_card = LiveMetricCard(self.metrics_container, "Disk Activity", "💿")
        self.disk_card.pack(fill="x", pady=6)
        
        self.gpu_card = LiveMetricCard(self.metrics_container, "GPU Load", "🎮")
        self.gpu_card.pack(fill="x", pady=6)

        # --- RIGHT PANEL: AI INSIGHTS ---
        self.right_panel = CTkFrame(self, fg_color=theme.colors.card_bg, corner_radius=12)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, theme.spacing.lg), pady=theme.spacing.lg)
        
        # Insights Header
        header_frame = CTkFrame(self.right_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        CTkLabel(
            header_frame, 
            text="Live AI Insights", 
            font=(theme.typography.font_primary, 18, "bold"), 
            text_color=theme.colors.text_primary
        ).pack(anchor="w")
        
        CTkLabel(
            header_frame, 
            text="Real-time system interpretation", 
            font=(theme.typography.font_primary, 13), 
            text_color=theme.colors.text_secondary
        ).pack(anchor="w")

        # Separator
        ctk.CTkFrame(self.right_panel, fg_color=theme.colors.border_light, height=1).pack(fill="x", padx=20)

        # Insights Log (Scrollable)
        self.insights_log = CTkScrollableFrame(self.right_panel, fg_color="transparent")
        self.insights_log.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize Insights
        self.add_insight("AI Watchdog initialized. Monitoring system metrics...", "info")

        # Retry UI (Hidden initially)
        self.retry_btn = CTkButton(
            self.left_panel, 
            text="Retry Connection", 
            fg_color=theme.colors.primary_accent,
            command=self.start_monitoring
        )
        # Note: We won't pack it unless error occurs

        # Start Monitoring
        self.start_monitoring()

    def start_monitoring(self):
        self.monitoring = True
        self.status_lbl.configure(text="● Monitoring Active", text_color=theme.colors.success)
        self.retry_btn.pack_forget()
        
        # Start background thread
        threading.Thread(target=self._update_loop, daemon=True).start()

    def stop_monitoring(self):
        self.monitoring = False
        self.status_lbl.configure(text="● Monitoring Paused", text_color=theme.colors.text_disabled)

    def destroy(self):
        self.stop_monitoring()
        super().destroy()

    def _update_loop(self):
        """Background loop for real-time data"""
        while self.monitoring:
            try:
                # 1. Fetch Data
                data = self.metrics.get_metrics()
                temp = self.metrics.get_cpu_temperature()
                
                # 2. Check Triggers (Logic-based AI)
                self._check_ai_triggers(data, temp)
                
                # 3. Update UI (Thread-safe)
                self.after(0, lambda: self._update_ui(data, temp))
                
                # 4. Save state
                self.previous_state = data.copy()
                
                # 5. Throttle (1.5s)
                time.sleep(1.5)
                
            except Exception as e:
                print(f"Live Monitor Error: {e}")
                self.after(0, self._handle_error)
                self.monitoring = False
                break

    def _handle_error(self):
        self.status_lbl.configure(text="● Live monitoring unavailable", text_color=theme.colors.danger)
        self.retry_btn.pack(pady=10, anchor="w")
        self.add_insight("Sensors unavailable. Check permissions or driver status.", "critical")

    def _update_ui(self, data, temp):
        try:
            # CPU
            cpu_status, cpu_col = self._get_status(data['cpu'], 80, 90)
            self.cpu_card.update_data(f"{int(data['cpu'])}%", data['cpu']/100, cpu_col, cpu_status, f"{temp}°C")
            
            # RAM
            ram_status, ram_col = self._get_status(data['memory'], 75, 90)
            self.ram_card.update_data(f"{int(data['memory'])}%", data['memory']/100, ram_col, ram_status, "Used")
            
            # Disk
            disk_status, disk_col = self._get_status(data['disk'], 85, 95)
            self.disk_card.update_data(f"{int(data['disk'])}%", data['disk']/100, disk_col, disk_status, "Full")
            
            # GPU
            gpu_val = data.get('gpu', 0)
            gpu_status, gpu_col = self._get_status(gpu_val, 80, 90)
            self.gpu_card.update_data(f"{int(gpu_val)}%", gpu_val/100, gpu_col, gpu_status, "Load")
            
        except Exception:
            pass

    def _get_status(self, val, warn_thresh, crit_thresh):
        if val >= crit_thresh: return ("Critical", theme.colors.danger)
        if val >= warn_thresh: return ("Warning", theme.colors.warning)
        return ("Normal", theme.colors.success)

    def _check_ai_triggers(self, data, temp):
        """Analyze metrics and generate insights if state changes"""
        
        # --- CPU ---
        if data['cpu'] > 85:
            if not self.triggers_active['cpu_high']:
                self.after(0, lambda: self.add_insight(
                    f"High CPU usage ({data['cpu']}%). Background processing is intensive.", "warning"
                ))
                self.triggers_active['cpu_high'] = True
        elif data['cpu'] < 75: # Hysteresis
            if self.triggers_active['cpu_high']:
                self.after(0, lambda: self.add_insight("CPU load has returned to normal levels.", "success"))
                self.triggers_active['cpu_high'] = False

        # --- RAM ---
        if data['memory'] > 80:
            if not self.triggers_active['memory_crit']:
                self.after(0, lambda: self.add_insight(
                    f"RAM usage is critically high ({data['memory']}%). System may become unresponsive.", "critical"
                ))
                self.triggers_active['memory_crit'] = True
        elif data['memory'] < 70:
            if self.triggers_active['memory_crit']:
                self.after(0, lambda: self.add_insight("Memory pressure released. Stability restored.", "success"))
                self.triggers_active['memory_crit'] = False

        # --- TEMP ---
        if temp > 85:
            if not self.triggers_active['temp_high']:
                self.after(0, lambda: self.add_insight(
                    f"CPU temperature is high ({temp}°C). Thermal throttling may occur.", "warning"
                ))
                self.triggers_active['temp_high'] = True
        elif temp < 75:
            if self.triggers_active['temp_high']:
                self.after(0, lambda: self.add_insight("CPU temperature is stable.", "success"))
                self.triggers_active['temp_high'] = False

        # --- GPU SPIKE ---
        prev_gpu = self.previous_state.get('gpu', 0)
        curr_gpu = data.get('gpu', 0)
        if curr_gpu > 50 and (curr_gpu - prev_gpu > 30):
             self.after(0, lambda: self.add_insight(
                f"Sudden GPU spike detected ({int(curr_gpu)}%). Graphic workload engaged.", "info"
             ))

    def add_insight(self, message, type="info"):
        """Add a formatted insight card to the feed"""
        
        # Determine Color
        color = theme.colors.text_secondary
        icon = "ℹ️"
        border_color = theme.colors.border_light
        
        if type == "warning":
            color = theme.colors.warning
            icon = "⚠️"
            border_color = theme.colors.warning
        elif type == "critical":
            color = theme.colors.danger
            icon = "🔥"
            border_color = theme.colors.danger
        elif type == "success":
            color = theme.colors.success
            icon = "✅"
            border_color = theme.colors.success

        # Card Container
        card = CTkFrame(self.insights_log, fg_color=theme.colors.primary_bg, border_width=1, border_color=border_color, corner_radius=8)
        card.pack(fill="x", pady=4, padx=5)
        
        # Grid Layout
        card.grid_columnconfigure(1, weight=1)
        
        # Icon
        CTkLabel(card, text=icon, font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        # Content
        content_frame = CTkFrame(card, fg_color="transparent")
        content_frame.grid(row=0, column=1, sticky="nsew", pady=5, padx=(0, 10))
        
        # Timestamp
        time_str = datetime.now().strftime("%H:%M:%S")
        CTkLabel(
            content_frame, 
            text=time_str, 
            font=(theme.typography.font_primary, 10), 
            text_color=theme.colors.text_tertiary
        ).pack(anchor="w")
        
        # Message
        CTkLabel(
            content_frame, 
            text=message, 
            font=(theme.typography.font_primary, 12), 
            text_color=theme.colors.text_primary,
            wraplength=300,
            justify="left"
        ).pack(anchor="w")

        # Scroll to bottom
        self.insights_log._parent_canvas.yview_moveto(1.0)


class LiveMetricCard(CTkFrame):
    """Compact metric card with slim progress bar"""
    def __init__(self, parent, title, icon):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=8)
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        
        # Icon
        CTkLabel(self, text=icon, font=("Arial", 20)).grid(row=0, column=0, rowspan=2, padx=15, pady=10)
        
        # Title
        CTkLabel(
            self, text=title, 
            font=(theme.typography.font_primary, 12, "bold"), 
            text_color=theme.colors.text_secondary
        ).grid(row=0, column=1, sticky="w", pady=(10, 0))
        
        # Value Value
        self.value_lbl = CTkLabel(
            self, text="--%", 
            font=(theme.typography.font_primary, 16, "bold"), 
            text_color="white"
        )
        self.value_lbl.grid(row=1, column=1, sticky="w")
        
        # Extra Info (Temp/Space/etc)
        self.extra_lbl = CTkLabel(
            self, text="--", 
            font=(theme.typography.font_primary, 11), 
            text_color=theme.colors.text_tertiary
        )
        self.extra_lbl.grid(row=1, column=2, padx=15, sticky="e")

        # Progress Bar
        self.bar = CTkProgressBar(self, height=6, progress_color=theme.colors.success)
        self.bar.set(0)
        self.bar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=(5, 15))

    def update_data(self, value_text, ratio, color, status, extra):
        self.value_lbl.configure(text=value_text)
        self.extra_lbl.configure(text=f"{status} • {extra}")
        self.bar.configure(progress_color=color)
        self.bar.set(ratio)
