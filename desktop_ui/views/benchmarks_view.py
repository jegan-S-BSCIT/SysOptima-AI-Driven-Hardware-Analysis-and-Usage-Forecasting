"""
Benchmarks View - Safe Lightweight Benchmarking
Quick system evaluation without stress testing
"""
import tkinter as tk
from tkinter import ttk
import threading
import sys
import os

from desktop_ui.styles import COLORS, FONTS, SPACING

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.benchmark_engine import BenchmarkEngine


class BenchmarksView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        self.benchmark_engine = BenchmarkEngine()
        self.benchmark_thread = None
        self.running = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Content area (no AI panel - takes full width now)
        content = tk.Frame(self, bg=COLORS["bg_main"])
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING["xl"], pady=SPACING["xl"])
        
        # Header
        title = tk.Label(content, text="System Benchmark", font=FONTS["h1"],
                        bg=COLORS["bg_main"], fg=COLORS["text_main"])
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        desc = tk.Label(content, text="Lightweight performance measurement - Quick, safe, and non-stressful",
                       font=FONTS["body"], bg=COLORS["bg_main"], fg=COLORS["text_dim"])
        desc.pack(anchor="w", pady=(0, SPACING["lg"]))
        
        # Main benchmark button
        self.run_btn = tk.Button(content, text="▶ Run Full Benchmark",
                                bg=COLORS["accent"], fg=COLORS["text_main"],
                                font=("Segoe UI", 12, "bold"), relief=tk.FLAT,
                                padx=SPACING["lg"], pady=SPACING["md"],
                                command=self.start_full_benchmark)
        self.run_btn.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        
        # Component buttons
        btn_frame = tk.Frame(content, bg=COLORS["bg_main"])
        btn_frame.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        
        components = [("CPU", "cpu"), ("RAM", "ram"), ("Disk", "disk"), ("GPU", "gpu")]
        for i, (label, comp_key) in enumerate(components):
            btn_frame.columnconfigure(i, weight=1)
            btn = tk.Button(btn_frame, text=label, bg=COLORS["bg_card"], fg=COLORS["text_dim"],
                          font=FONTS["body"], relief=tk.FLAT, padx=SPACING["md"], pady=SPACING["md"],
                          command=lambda c=comp_key: self.start_single_benchmark(c))
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING["sm"])
        
        # Results container (scrollable)
        scroll_frame = tk.Frame(content, bg=COLORS["bg_main"])
        scroll_frame.pack(fill=tk.BOTH, expand=True, pady=SPACING["lg"])
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(scroll_frame, bg=COLORS["bg_main"], yscrollcommand=scrollbar.set,
                          highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        self.results_frame = tk.Frame(canvas, bg=COLORS["bg_main"])
        canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        
        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.results_frame.bind("<Configure>", on_configure)
        
        # Create result cards
        self.result_cards = {}
        for comp in ["CPU", "RAM", "DISK", "GPU"]:
            self.result_cards[comp] = self.create_result_card(comp)
        
        # Status message
        self.status_label = tk.Label(content, text="Ready to benchmark", font=FONTS["small"],
                                    bg=COLORS["bg_main"], fg=COLORS["text_dim"])
        self.status_label.pack(anchor="w", pady=(SPACING["lg"], 0))
    
    def create_result_card(self, component: str) -> dict:
        """Create a benchmark result card"""
        card = tk.Frame(self.results_frame, bg=COLORS["bg_card"], relief=tk.FLAT)
        card.pack(fill=tk.X, pady=SPACING["sm"])
        
        # Header
        header = tk.Frame(card, bg=COLORS["bg_card_alt"], height=40)
        header.pack(fill=tk.X)
        
        display_name = component.capitalize() if component == "DISK" else component
        title = tk.Label(header, text=f"  {display_name} Benchmark", font=("Segoe UI", 11, "bold"),
                        bg=COLORS["bg_card_alt"], fg=COLORS["text_main"])
        title.pack(side=tk.LEFT, padx=SPACING["md"], pady=SPACING["sm"])
        
        status = tk.Label(header, text="Not run", font=FONTS["small"],
                         bg=COLORS["bg_card_alt"], fg=COLORS["text_dim"])
        status.pack(side=tk.RIGHT, padx=SPACING["md"], pady=SPACING["sm"])
        
        # Content
        content = tk.Frame(card, bg=COLORS["bg_card"], padx=SPACING["lg"], pady=SPACING["lg"])
        content.pack(fill=tk.X)
        
        # Score display
        score_frame = tk.Frame(content, bg=COLORS["bg_card"])
        score_frame.pack(fill=tk.X, pady=(0, SPACING["md"]))
        
        score_label = tk.Label(score_frame, text="Score: --", font=("Segoe UI", 14, "bold"),
                              bg=COLORS["bg_card"], fg=COLORS["accent"])
        score_label.pack(side=tk.LEFT)
        
        detail_label = tk.Label(score_frame, text="", font=FONTS["small"],
                               bg=COLORS["bg_card"], fg=COLORS["text_dim"])
        detail_label.pack(side=tk.RIGHT)
        
        # Progress bar
        progress = tk.Canvas(content, height=6, bg=COLORS["bg_input"], highlightthickness=0)
        progress.pack(fill=tk.X, pady=(0, SPACING["md"]))
        
        # Description
        desc_label = tk.Label(content, text="", font=FONTS["small"],
                             bg=COLORS["bg_card"], fg=COLORS["text_muted"], wraplength=500, justify=tk.LEFT)
        desc_label.pack(anchor="w")
        
        return {
            'card': card,
            'status': status,
            'score': score_label,
            'detail': detail_label,
            'progress': progress,
            'description': desc_label
        }
    
    def start_full_benchmark(self):
        """Start full benchmark in background thread"""
        if self.running:
            return
        
        self.running = True
        self.run_btn.config(state=tk.DISABLED, text="Running...")
        self.status_label.config(text="Running benchmark... (do not close)", fg=COLORS["warning"])
        
        self.benchmark_thread = threading.Thread(target=self._run_full_benchmark, daemon=True)
        self.benchmark_thread.start()
    
    def start_single_benchmark(self, component: str):
        """Start single component benchmark"""
        if self.running:
            return
        
        self.running = True
        self.status_label.config(text=f"Running {component} benchmark...", fg=COLORS["warning"])
        
        self.benchmark_thread = threading.Thread(
            target=self._run_single_benchmark,
            args=(component,),
            daemon=True
        )
        self.benchmark_thread.start()
    
    def _run_full_benchmark(self):
        """Background thread: run all benchmarks"""
        try:
            def progress_callback(msg, progress=None):
                self.after(0, lambda: self._update_progress(msg, progress))
            
            self.benchmark_engine.set_callback(progress_callback)
            results = self.benchmark_engine.run_all()
            
            self.after(0, lambda: self._display_results(results))
        
        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))
        
        finally:
            self.running = False
            self.after(0, self._reset_ui)
    
    def _run_single_benchmark(self, component: str):
        """Background thread: run single benchmark"""
        try:
            methods = {
                'cpu': self.benchmark_engine.run_cpu,
                'ram': self.benchmark_engine.run_memory,
                'disk': self.benchmark_engine.run_disk,
                'gpu': self.benchmark_engine.run_gpu,
            }
            
            method = methods.get(component.lower())
            if method:
                result = method()
                self.after(0, lambda: self._display_single_result(component.upper(), result))
        
        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))
        
        finally:
            self.running = False
            self.after(0, self._reset_ui)
    
    def _update_progress(self, message: str, progress: int = None):
        """Update progress message"""
        self.status_label.config(text=message, fg=COLORS["warning"])
    
    def _display_results(self, results: dict):
        """Display benchmark results"""
        for component, data in results.items():
            if component == 'overall':
                continue
            
            comp_upper = component.upper()
            if comp_upper in self.result_cards:
                self._update_card(comp_upper, data)
        
        # Show overall score
        if 'overall' in results:
            overall = results['overall']['score']
            self.status_label.config(
                text=f"✓ Benchmark complete! Overall score: {overall}/100",
                fg=COLORS["success"]
            )
    
    def _display_single_result(self, component: str, result: dict):
        """Display single benchmark result"""
        self._update_card(component, result)
    
    def _update_card(self, component: str, data: dict):
        """Update result card with data"""
        if component not in self.result_cards:
            return
        
        card = self.result_cards[component]
        
        if 'error' in data:
            card['status'].config(text="Error", fg=COLORS["danger"])
            card['description'].config(text=data['error'], fg=COLORS["danger"])
            return
        
        if 'score' not in data:
            return
        
        score = data['score']
        status = data.get('status', 'Unknown')
        
        # Update score
        card['score'].config(text=f"Score: {score}/100")
        
        # Update status with color
        status_color = {
            'Excellent': COLORS["success"],
            'Good': COLORS["info"],
            'Average': COLORS["warning"],
            'Below Average': COLORS["warning"],
            'Poor': COLORS["danger"]
        }.get(status, COLORS["text_dim"])
        
        card['status'].config(text=status, fg=status_color)
        
        # Update progress bar
        progress = card['progress']
        width = progress.winfo_width()
        if width > 10:
            fill_width = (score / 100) * width
            progress.create_rectangle(0, 0, fill_width, 6, fill=status_color, outline="")
        
        # Add details
        details = []
        if 'elapsed' in data:
            details.append(f"Time: {data['elapsed']:.2f}s")
        if 'bandwidth_mbps' in data:
            details.append(f"Speed: {data['bandwidth_mbps']:.0f} MB/s")
        if 'write_mbps' in data:
            details.append(f"Write: {data['write_mbps']:.0f} MB/s | Read: {data['read_mbps']:.0f} MB/s")
        if 'name' in data:
            details.append(f"GPU: {data['name']} ({data.get('vram_gb', '?')} GB)")
        
        detail_text = " • ".join(details)
        card['detail'].config(text=detail_text)
        
        # Add description
        desc = self._get_benchmark_description(component, score)
        card['description'].config(text=desc)
    
    def _get_benchmark_description(self, component: str, score: int) -> str:
        """Generate description based on score"""
        if score >= 80:
            return f"{component} is performing excellent."
        elif score >= 65:
            return f"{component} is performing well above average."
        elif score >= 50:
            return f"{component} is performing at average level."
        elif score >= 35:
            return f"{component} is performing below average. Consider optimization."
        else:
            return f"{component} is performing poorly. Hardware limitations detected."
    
    def _show_error(self, error: str):
        """Show error message"""
        self.status_label.config(text=f"Error: {error}", fg=COLORS["danger"])
    
    def _reset_ui(self):
        """Reset UI after benchmark"""
        self.run_btn.config(state=tk.NORMAL, text="▶ Run Full Benchmark")
    
    def cleanup(self):
        """Clean up on view close"""
        if self.running:
            self.benchmark_engine.cancel()

