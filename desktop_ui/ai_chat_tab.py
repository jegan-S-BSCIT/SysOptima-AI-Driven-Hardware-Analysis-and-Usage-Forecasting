"""
AI Chat Tab - Conversational AI Assistant
Rule-based responses with optional Gemini API fallback
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from datetime import datetime
import psutil
from desktop_ui.styles import COLORS, FONTS, SPACING

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.gemini_ai_assistant import HybridAILogic
    HAS_GEMINI = True
except:
    HAS_GEMINI = False


class AIChatTab:
    """AI Assistant chat interface"""
    
    def __init__(self, parent):
        """Initialize AI chat tab"""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Initialize AI logic
        if HAS_GEMINI:
            self.ai = HybridAILogic()
        else:
            self.ai = None
        
        self.create_widgets()
        self.display_welcome_message()
    
    def create_widgets(self):
        """Create UI widgets"""
        
        # Main container
        main_frame = tk.Frame(self.frame, bg=COLORS["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING["lg"], pady=SPACING["md"])
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        header_frame.pack(fill=tk.X, pady=(0, SPACING["md"]))
        
        header_label = tk.Label(
            header_frame,
            text="AI Assistant - Ask about system performance",
            font=FONTS["h2"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_main"]
        )
        header_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="",
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_dim"]
        )
        self.status_label.pack(side=tk.RIGHT)
        self.update_ai_status()
        
        # Chat display area
        chat_frame = tk.LabelFrame(
            main_frame,
            text="Conversation",
            bg=COLORS["bg_card"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
            padx=SPACING["sm"],
            pady=SPACING["sm"]
        )
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, SPACING["md"]))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for chat history
        self.chat_display = tk.Text(
            chat_frame,
            height=15,
            width=80,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=FONTS["mono"],
            bg=COLORS["bg_input"],
            fg=COLORS["text_main"],
            relief=tk.FLAT
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure text tags for formatting
        self.chat_display.tag_configure("user", foreground=COLORS["accent"], font=("Consolas", 10, "bold"))
        self.chat_display.tag_configure("ai", foreground=COLORS["info"], font=("Consolas", 10))
        self.chat_display.tag_configure("system", foreground=COLORS["warning"], font=("Consolas", 9, "italic"))
        self.chat_display.tag_configure("timestamp", foreground=COLORS["text_muted"], font=("Consolas", 8))
        
        # Input area
        input_area = tk.Frame(main_frame, bg=COLORS["bg_main"])
        input_area.pack(fill=tk.X)

        input_frame = tk.LabelFrame(
            input_area,
            text="Type your question",
            bg=COLORS["bg_card"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
            padx=SPACING["sm"],
            pady=SPACING["sm"]
        )
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Input field
        self.input_field = tk.Text(
            input_frame,
            height=3,
            width=80,
            wrap=tk.WORD,
            font=FONTS["mono"],
            bg=COLORS["bg_input"],
            fg=COLORS["text_main"],
            relief=tk.FLAT
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, SPACING["sm"]))
        
        # Input scrollbar
        input_scrollbar = ttk.Scrollbar(input_frame, command=self.input_field.yview)
        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_field.config(yscrollcommand=input_scrollbar.set)
        
        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send\n(Ctrl+Enter)",
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT, fill=tk.Y, padx=(SPACING["sm"], 0))
        
        # Bind Enter key
        self.input_field.bind("<Control-Return>", lambda e: self.send_message())
        
        # Info section
        # Suggested questions panel
        suggestions = tk.LabelFrame(
            main_frame,
            text="Suggested Questions",
            bg=COLORS["bg_card"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
            padx=SPACING["sm"],
            pady=SPACING["sm"]
        )
        suggestions.pack(fill=tk.X, pady=(SPACING["md"], 0))

        self._add_suggestion(suggestions, "Why is my RAM usage high?")
        self._add_suggestion(suggestions, "Is my PC good for gaming?")
        self._add_suggestion(suggestions, "What should I upgrade?")

    def _add_suggestion(self, parent, text):
        btn = ttk.Button(parent, text=text, command=lambda t=text: self._use_suggestion(t))
        btn.pack(side=tk.LEFT, padx=SPACING["sm"], pady=SPACING["xs"])

    def _use_suggestion(self, text):
        self.input_field.delete("1.0", tk.END)
        self.input_field.insert(tk.END, text)
        self.input_field.focus_set()
    
    def update_ai_status(self):
        """Update AI connection status"""
        if not HAS_GEMINI:
            self.status_label.config(
                text="⚠ AI Module: Offline (using rule-based only)",
                foreground=COLORS["warning"]
            )
        else:
            try:
                status = self.ai.perplexity.check_api_connection()
                if status['connected']:
                    self.status_label.config(
                        text=f"✓ AI: Online (Perplexity - {status['model']})",
                        foreground=COLORS["success"]
                    )
                else:
                    self.status_label.config(
                        text="⚠ AI: Offline (using fallback diagnostics)",
                        foreground=COLORS["warning"]
                    )
            except:
                self.status_label.config(
                    text="⚠ AI: Checking...",
                    foreground=COLORS["warning"]
                )
    
    def display_welcome_message(self):
        """Display welcome message"""
        welcome = (
            "Welcome to the SysOptima AI Assistant.\n\n"
            "Ask about CPU, RAM, GPU, or disk performance.\n"
            "Try: \"Why is my RAM usage high?\" or \"What should I upgrade?\"\n\n"
            "Special commands: hello gemini, help, clear, status."
        )
        self.append_chat("SYSTEM", welcome, tag="system")
    
    def send_message(self):
        """Send message and get AI response"""
        
        # Get user input
        user_input = self.input_field.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Clear input
        self.input_field.delete("1.0", tk.END)
        
        # Handle special commands
        if user_input.lower() == "clear":
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.display_welcome_message()
            return
        
        if user_input.lower() == "help":
            help_text = """
