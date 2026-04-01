"""
Chatbot View Module
UI for the AI System Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

class ChatbotView(ttk.Frame):
    """Chat interface for the System Expert"""
    
    def __init__(self, parent, on_query=None):
        super().__init__(parent)
        self.on_query = on_query # Handler function to call
        self._build()
        
    def _build(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=20, pady=20)
        
        title = ttk.Label(header, text="AI System Assistant", font=("Segoe UI", 18, "bold"))
        title.pack(side=tk.LEFT)
        
        subtitle = ttk.Label(header, text="Ask questions about your system performance", font=("Segoe UI", 10))
        subtitle.pack(side=tk.LEFT, padx=10, pady=(8,0))
        
        # Chat History Area
        self.history = scrolledtext.ScrolledText(
            self, 
            state='disabled', 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            bg="#f4f4f4", 
            padx=10, 
            pady=10
        )
        self.history.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Tag configuration for colors
        self.history.tag_config("user", foreground="#0000aa", font=("Segoe UI", 10, "bold"))
        self.history.tag_config("ai", foreground="#006600")
        self.history.tag_config("sys", foreground="#666666", font=("Segoe UI", 9, "italic"))
        
        # Input Area
        input_frame = ttk.Frame(self, padding=20)
        input_frame.pack(fill=tk.X)
        
        self.msg_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", self._on_send)
        
        send_btn = ttk.Button(input_frame, text="Ask AI", command=self._on_send)
        send_btn.pack(side=tk.RIGHT)
        
        # Quick Chips Suggestions
        chips_frame = ttk.Frame(self)
        chips_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        suggestions = ["Is my system healthy?", "Can I run modern games?", "Why is my RAM usage high?"]
        for sug in suggestions:
            btn = ttk.Button(chips_frame, text=sug, command=lambda s=sug: self._insert_and_send(s))
            btn.pack(side=tk.LEFT, padx=5)

        # Initial greeting
        self._add_message("System", "Ready. I can analyze your Hardware and Live Monitoring data.")

    def _insert_and_send(self, text):
        self.msg_entry.delete(0, tk.END)
        self.msg_entry.insert(0, text)
        self._on_send()

    def _on_send(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        # Clear input
        self.msg_entry.delete(0, tk.END)
        
        # Show user message
        self._add_message("You", msg)
        
        # Get AI response
        if self.on_query:
            response = self.on_query(msg)
            self._add_message("SysOptima AI", response)
            
    def _add_message(self, sender, text):
        self.history.config(state='normal')
        
        tag = "user" if sender == "You" else "ai"
        if sender == "System": tag = "sys"
        
        self.history.insert(tk.END, f"{sender}:\n", tag)
        self.history.insert(tk.END, f"{text}\n\n")
        
        self.history.see(tk.END)
        self.history.config(state='disabled')
