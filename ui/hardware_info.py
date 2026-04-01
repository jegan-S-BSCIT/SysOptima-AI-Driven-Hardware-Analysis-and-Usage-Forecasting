"""
Hardware Info View - SysOptima
Design: Structured, Clean Cards (Not Text Dump)
"""

import tkinter as tk
from tkinter import ttk
import threading

class HardwareInfoView(tk.Frame):
    """Displays detected hardware details in structured sections"""
    def __init__(self, parent, on_detect=None, *args, **kwargs):
        super().__init__(parent, bg="#F8F9FA", *args, **kwargs)
        self.on_detect = on_detect
        
        # Main Container
        self.container = tk.Frame(self, bg="#F8F9FA", padx=40, pady=30)
        self.container.pack(fill="both", expand=True)

        self._setup_header()
        
        # Grid for hardware sections
        self.grid_frame = tk.Frame(self.container, bg="#F8F9FA")
        self.grid_frame.pack(fill="both", expand=True)
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)

        # Placeholders
        self.cpu_section = self._create_section(self.grid_frame, "Processor (CPU)", 0, 0)
        self.mem_section = self._create_section(self.grid_frame, "Memory (RAM)", 0, 1)
        self.disk_section = self._create_section(self.grid_frame, "Storage (Disk)", 1, 0)
        self.gpu_section = self._create_section(self.grid_frame, "Graphics (GPU)", 1, 1)

    def _setup_header(self):
        header = tk.Frame(self.container, bg="#F8F9FA")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="Hardware Information", bg="#F8F9FA", fg="#0F172A", 
                 font=("Segoe UI", 24, "bold")).pack(side="left")
        
        btn = tk.Button(header, text="Detect Hardware", command=self._handle_detect,
                        bg="#2563EB", fg="white", font=("Segoe UI", 10, "bold"),
                        relief="flat", padx=15, pady=5, borderwidth=0)
        btn.pack(side="right")

    def _create_section(self, parent, title, row, col):
        card = tk.Frame(parent, bg="#FFFFFF", padx=20, pady=20, highlightbackground="#E2E8F0", highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        tk.Label(card, text=title.upper(), bg="#FFFFFF", fg="#94A3B8", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Data container
        data_frame = tk.Frame(card, bg="#FFFFFF")
        data_frame.pack(fill="both", expand=True)
        
        card.data_frame = data_frame
        return card

    def _add_row(self, parent, label, value):
        row = tk.Frame(parent, bg="#FFFFFF")
        row.pack(fill="x", pady=4)
        
        tk.Label(row, text=label, bg="#FFFFFF", fg="#64748B", font=("Segoe UI", 10)).pack(side="left")
        tk.Label(row, text=str(value), bg="#FFFFFF", fg="#0F172A", font=("Segoe UI", 10, "bold")).pack(side="right")

    def _handle_detect(self):
        if self.on_detect:
            # Show loading state?
            threading.Thread(target=self._run_detect, daemon=True).start()

    def _run_detect(self):
        # We assume on_detect is thread-safe or returns data we render on main thread
        # Actually MainWindow.detect_hardware is purely internal. 
        # The MainWindow usually calls render_info. 
        # But here we have a button. 
        # Let's assume on_detect returns the data directly or we trigger an update.
        # Given previous logic, MainWindow passed `self.detect_hardware` which UPDATES `HardwareInfoView`?
        # No, previous code was `self.on_detect()` returns data.
        if self.on_detect:
            data = self.on_detect() 
            self.after(0, lambda: self.render_info(data))

    def render_info(self, info: dict):
        """Render data into cards"""
        if not info: return

        # Clear old rows
        for section in [self.cpu_section, self.mem_section, self.disk_section, self.gpu_section]:
            for widget in section.data_frame.winfo_children():
                widget.destroy()

        # CPU
        cpu = info.get('cpu', {})
        p = self.cpu_section.data_frame
        self._add_row(p, "Processor Name", cpu.get('name', 'Unknown'))
        self._add_row(p, "Physical Cores", cpu.get('physical_cores', '-'))
        self._add_row(p, "Logical Threads", cpu.get('logical_threads', '-'))
        self._add_row(p, "Current Usage", f"{cpu.get('usage_percent', 0)}%")

        # Memory
        ram = info.get('ram', {})
        p = self.mem_section.data_frame
        self._add_row(p, "Total RAM", f"{ram.get('total_gb', 0)} GB")
        self._add_row(p, "Used RAM", f"{ram.get('used_gb', 0)} GB")
        self._add_row(p, "Available", f"{ram.get('available_gb', 0)} GB") # if available key exists
        self._add_row(p, "Usage", f"{ram.get('usage_percent', 0)}%")
        # Note: Original hardware_detector might use diff keys. 
        # Checking hardware_detector.py... 
        # detect_ram returns: total_gb, used_gb, usage_percent. 
        # get_memory_info (hardware_info.py) returns: available_gb too. 
        # We'll use get() safe access.

        # Disk
        disk = info.get('disk', {})
        p = self.disk_section.data_frame
        self._add_row(p, "Primary Drive", disk.get('mountpoint', 'C:\\'))
        self._add_row(p, "Total Space", f"{disk.get('total_gb', 0)} GB")
        self._add_row(p, "Used Space", f"{disk.get('used_gb', 0)} GB")
        self._add_row(p, "Free Space", f"{disk.get('total_gb', 0) - disk.get('used_gb', 0):.2f} GB")

        # GPU
        gpu = info.get('gpu', {})
        p = self.gpu_section.data_frame
        self._add_row(p, "GPU Name", gpu.get('name', 'Unknown'))
        self._add_row(p, "VRAM Total", f"{gpu.get('memory_total_mb', 0):.0f} MB")
        self._add_row(p, "VRAM Used", f"{gpu.get('memory_used_mb', 0):.0f} MB")
        self._add_row(p, "Status", gpu.get('status', 'Unknown'))
