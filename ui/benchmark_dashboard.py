"""
Modern Dashboard UI for Benchmark System
B.Sc. IT Final Year Project - Intelligent Computer Performance Analysis
Clean, lightweight, lag-free interface with benchmark comparison
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import time
from core.lightweight_benchmarks import LightweightBenchmark
from typing import Dict


class ModernDashboard:
    """Modern benchmark dashboard UI"""
    
    def __init__(self, root):
        """Initialize modern dashboard"""
        self.root = root
        self.root.title("System Performance Benchmark - B.Sc. IT Project")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.setup_styles()
        
        # Initialize benchmark engine
        self.benchmark = LightweightBenchmark()
        self.results = None
        self.is_benchmarking = False
        
        # Build UI
        self.create_ui()
    
    def setup_styles(self):
        """Configure color scheme and styles"""
        self.colors = {
            'bg_main': '#f0f0f0',
            'bg_card': '#ffffff',
            'text_primary': '#1a1a1a',
            'text_secondary': '#666666',
            'accent_blue': '#2196F3',
            'accent_green': '#4CAF50',
            'accent_orange': '#FF9800',
            'accent_red': '#F44336',
            'border_light': '#e0e0e0'
        }
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('TButton', font=('Segoe UI', 10), padding=10)
        style.map('TButton',
                 background=[('active', self.colors['accent_blue'])])
    
    def create_ui(self):
        """Create main UI layout"""
        # Header
        self.create_header()
        
        # Main content area
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Benchmark controls
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Benchmark button
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.btn_benchmark = tk.Button(
            btn_frame,
            text="Run Benchmarks",
            command=self.start_benchmarks,
            bg=self.colors['accent_green'],
            fg="white",
            font=('Segoe UI', 12, 'bold'),
            cursor="hand2",
            padx=20,
            pady=15,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.btn_benchmark.pack(fill=tk.X)
        
        # Status label
        self.label_status = ttk.Label(
            left_panel,
            text="Ready",
            foreground=self.colors['accent_green']
        )
        self.label_status.pack(pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            left_panel,
            mode='indeterminate',
            length=250
        )
        self.progress.pack(fill=tk.X, pady=10)
        
        # Right panel - Results display
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Component cards in grid
        self.component_frames = {}
        cards_container = ttk.Frame(right_panel)
        cards_container.pack(fill=tk.BOTH, expand=True)
        
        # Create 2x2 grid of component cards
        components = [
            ('cpu', 'CPU Performance', 0, 0),
            ('ram', 'RAM Performance', 0, 1),
            ('storage', 'Storage Performance', 1, 0),
            ('gpu', 'GPU Performance', 1, 1)
        ]
        
        for component_id, title, row, col in components:
            frame = self.create_component_card(cards_container, title, component_id)
            frame.grid(row=row, column=col, sticky='nsew', padx=(0, 10), pady=(0, 10))
            self.component_frames[component_id] = frame
        
        # Configure grid weights
        cards_container.rowconfigure(0, weight=1)
        cards_container.rowconfigure(1, weight=1)
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)
        
        # Bottom section - Overall health and recommendations
        bottom_section = ttk.Frame(right_panel)
        bottom_section.pack(fill=tk.X, pady=(20, 0))
        
        self.create_health_section(bottom_section)
    
    def create_header(self):
        """Create header section"""
        header = tk.Frame(self.root, bg=self.colors['accent_blue'])
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header,
            text="System Performance Benchmark Analysis",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['accent_blue'],
            fg='white',
            pady=15
        )
        title_label.pack()
        
        subtitle = tk.Label(
            header,
            text="B.Sc. IT Final Year Project - Compare Your Hardware Against Reference Systems",
            font=('Segoe UI', 10),
            bg=self.colors['accent_blue'],
            fg='rgba(255,255,255,0.8)',
            pady=(0, 10)
        )
        subtitle.pack()
    
    def create_component_card(self, parent, title: str, component_id: str) -> tk.Frame:
        """Create a component benchmark card"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT)
        card.configure(highlightthickness=1, highlightbackground=self.colors['border_light'])
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Scores frame
        scores_frame = tk.Frame(card, bg=self.colors['bg_card'])
        scores_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Local score
        tk.Label(scores_frame, text="Your Score:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.score_labels = getattr(self, 'score_labels', {})
        self.score_labels[component_id] = tk.Label(
            scores_frame,
            text="--/100",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_blue']
        )
        self.score_labels[component_id].pack(side=tk.LEFT, padx=(5, 20))
        
        # Reference score
        tk.Label(scores_frame, text="Reference:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.ref_labels = getattr(self, 'ref_labels', {})
        self.ref_labels[component_id] = tk.Label(
            scores_frame,
            text="--/100",
            font=('Segoe UI', 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.ref_labels[component_id].pack(side=tk.LEFT, padx=5)
        
        # Difference frame
        diff_frame = tk.Frame(card, bg=self.colors['bg_card'])
        diff_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(diff_frame, text="Difference:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.diff_labels = getattr(self, 'diff_labels', {})
        self.diff_labels[component_id] = tk.Label(
            diff_frame,
            text="--%",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.diff_labels[component_id].pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_labels = getattr(self, 'status_labels', {})
        self.status_labels[component_id] = tk.Label(
            card,
            text="Waiting for benchmark...",
            font=('Segoe UI', 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            wraplength=250
        )
        self.status_labels[component_id].pack(anchor=tk.W, padx=15, pady=(10, 15))
        
        return card
    
    def create_health_section(self, parent):
        """Create overall health section"""
        health_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT)
        health_frame.configure(highlightthickness=1, highlightbackground=self.colors['border_light'])
        health_frame.pack(fill=tk.X)
        
        # Title
        tk.Label(
            health_frame,
            text="Overall System Health",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Health score and classification
        info_frame = tk.Frame(health_frame, bg=self.colors['bg_card'])
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(info_frame, text="Score:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.health_score_label = tk.Label(
            info_frame,
            text="--/100",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_blue']
        )
        self.health_score_label.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(info_frame, text="Classification:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.classification_label = tk.Label(
            info_frame,
            text="--",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_green']
        )
        self.classification_label.pack(side=tk.LEFT, padx=5)
        
        # Bottleneck
        tk.Label(
            health_frame,
            text="Bottleneck Identified:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.bottleneck_label = tk.Label(
            health_frame,
            text="--",
            font=('Segoe UI', 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            wraplength=1100,
            justify=tk.LEFT
        )
        self.bottleneck_label.pack(anchor=tk.W, padx=15, pady=(0, 15))
    
    def start_benchmarks(self):
        """Start benchmark in background thread"""
        if self.is_benchmarking:
            messagebox.showwarning("Busy", "Benchmarks are already running!")
            return
        
        self.is_benchmarking = True
        self.btn_benchmark.config(state=tk.DISABLED, text="Running...")
        self.progress.start()
        self.label_status.config(text="Running benchmarks...", foreground=self.colors['accent_orange'])
        
        # Run in background thread
        thread = threading.Thread(target=self.run_benchmarks_thread, daemon=True)
        thread.start()
    
    def run_benchmarks_thread(self):
        """Run benchmarks in background"""
        try:
            self.results = self.benchmark.run_all_benchmarks()
            
            # Update UI from main thread
            self.root.after(0, self.update_results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Benchmark failed: {str(e)}"))
        finally:
            self.is_benchmarking = False
            self.root.after(0, self.benchmark_complete)
    
    def update_results(self):
        """Update UI with benchmark results"""
        if not self.results:
            return
        
        # Update each component card
        for component in ['cpu', 'ram', 'storage', 'gpu']:
            comp_data = self.results[component]
            
            local_score = comp_data['score']
            ref_score = comp_data['reference_score']
            diff_percent = self.benchmark.get_percent_difference(local_score, ref_score)
            status = comp_data['status']
            
            # Update scores
            self.score_labels[component].config(text=f"{local_score}/100")
            self.ref_labels[component].config(text=f"{ref_score}/100")
            self.diff_labels[component].config(text=f"{diff_percent:+.1f}%")
            
            # Update status with color coding
            status_color = self.get_status_color(status)
            self.diff_labels[component].config(fg=status_color)
            
            # Update status text with component details
            if component == 'cpu':
                detail = f"{comp_data['cores']} cores @ {comp_data['clock_speed_ghz']} GHz"
            elif component == 'ram':
                detail = f"{comp_data['total_gb']}GB ({comp_data['percent_used']}% used)"
            elif component == 'storage':
                detail = f"{comp_data['type']} - {comp_data['avg_speed_mbps']} MB/s"
            elif component == 'gpu':
                detail = f"{comp_data['class'].replace('_', ' ')} - {comp_data['vram_gb']}GB VRAM"
            else:
                detail = ""
            
            self.status_labels[component].config(
                text=f"{status}\n{detail}",
                fg=status_color
            )
        
        # Update overall health
        overall_score = self.results['overall_score']
        self.health_score_label.config(text=f"{overall_score}/100")
        
        # Classification
        if overall_score >= 85:
            classification = "Excellent"
            color = self.colors['accent_green']
        elif overall_score >= 70:
            classification = "Good"
            color = self.colors['accent_blue']
        elif overall_score >= 50:
            classification = "Average"
            color = self.colors['accent_orange']
        else:
            classification = "Poor"
            color = self.colors['accent_red']
        
        self.classification_label.config(text=classification, fg=color)
        
        # Identify bottleneck
        scores = {c: self.results[c]['score'] for c in ['cpu', 'ram', 'storage', 'gpu']}
        bottleneck = min(scores, key=scores.get)
        self.bottleneck_label.config(
            text=f"{bottleneck.upper()} is the limiting factor ({scores[bottleneck]}/100)\nConsider optimizing or upgrading this component"
        )
    
    def benchmark_complete(self):
        """Called when benchmarks complete"""
        self.progress.stop()
        self.btn_benchmark.config(state=tk.NORMAL, text="Run Benchmarks")
        self.label_status.config(text="Complete", foreground=self.colors['accent_green'])
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color based on status"""
        colors = {
            'ABOVE AVERAGE': '#4CAF50',
            'AVERAGE': '#2196F3',
            'BELOW AVERAGE': '#FF9800'
        }
        return colors.get(status, '#666666')


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
