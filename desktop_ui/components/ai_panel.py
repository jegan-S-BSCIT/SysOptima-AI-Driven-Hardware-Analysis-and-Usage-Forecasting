"""
AI Assistant Panel - Reusable Component
Appears on Dashboard, Benchmarks, and Live pages.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys
import os
import psutil

from desktop_ui.styles import COLORS, FONTS, SPACING

# Add project root to path to import core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Use the unified Hybrid Logic
from core.gemini_ai_assistant import HybridAILogic

class AIPanel(tk.Frame):
    def __init__(self, parent):
        # Improved styling for visibility & contrast
        super().__init__(parent, bg=COLORS["bg_card"], width=320,
                 highlightthickness=1, highlightbackground=COLORS["border"]) 
        self.pack_propagate(False) # Strict width
        
        # Use Hybrid Logic (Rules + Gemini)
        self.ai_logic = HybridAILogic()
        
        # Header - distinctive styling
        self.create_header()
        
        # Chat History
        self.create_chat_area()
        
        # Quick Actions
        self.create_quick_actions()
        
        # Input Area
        self.create_input_area()
        
        # Auto-Greeting
        gemini_status = "Online (Gemini)" if self.ai_logic.gemini.connected else "Offline (Rules Only)"
        self.add_message("System", f"SysOptima Assistant initialized.\nAI Status: {gemini_status}")

    def create_header(self):
        # Darker header for contrast
        header = tk.Frame(self, bg=COLORS["bg_card_alt"], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        # Inner padding container
        inner = tk.Frame(header, bg=COLORS["bg_card_alt"])
        inner.pack(fill=tk.X, padx=SPACING["md"], pady=SPACING["md"])
        
        icon = tk.Label(inner, text="🤖", bg=COLORS["bg_card_alt"], fg=COLORS["text_main"], font=("Segoe UI", 16))
        icon.pack(side=tk.LEFT)
        
        title_frame = tk.Frame(inner, bg=COLORS["bg_card_alt"])
        title_frame.pack(side=tk.LEFT, padx=10)
        
        title = tk.Label(title_frame, text="SysOptima AI", bg=COLORS["bg_card_alt"], fg=COLORS["text_main"], font=("Segoe UI", 12, "bold"))
        title.pack(anchor="w")
        
        # Status
        status_text = "● Connected" if self.ai_logic.gemini.connected else "● Local Mode"
        status_color = COLORS["success"] if self.ai_logic.gemini.connected else COLORS["warning"]
        
        status = tk.Label(title_frame, text=status_text, bg=COLORS["bg_card_alt"], fg=status_color, font=FONTS["small"])
        status.pack(anchor="w")
        
        clear_btn = tk.Button(inner, text="Clear", bg=COLORS["bg_input"], fg=COLORS["text_main"],
                      font=FONTS["small"], relief=tk.FLAT, command=self.clear_chat, padx=8)
        clear_btn.pack(side=tk.RIGHT)

    def create_chat_area(self):
        self.chat_frame = tk.Frame(self, bg=COLORS["bg_card"])
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.chat_display = tk.Text(
            self.chat_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"],
            font=FONTS["body"], wrap=tk.WORD, relief=tk.FLAT,
            state=tk.DISABLED, spacing1=6, spacing3=6, padx=SPACING["md"], pady=SPACING["md"]
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Tags for styling
        self.chat_display.tag_config("user", foreground=COLORS["accent"], font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("ai", foreground=COLORS["info"], font=("Segoe UI", 10))
        self.chat_display.tag_config("system", foreground=COLORS["text_muted"], font=("Segoe UI", 9, "italic"))

    def create_quick_actions(self):
        actions_frame = tk.Frame(self, bg=COLORS["bg_card"])
        actions_frame.pack(fill=tk.X, padx=SPACING["md"], pady=SPACING["md"])
        
        buttons = ["Gaming Check", "Explain RAM", "Upgrade?"]
        for txt in buttons:
            btn = tk.Button(actions_frame, text=txt, bg=COLORS["bg_input"], fg=COLORS["text_main"],
                            font=FONTS["small"], relief=tk.FLAT, activebackground=COLORS["accent"],
                            command=lambda t=txt: self.handle_action(t))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def create_input_area(self):
        input_frame = tk.Frame(self, bg=COLORS["bg_card"], height=60)
        input_frame.pack(fill=tk.X, padx=SPACING["md"], pady=(0, SPACING["md"]))
        
        self.entry = tk.Entry(input_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"],
                      font=FONTS["body"], relief=tk.FLAT, insertbackground=COLORS["text_main"])
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), ipady=8)
        self.entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(input_frame, text="➤", bg=COLORS["accent"], fg=COLORS["text_main"],
                     font=("Segoe UI", 12), relief=tk.FLAT, command=self.send_message)
        send_btn.pack(side=tk.RIGHT, fill=tk.Y)

    def add_message(self, sender, text, tag="ai"):
        self.chat_display.config(state=tk.NORMAL)
        if sender:
            self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{text}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self):
        msg = self.entry.get().strip()
        if not msg: return
        self.entry.delete(0, tk.END)
        self.add_message("You", msg, "user")
        
        # Async-like update to avoid freezing UI if API lags
        self.after(10, lambda: self._fetch_response(msg))

    def _fetch_response(self, msg):
        try:
            # 1. Fetch Real-Time Context
            metrics = self.get_current_metrics()
            
            # 2. Call Hybrid Engine (Gemini + Rules)
            response = self.ai_logic.process_query(msg, metrics)
            self.add_message("SysOptima AI", response, "ai")
        except Exception as e:
            self.add_message("System", f"Error: {str(e)}", "system")

    def get_current_metrics(self):
        """Fetch live metrics for AI context"""
        try:
            cpu = psutil.cpu_percent(interval=None) # Instant check
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            gpu_avail = False
            try:
                import GPUtil
                if GPUtil.getGPUs(): gpu_avail = True
            except: pass

            return {
                'cpu_percent': cpu,
                'memory_percent': ram.percent,
                'disk_percent': disk.percent,
                'gpu_available': gpu_avail
            }
        except: return {}

    def handle_action(self, action):
        self.add_message("You", action, "user")
        
        query_map = {
            "Gaming Check": "Can I play games? Check my specs.",
            "Explain RAM": "Why is my RAM usage high?",
            "Upgrade?": "What should I upgrade in my PC?"
        }
        
        query = query_map.get(action, action)
        
        self.after(10, lambda: self._fetch_response(query))

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("System", "Chat history cleared.")
