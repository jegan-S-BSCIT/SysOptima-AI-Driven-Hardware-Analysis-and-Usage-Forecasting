"""
Dashboard View
Layout: Animated System Health Bars
"""
import tkinter as tk
import psutil
from desktop_ui.styles import COLORS, FONTS

class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # NOTE: AIPanel is now handled globally by MainWindow
        
        # Content Area - Takes Full Remaining Space or Left Side
        self.content_area = tk.Frame(self, bg=COLORS["bg_main"])
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Header
        tk.Label(self.content_area, text="System Health Overview", font=("Segoe UI", 20, "bold"), 
                 bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 40))
        
        # Health Bars Container
        self.bar_data = {}
        items = ["CPU Health", "Memory Health", "Disk Health", "System Overall"]
        
        for item in items:
            self.create_health_bar(item)
            
        self.target_values = {k: 0 for k in items}
        self.current_values = {k: 0.0 for k in items}
        
        self.measure_loop()
        self.animation_loop()

    def create_health_bar(self, title):
        frame = tk.Frame(self.content_area, bg=COLORS["bg_main"])
        frame.pack(fill=tk.X, pady=15)
        
        # Labels
        header = tk.Frame(frame, bg=COLORS["bg_main"])
        header.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header, text=title, font=FONTS["h2"], bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(side=tk.LEFT)
        pct_lbl = tk.Label(header, text="0%", font=FONTS["h2"], bg=COLORS["bg_main"], fg=COLORS["text_accent"])
        pct_lbl.pack(side=tk.RIGHT)
        
        # Bar Canvas
        canvas = tk.Canvas(frame, height=12, bg="#334155", highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        # Initial draw
        canvas.create_rectangle(0, 0, 0, 12, fill=COLORS["success"], outline="", tags="bar")
        
        self.bar_data[title] = {"canvas": canvas, "label": pct_lbl}

    def measure_loop(self):
        """Fetch actual data periodically"""
        if not self.winfo_exists(): return
        
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            # Health Score (Inverse of usage roughly)
            self.target_values["CPU Health"] = 100 - cpu
            self.target_values["Memory Health"] = 100 - ram
            self.target_values["Disk Health"] = 100 - disk
            self.target_values["System Overall"] = (300 - cpu - ram - disk) / 3
            
        except: pass
        self.after(2000, self.measure_loop)

    def animation_loop(self):
        """Smoothly interpolate current value to target"""
        if not self.winfo_exists(): return
        
        needs_redraw = False
        
        for key, target in self.target_values.items():
            current = self.current_values[key]
            
            diff = target - current
            if abs(diff) > 0.5:
                # Move towards target
                step = diff * 0.1 # Lerp factor
                new_val = current + step
                self.current_values[key] = new_val
                self.draw_bar(key, new_val)
                needs_redraw = True
            else:
                if current != target:
                    self.current_values[key] = target
                    self.draw_bar(key, target)
        
        self.after(30, self.animation_loop)

    def draw_bar(self, key, val):
        widgets = self.bar_data[key]
        canvas = widgets["canvas"]
        lbl = widgets["label"]
        
        # Update text
        lbl.config(text=f"{val:.1f}%")
        
        # Update Bar
        width = canvas.winfo_width()
        if width < 10: return # Not rendered yet
        
        fill_width = (val / 100) * width
        
        # Color Logic
        color = COLORS["success"]
        if val < 50: color = COLORS["danger"]
        elif val < 80: color = COLORS["warning"]
            
        # Update canvas
        canvas.coords("bar", 0, 0, fill_width, 12)
        canvas.itemconfig("bar", fill=color)

    def cleanup(self): pass