Available Commands:
  • "hello gemini" - Test Gemini API connection
  • "help" - Show this help message
  • "clear" - Clear chat history
  • "status" - Show system metrics
  
Ask about:
  • CPU usage and performance
  • RAM memory usage
  • GPU and graphics
  • Disk space and speed
  • Overall system health
  • How to fix performance issues
  • What's causing slowdowns
"""
            self.append_chat("ASSISTANT", help_text, tag="ai")
            return
        
        if user_input.lower() == "status":
            status_text = self.get_system_status()
            self.append_chat("ASSISTANT", status_text, tag="ai")
            return
        
        # Display user message
        self.append_chat("You", user_input, tag="user")
        
        # Get AI response
        try:
            if self.ai:
                # Get system metrics for context
                metrics = self.get_current_metrics()
                response = self.ai.process_query(user_input, metrics)
            else:
                response = "Error: AI module not initialized. Using fallback response.\n\nPlease try again or check system configuration."
            
            # Display AI response
            self.append_chat("Assistant", response, tag="ai")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n\nPlease try again."
            self.append_chat("SYSTEM", error_msg, tag="system")
    
    def append_chat(self, sender, message, tag="ai"):
        """Append message to chat display"""
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add sender and message
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        
        self.chat_display.config(state=tk.DISABLED)
    
    def get_current_metrics(self):
        """Get current system metrics for AI context"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu,
                'memory_percent': ram.percent,
                'disk_percent': disk.percent,
                'gpu_available': True
            }
        except:
            return {}
    
    def get_system_status(self):
        """Get formatted system status"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"""
Current System Status:
  CPU: {cpu}% ({psutil.cpu_count(logical=False)} cores)
  RAM: {ram.percent}% ({round(ram.used/(1024**3), 1)}GB / {round(ram.total/(1024**3), 1)}GB)
  Disk: {disk.percent}% ({round(disk.used/(1024**3), 1)}GB / {round(disk.total/(1024**3), 1)}GB)
  Processes: {len(psutil.pids())}
"""
            return status
        except:
            return "Unable to retrieve system status."
    
    def cleanup(self):
        """Cleanup resources"""
        pass
