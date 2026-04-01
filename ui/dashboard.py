"""
Dashboard View - SysOptima
Design: Clean, Modern, Professional Light Theme
"""

import tkinter as tk
from tkinter import ttk
from core.performance_analyzer import PerformanceAnalyzer
from core.hardware_detector import HardwareDetector
import threading

class DashboardView(tk.Frame):
    """
    Overview Dashboard with System Health and Component Status Cards.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#F8F9FA", *args, **kwargs)
        
        self.detector = HardwareDetector()
        
        # Main Container with padding
        self.main_container = tk.Frame(self, bg="#F8F9FA", padx=40, pady=30)
        self.main_container.pack(fill="both", expand=True)

        self._setup_header()
        self._setup_cards()
        
        # Load data
        self.refresh_data()

    def _setup_header(self):
        header_frame = tk.Frame(self.main_container, bg="#F8F9FA")
        header_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(header_frame, text="System Dashboard", bg="#F8F9FA", fg="#0F172A", 
                 font=("Segoe UI", 24, "bold")).pack(anchor="w")
        
        tk.Label(header_frame, text="Quick overview of your system health", bg="#F8F9FA", fg="#64748B", 
                 font=("Segoe UI", 11)).pack(anchor="w")

    def _setup_cards(self):
        # Grid layout for cards
        self.cards_frame = tk.Frame(self.main_container, bg="#F8F9FA")
        self.cards_frame.pack(fill="x")
        self.cards_frame.columnconfigure(0, weight=1)
        self.cards_frame.columnconfigure(1, weight=1)
        
        # Placeholders for cards
        self.cpu_card = self._create_status_card(self.cards_frame, "CPU Status", 0, 0)
        self.mem_card = self._create_status_card(self.cards_frame, "Memory Status", 0, 1)
        self.disk_card = self._create_status_card(self.cards_frame, "Disk Status", 1, 0)
        self.gpu_card = self._create_status_card(self.cards_frame, "GPU Status", 1, 1)

    def _create_status_card(self, parent, title, row, col):
        # Card Frame
        card = tk.Frame(parent, bg="#FFFFFF", padx=20, pady=20, highlightbackground="#E2E8F0", highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Title
        tk.Label(card, text=title.upper(), bg="#FFFFFF", fg="#94A3B8", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        # Storage for updating widgets
        card.widgets = {}
        
        # Status Label (Large)
        lbl_status = tk.Label(card, text="--", bg="#FFFFFF", font=("Segoe UI", 16, "bold"), fg="#0F172A")
        lbl_status.pack(anchor="w", pady=(10, 5))
        card.widgets['status'] = lbl_status
        
        # Description
        lbl_desc = tk.Label(card, text="Waiting for data...", bg="#FFFFFF", fg="#64748B", font=("Segoe UI", 10), wraplength=300, justify="left")
        lbl_desc.pack(anchor="w")
        card.widgets['desc'] = lbl_desc
        
        # Accent Bar (Bottom)
        bar = tk.Frame(card, bg="#E2E8F0", height=4)
        bar.pack(side="bottom", fill="x", pady=(15, 0))
        card.widgets['bar'] = bar
        
        return card

    def refresh_data(self):
        """Fetch data and update UI (Async)"""
        threading.Thread(target=self._fetch_and_update, daemon=True).start()

    def _fetch_and_update(self):
        try:
            # Get Hardware Info
            hw = self.detector.detect_all()
            
            # Simple Logic for Dashboard (Overview)
            # CPU
            cpu_usage = hw['cpu']['usage_percent']
            cpu_status, cpu_color, cpu_msg = self._get_status(cpu_usage, 50, 80)
            
            # Memory
            ram_usage = hw['ram']['usage_percent']
            ram_status, ram_color, ram_msg = self._get_status(ram_usage, 60, 85)
            
            # Disk
            disk_usage = hw['disk']['usage_percent']
            disk_status, disk_color, disk_msg = self._get_status(disk_usage, 70, 90)
            
            # GPU
            gpu_data = hw.get('gpu', {})
            gpu_mem_used = gpu_data.get('memory_used_mb', 0)
            gpu_mem_total = gpu_data.get('memory_total_mb', 1) 
            # Avoid div by zero. If total is 0/1, assume low usage or 0
            if gpu_mem_total > 1:
                gpu_usage = (gpu_mem_used / gpu_mem_total) * 100
            else:
                gpu_usage = 0
            
            gpu_status, gpu_color, gpu_msg = self._get_status(gpu_usage, 50, 85)
            
            # Schedule UI Update
            self.after(0, lambda: self._update_ui(
                (cpu_status, cpu_color, f"Usage at {cpu_usage:.1f}%"),
                (ram_status, ram_color, f"Usage at {ram_usage:.1f}%"),
                (disk_status, disk_color, f"Usage at {disk_usage:.1f}%"),
                (gpu_status, gpu_color, f"VRAM Usage at {gpu_usage:.1f}%")
            ))
            
        except Exception as e:
            print(f"Dashboard update error: {e}")

    def _get_status(self, value, warn_thresh, crit_thresh):
        if value < warn_thresh:
            return "Good", "#10B981", "Optimal range"
        elif value < crit_thresh:
            return "Moderate", "#F59E0B", "Load is increasing"
        else:
            return "High Usage", "#EF4444", "Near capacity"

    def _update_ui(self, cpu, ram, disk, gpu):
        # Helper to update a single card
        def update_card(card, data):
            status, color, desc = data
            card.widgets['status'].config(text=status, fg=color)
            card.widgets['desc'].config(text=desc)
            card.widgets['bar'].config(bg=color)
            
        update_card(self.cpu_card, cpu)
        update_card(self.mem_card, ram)
        update_card(self.disk_card, disk)
        update_card(self.gpu_card, gpu)
