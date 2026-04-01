"""
Live Monitor View
Layout: Left Hardware Progress | Right Live Insights (System Log Style)
"""
import tkinter as tk
from desktop_ui.styles import COLORS, FONTS
import psutil

class LiveView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # Split Layout
        self.left_panel = tk.Frame(self, bg=COLORS["bg_main"])
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.right_panel = tk.Frame(self, bg=COLORS["bg_card"], width=300)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False)

        self.create_hardware_bars()
        self.create_live_insights()
        
        self.running = True
        self.update_loop()

    def create_hardware_bars(self):
        tk.Label(self.left_panel, text="Real-Time Hardware Monitor", font=FONTS["h2"], bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 20))
        
        self.bars = {}
        for comp in ["CPU Usage", "RAM Usage", "Disk Activity", "GPU Load"]:
            frame = tk.Frame(self.left_panel, bg=COLORS["bg_card"], padx=15, pady=15)
            frame.pack(fill=tk.X, pady=5)
            
            # Header
            header = tk.Frame(frame, bg=COLORS["bg_card"])
            header.pack(fill=tk.X)
            tk.Label(header, text=comp, bg=COLORS["bg_card"], fg="white", font=FONTS["body"]).pack(side=tk.LEFT)
            val_lbl = tk.Label(header, text="0%", bg=COLORS["bg_card"], fg=COLORS["text_accent"], font=("Segoe UI", 10, "bold"))
            val_lbl.pack(side=tk.RIGHT)
            
            # Bar
            canvas = tk.Canvas(frame, height=10, bg=COLORS["bg_input"], highlightthickness=0)
            canvas.pack(fill=tk.X, pady=(10, 0))
            
            self.bars[comp] = {"val": val_lbl, "canvas": canvas}

    def create_live_insights(self):
        header = tk.Frame(self.right_panel, bg=COLORS["bg_card"], height=50)
        header.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(header, text="Live Insights", bg=COLORS["bg_card"], fg="white", font=FONTS["h2"]).pack(anchor="w")
        
        self.log_display = tk.Text(self.right_panel, bg=COLORS["bg_main"], fg=COLORS["text_dim"], 
                                   font=("Consolas", 9), relief=tk.FLAT, state=tk.DISABLED, padx=10, pady=10)
        self.log_display.pack(fill=tk.BOTH, expand=True)
        
        self.log_message("System Monitor Started...")

    def update_loop(self):
        if not self.winfo_exists(): return
        
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            self.update_bar("CPU Usage", cpu)
            self.update_bar("RAM Usage", ram)
            self.update_bar("Disk Activity", disk)
            self.update_bar("GPU Load", 0)
            
            # Simulated insights
            if ram > 85: self.log_message(f"WARN: High Memory Usage ({ram}%)")
            if cpu > 90: self.log_message(f"CRITICAL: CPU Load ({cpu}%)")
            
        except: pass
        
        self.after(1000, self.update_loop)

    def update_bar(self, key, val):
        widgets = self.bars[key]
        widgets["val"].config(text=f"{val}%")
        
        canvas = widgets["canvas"]
        canvas.delete("all")
        width = canvas.winfo_width()
        fill = (val / 100) * width
        
        color = COLORS["info"]
        if val > 80: color = COLORS["warning"]
        if val > 90: color = COLORS["danger"]
        
        canvas.create_rectangle(0, 0, fill, 10, fill=color, outline="")

    def log_message(self, msg):
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert(tk.END, f"> {msg}\n")
        self.log_display.see(tk.END)
        self.log_display.config(state=tk.DISABLED)

    def cleanup(self): 
        self.running = False
