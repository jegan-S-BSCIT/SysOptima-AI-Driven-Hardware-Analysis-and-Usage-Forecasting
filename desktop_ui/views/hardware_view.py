"""
Hardware View - Detailed System Specifications & Real-time Status
replaces the simple Diagnostics Tab
"""
import tkinter as tk
import psutil
import platform
import math
from desktop_ui.styles import COLORS, FONTS

try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

class HardwareView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # Scrollable Container (in case of many disks/GPUs)
        self.canvas = tk.Canvas(self, bg=COLORS["bg_main"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=COLORS["bg_main"])
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")
        
        # Header
        tk.Label(self.scroll_frame, text="Hardware Specification & Status", font=FONTS["h1"], 
                 bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(10, 20), padx=10)
        
        # Dynamic Widgets Store
        self.widgets = {}
        
        # Build Sections
        self.create_cpu_section()
        self.create_memory_section()
        self.create_gpu_section()
        self.create_disk_section()
        
        # Start Live Update
        self.update_loop()

    def create_section_header(self, text, icon=""):
        f = tk.Frame(self.scroll_frame, bg=COLORS["bg_main"])
        f.pack(fill="x", padx=10, pady=(20, 10))
        tk.Label(f, text=icon, font=("Segoe UI", 12), bg=COLORS["bg_main"], fg=COLORS["text_accent"]).pack(side="left", padx=(0,10))
        tk.Label(f, text=text, font=FONTS["h2"], bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(side="left")

    def create_card(self, parent):
        card = tk.Frame(parent, bg=COLORS["bg_card"], padx=15, pady=15)
        card.pack(fill="x", padx=10, pady=5)
        return card

    def add_row(self, parent, label, value_key, static_value=None):
        row = tk.Frame(parent, bg=COLORS["bg_card"])
        row.pack(fill="x", pady=2)
        
        tk.Label(row, text=label, font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["text_dim"], width=20, anchor="w").pack(side="left")
        
        if static_value:
            tk.Label(row, text=static_value, font=("Segoe UI", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(side="left")
        else:
            val_lbl = tk.Label(row, text="--", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_main"])
            val_lbl.pack(side="left")
            self.widgets[value_key] = val_lbl

    def create_cpu_section(self):
        self.create_section_header("Processor (CPU)", "⚡")
        card = self.create_card(self.scroll_frame)
        
        # Static Info
        cpu_name = platform.processor()
        phys_cores = psutil.cpu_count(logical=False)
        log_cores = psutil.cpu_count(logical=True)
        
        self.add_row(card, "Model Name:", None, static_value=cpu_name)
        self.add_row(card, "Physical Cores:", None, static_value=str(phys_cores))
        self.add_row(card, "Logical Cores:", None, static_value=str(log_cores))
        
        # Dynamic Info
        self.add_row(card, "Current Frequency:", "cpu_freq")
        self.add_row(card, "Current Utilization:", "cpu_usage")
        
        # Status
        self.widgets["cpu_status"] = tk.Label(card, text="Status: Analyzing...", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_dim"])
        self.widgets["cpu_status"].pack(anchor="w", pady=(10, 0))

    def create_memory_section(self):
        self.create_section_header("Memory (RAM)", "🧠")
        card = self.create_card(self.scroll_frame)
        
        ram = psutil.virtual_memory()
        total_gb = f"{ram.total / (1024**3):.2f} GB"
        
        self.add_row(card, "Total Capacity:", None, static_value=total_gb)
        self.add_row(card, "Used Memory:", "ram_used")
        self.add_row(card, "Available:", "ram_free")
        self.add_row(card, "Usage Percentage:", "ram_percent")

    def create_gpu_section(self):
        if not HAS_GPU: return
        try:
            gpus = GPUtil.getGPUs()
            if not gpus: return
            
            self.create_section_header("Graphics (GPU)", "🎮")
            for i, gpu in enumerate(gpus):
                card = self.create_card(self.scroll_frame)
                self.add_row(card, f"GPU {i} Name:", None, static_value=gpu.name)
                self.add_row(card, "Total VRAM:", None, static_value=f"{gpu.memoryTotal} MB")
                self.add_row(card, "GPU Temperature:", f"gpu_{i}_temp")
                self.add_row(card, "GPU Load:", f"gpu_{i}_load")
                self.add_row(card, "Memory Used:", f"gpu_{i}_mem")
        except: pass

    def create_disk_section(self):
        self.create_section_header("Storage (Disk)", "💽")
        
        for part in psutil.disk_partitions():
            if 'cdrom' in part.opts or part.fstype == '': continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
                card = self.create_card(self.scroll_frame)
                
                # Header for drive
                drive_header = tk.Frame(card, bg=COLORS["bg_card"])
                drive_header.pack(fill="x", pady=(0, 5))
                tk.Label(drive_header, text=f"Drive: {part.device} ({part.mountpoint})", 
                         font=("Segoe UI", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_accent"]).pack(side="left")
                tk.Label(drive_header, text=f"Type: {part.fstype}", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(side="right")
                
                total_gb = f"{usage.total / (1024**3):.2f} GB"
                self.add_row(card, "Total Size:", None, static_value=total_gb)
                
                # We need unique keys for updates if we want dynamic, but disks change slowly. 
                # For this assignment, we'll keep it static or simple refresh. 
                # Let's add dynamic references
                key_prefix = f"disk_{part.device}"
                self.add_row(card, "Used Space:", f"{key_prefix}_used")
                self.add_row(card, "Free Space:", f"{key_prefix}_free")
                self.add_row(card, "Usage:", f"{key_prefix}_percent")
                
            except: pass

    def update_loop(self):
        if not self.winfo_exists(): return
        
        try:
            # CPU
            cpu_freq = psutil.cpu_freq()
            freq_txt = f"{cpu_freq.current:.1f} MHz" if cpu_freq else "N/A"
            self.widgets["cpu_freq"].config(text=freq_txt)
            
            cpu_pct = psutil.cpu_percent()
            self.widgets["cpu_usage"].config(text=f"{cpu_pct}%")
            
            # CPU Status color
            status_lbl = self.widgets["cpu_status"]
            if cpu_pct < 50:
                status_lbl.config(text="✔ Normal Load", fg=COLORS["success"])
            elif cpu_pct < 80:
                status_lbl.config(text="⚠ Heavy Load", fg=COLORS["warning"])
            else:
                status_lbl.config(text="❌ Critical Load", fg=COLORS["danger"])
            
            # RAM
            ram = psutil.virtual_memory()
            self.widgets["ram_used"].config(text=f"{ram.used / (1024**3):.2f} GB")
            self.widgets["ram_free"].config(text=f"{ram.available / (1024**3):.2f} GB")
            self.widgets["ram_percent"].config(text=f"{ram.percent}%")
            
            # GPU
            if HAS_GPU:
                gpus = GPUtil.getGPUs()
                for i, gpu in enumerate(gpus):
                    try:
                        self.widgets[f"gpu_{i}_load"].config(text=f"{gpu.load*100:.1f}%")
                        self.widgets[f"gpu_{i}_temp"].config(text=f"{gpu.temperature} °C")
                        self.widgets[f"gpu_{i}_mem"].config(text=f"{gpu.memoryUsed} MB / {gpu.memoryTotal} MB")
                    except: pass
            
            # Disk (Refreshing some metrics)
            for part in psutil.disk_partitions():
                if 'cdrom' in part.opts or part.fstype == '': continue
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    prefix = f"disk_{part.device}"
                    if f"{prefix}_used" in self.widgets:
                        self.widgets[f"{prefix}_used"].config(text=f"{usage.used / (1024**3):.2f} GB")
                        self.widgets[f"{prefix}_free"].config(text=f"{usage.free / (1024**3):.2f} GB")
                        self.widgets[f"{prefix}_percent"].config(text=f"{usage.percent}%")
                except: pass
                
        except Exception as e:
            print(f"Hardware Update Error: {e}")
            
        self.after(1000, self.update_loop)

    def cleanup(self): pass
