"""
Performance View
Layout: Grid of Live Usage Cards (CPU, RAM, Disk, GPU)
"""
import tkinter as tk
import psutil
from desktop_ui.styles import COLORS, FONTS

class PerformanceView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # NOTE: AIPanel is now handled globally by MainWindow
        
        # Content Area Only
        self.content_area = tk.Frame(self, bg=COLORS["bg_main"])
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        tk.Label(self.content_area, text="Performance Metrics", font=FONTS["h2"], 
                 bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 20))
        
        # Cards Container
        cards_frame = tk.Frame(self.content_area, bg=COLORS["bg_main"])
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cards = {}
        metrics = ["CPU", "Memory", "Disk", "GPU"]
        
        # Grid 2x2
        for i, metric in enumerate(metrics):
            row = i // 2
            col = i % 2
            frame = self.create_card(cards_frame, metric)
            frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            cards_frame.grid_columnconfigure(col, weight=1)
            cards_frame.grid_rowconfigure(row, weight=1)

        self.update_loop()

    def create_card(self, parent, title):
        card = tk.Frame(parent, bg=COLORS["bg_card"], highlightthickness=1, highlightbackground=COLORS["bg_input"])
        
        # Icon & Title
        header = tk.Frame(card, bg=COLORS["bg_card"])
        header.pack(fill=tk.X, padx=15, pady=15)
        
        icons = {"CPU": "⚡", "Memory": "🧠", "Disk": "💽", "GPU": "🎮"}
        tk.Label(header, text=icons.get(title, ""), font=("Segoe UI", 14), 
                 bg=COLORS["bg_card"], fg=COLORS["text_accent"]).pack(side=tk.LEFT)
        tk.Label(header, text=f"{title} Usage", font=FONTS["h2"], 
                 bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(side=tk.LEFT, padx=10)
        
        # Value
        val_lbl = tk.Label(card, text="0%", font=("Segoe UI", 36, "bold"), 
                           bg=COLORS["bg_card"], fg="white")
        val_lbl.pack(expand=True)
        
        # Status
        status_lbl = tk.Label(card, text="Status: --", font=FONTS["small"], 
                              bg=COLORS["bg_card"], fg=COLORS["text_dim"])
        status_lbl.pack(anchor="w", padx=15, pady=(0, 15))
        
        self.cards[title] = {"val": val_lbl, "status": status_lbl}
        return card

    def update_loop(self):
        if not self.winfo_exists(): return
        
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            gpu = 0 # Placeholder
            
            self.update_card("CPU", cpu)
            self.update_card("Memory", ram)
            self.update_card("Disk", disk)
            self.update_card("GPU", gpu)
        except: pass
        
        self.after(2000, self.update_loop)

    def update_card(self, key, val):
        widgets = self.cards[key]
        widgets["val"].config(text=f"{val:.1f}%")
        
        if val < 50:
            status, color = "Stable", COLORS["success"]
        elif val < 80:
            status, color = "Moderate", COLORS["warning"]
        else:
            status, color = "Critical", COLORS["danger"]
            
        widgets["status"].config(text=f"Status: {status}", fg=color)
    
    def cleanup(self): pass
