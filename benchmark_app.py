"""
Standalone Benchmark Application
B.Sc. IT Final Year Project - System Performance Analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import psutil
import math
import tempfile
import os
from typing import Dict


class LightweightBenchmark:
    """Lightweight benchmarking engine"""
    
    def __init__(self):
        self.results = {}
        self.reference = {
            "cpu_reference": {"average_score": 65},
            "ram_reference": {"average_score": 70},
            "storage_reference": {"average_score": 60},
            "gpu_reference": {"average_score": 65}
        }
    
    def run_all_benchmarks(self) -> Dict:
        """Run all benchmarks"""
        results = {
            "cpu": self.benchmark_cpu(),
            "ram": self.benchmark_ram(),
            "storage": self.benchmark_storage(),
            "gpu": self.benchmark_gpu(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        scores = [r["score"] for r in [results["cpu"], results["ram"], results["storage"], results["gpu"]]]
        results["overall_score"] = round(sum(scores) / len(scores), 1)
        
        self.results = results
        return results
    
    def benchmark_cpu(self) -> Dict:
        """CPU benchmark"""
        start_time = time.time()
        
        logical_cores = psutil.cpu_count(logical=True)
        physical_cores = psutil.cpu_count(logical=False)
        freq = psutil.cpu_freq()
        clock_speed_ghz = (freq.current / 1000) if freq else 3.0
        
        # Mathematical workload
        result = 0
        for i in range(10000000):
            result += math.sqrt(i % 1000)
        
        elapsed = time.time() - start_time
        
        core_score = min((logical_cores / 8) * 85, 100)
        speed_score = min((clock_speed_ghz / 4.0) * 90, 100)
        cpu_score = (core_score * 0.6 + speed_score * 0.4)
        
        ref_score = self.reference.get("cpu_reference", {}).get("average_score", 65)
        
        return {
            "score": round(cpu_score, 1),
            "reference_score": ref_score,
            "cores": logical_cores,
            "clock_speed_ghz": round(clock_speed_ghz, 2),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(cpu_score, ref_score)
        }
    
    def benchmark_ram(self) -> Dict:
        """RAM benchmark"""
        start_time = time.time()
        
        ram_info = psutil.virtual_memory()
        total_gb = ram_info.total / (1024**3)
        percent_used = ram_info.percent
        available_gb = ram_info.available / (1024**3)
        
        test_size_mb = 50
        allocation_times = []
        
        for _ in range(5):
            alloc_start = time.time()
            data = bytearray(test_size_mb * 1024 * 1024)
            for i in range(0, len(data), 1024):
                data[i:i+4] = bytearray([1, 2, 3, 4])
            _ = sum(data[i] for i in range(0, min(len(data), 100000), 100))
            allocation_times.append(time.time() - alloc_start)
            del data
        
        elapsed = time.time() - start_time
        
        capacity_score = min((total_gb / 16) * 90, 100)
        usage_score = max(0, 100 - (percent_used * 1.5))
        ram_score = (capacity_score * 0.6 + usage_score * 0.4)
        
        ref_score = self.reference.get("ram_reference", {}).get("average_score", 70)
        
        return {
            "score": round(ram_score, 1),
            "reference_score": ref_score,
            "total_gb": round(total_gb, 1),
            "available_gb": round(available_gb, 1),
            "percent_used": round(percent_used, 1),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(ram_score, ref_score)
        }
    
    def benchmark_storage(self) -> Dict:
        """Storage benchmark"""
        start_time = time.time()
        
        partitions = psutil.disk_partitions()
        drive_c = None
        for p in partitions:
            if p.device == 'C:\\':
                drive_c = p
                break
        
        if drive_c is None:
            drive_c = partitions[0] if partitions else None
        
        if drive_c:
            usage = psutil.disk_usage(drive_c.mountpoint)
            drive_name = drive_c.device
            fstype = drive_c.fstype
        else:
            drive_name = "Unknown"
            fstype = "Unknown"
        
        test_file_size_mb = 50
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "benchmark_test.bin")
                
                write_start = time.time()
                with open(test_file, 'wb') as f:
                    f.write(b'x' * (test_file_size_mb * 1024 * 1024))
                write_time = time.time() - write_start
                write_speed = test_file_size_mb / write_time if write_time > 0 else 0
                
                read_start = time.time()
                with open(test_file, 'rb') as f:
                    _ = f.read()
                read_time = time.time() - read_start
                read_speed = test_file_size_mb / read_time if read_time > 0 else 0
                
        except:
            read_speed = 100
            write_speed = 100
        
        avg_speed = (read_speed + write_speed) / 2
        is_ssd = fstype.lower() in ['ntfs', 'ext4', 'apfs'] and avg_speed > 200
        
        if is_ssd:
            speed_score = min((avg_speed / 550) * 70, 100)
        else:
            speed_score = min((avg_speed / 150) * 30, 100)
        
        storage_score = speed_score
        ref_score = self.reference.get("storage_reference", {}).get("average_score", 60)
        
        elapsed = time.time() - start_time
        
        return {
            "score": round(storage_score, 1),
            "reference_score": ref_score,
            "drive": drive_name,
            "fstype": fstype,
            "type": "SSD" if is_ssd else "HDD",
            "read_speed_mbps": round(read_speed, 1),
            "write_speed_mbps": round(write_speed, 1),
            "avg_speed_mbps": round(avg_speed, 1),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(storage_score, ref_score)
        }
    
    def benchmark_gpu(self) -> Dict:
        """GPU benchmark"""
        start_time = time.time()
        
        gpu_data = {}
        gpu_score = 0
        gpu_class = "unknown"
        
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            
            if gpus:
                gpu = gpus[0]
                vram_gb = gpu.memoryTotal / 1024
                gpu_name = gpu.name
                
                if vram_gb <= 2:
                    gpu_class = "entry_level"
                    gpu_score = 40
                elif vram_gb <= 4:
                    gpu_class = "mid_range"
                    gpu_score = 65
                elif vram_gb <= 8:
                    gpu_class = "high_performance"
                    gpu_score = 85
                else:
                    gpu_class = "professional"
                    gpu_score = 100
                
                gpu_data = {
                    "name": gpu_name,
                    "vram_gb": round(vram_gb, 1),
                    "class": gpu_class,
                    "temperature": round(gpu.temperature, 1) if hasattr(gpu, 'temperature') else None
                }
        except:
            gpu_data = {"name": "Integrated Graphics", "vram_gb": 0}
            gpu_class = "integrated"
            gpu_score = 30
        
        elapsed = time.time() - start_time
        ref_score = self.reference.get("gpu_reference", {}).get("average_score", 65)
        
        return {
            "score": round(gpu_score, 1),
            "reference_score": ref_score,
            "name": gpu_data.get("name", "Unknown"),
            "vram_gb": gpu_data.get("vram_gb", 0),
            "class": gpu_class,
            "temperature_c": gpu_data.get("temperature"),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(gpu_score, ref_score)
        }
    
    @staticmethod
    def _compare_score(local: float, reference: float) -> str:
        """Compare local vs reference"""
        diff_percent = ((local - reference) / reference) * 100
        
        if diff_percent > 10:
            return "ABOVE AVERAGE"
        elif diff_percent > -10:
            return "AVERAGE"
        else:
            return "BELOW AVERAGE"
    
    def get_percent_difference(self, local: float, reference: float) -> float:
        """Calculate percentage difference"""
        if reference == 0:
            return 0
        return round(((local - reference) / reference) * 100, 1)


class ModernDashboard:
    """Modern benchmark dashboard"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("System Performance Benchmark - B.Sc. IT Project")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
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
        
        self.benchmark = LightweightBenchmark()
        self.results = None
        self.is_benchmarking = False
        
        self.create_ui()
    
    def create_ui(self):
        """Create UI"""
        # Header
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
            fg='white',
            pady=10
        )
        subtitle.pack()
        
        # Main content
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg=self.colors['bg_main'])
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        self.btn_benchmark = tk.Button(
            left_panel,
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
        
        self.label_status = tk.Label(
            left_panel,
            text="Ready",
            fg=self.colors['accent_green'],
            bg=self.colors['bg_main'],
            font=('Segoe UI', 10)
        )
        self.label_status.pack(pady=(10, 0))
        
        self.progress = ttk.Progressbar(left_panel, mode='indeterminate', length=250)
        self.progress.pack(fill=tk.X, pady=10)
        
        # Right panel - Results
        right_panel = tk.Frame(main_container, bg=self.colors['bg_main'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.component_frames = {}
        cards_container = tk.Frame(right_panel, bg=self.colors['bg_main'])
        cards_container.pack(fill=tk.BOTH, expand=True)
        
        components = [
            ('cpu', 'CPU Performance', 0, 0),
            ('ram', 'RAM Performance', 0, 1),
            ('storage', 'Storage Performance', 1, 0),
            ('gpu', 'GPU Performance', 1, 1)
        ]
        
        self.score_labels = {}
        self.ref_labels = {}
        self.diff_labels = {}
        self.status_labels = {}
        
        for component_id, title, row, col in components:
            frame = self.create_component_card(cards_container, title, component_id)
            frame.grid(row=row, column=col, sticky='nsew', padx=(0, 10), pady=(0, 10))
            self.component_frames[component_id] = frame
        
        cards_container.rowconfigure(0, weight=1)
        cards_container.rowconfigure(1, weight=1)
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)
        
        # Bottom section
        bottom_section = tk.Frame(right_panel, bg=self.colors['bg_main'])
        bottom_section.pack(fill=tk.X, pady=(20, 0))
        
        self.create_health_section(bottom_section)
    
    def create_component_card(self, parent, title: str, component_id: str) -> tk.Frame:
        """Create component card"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT)
        card.configure(highlightthickness=1, highlightbackground=self.colors['border_light'])
        
        title_label = tk.Label(
            card,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        scores_frame = tk.Frame(card, bg=self.colors['bg_card'])
        scores_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(scores_frame, text="Your Score:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.score_labels[component_id] = tk.Label(
            scores_frame,
            text="--/100",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_blue']
        )
        self.score_labels[component_id].pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(scores_frame, text="Reference:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.ref_labels[component_id] = tk.Label(
            scores_frame,
            text="--/100",
            font=('Segoe UI', 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.ref_labels[component_id].pack(side=tk.LEFT, padx=5)
        
        diff_frame = tk.Frame(card, bg=self.colors['bg_card'])
        diff_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(diff_frame, text="Difference:", bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        self.diff_labels[component_id] = tk.Label(
            diff_frame,
            text="--%",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.diff_labels[component_id].pack(side=tk.LEFT, padx=5)
        
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
        """Create health section"""
        health_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT)
        health_frame.configure(highlightthickness=1, highlightbackground=self.colors['border_light'])
        health_frame.pack(fill=tk.X)
        
        tk.Label(
            health_frame,
            text="Overall System Health",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
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
        """Start benchmarks"""
        if self.is_benchmarking:
            messagebox.showwarning("Busy", "Benchmarks are already running!")
            return
        
        self.is_benchmarking = True
        self.btn_benchmark.config(state=tk.DISABLED, text="Running...")
        self.progress.start()
        self.label_status.config(text="Running benchmarks...", fg=self.colors['accent_orange'])
        
        thread = threading.Thread(target=self.run_benchmarks_thread, daemon=True)
        thread.start()
    
    def run_benchmarks_thread(self):
        """Run benchmarks"""
        try:
            self.results = self.benchmark.run_all_benchmarks()
            self.root.after(0, self.update_results)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Benchmark failed: {str(e)}"))
        finally:
            self.is_benchmarking = False
            self.root.after(0, self.benchmark_complete)
    
    def update_results(self):
        """Update results"""
        if not self.results:
            return
        
        for component in ['cpu', 'ram', 'storage', 'gpu']:
            comp_data = self.results[component]
            
            local_score = comp_data['score']
            ref_score = comp_data['reference_score']
            diff_percent = self.benchmark.get_percent_difference(local_score, ref_score)
            status = comp_data['status']
            
            self.score_labels[component].config(text=f"{local_score}/100")
            self.ref_labels[component].config(text=f"{ref_score}/100")
            self.diff_labels[component].config(text=f"{diff_percent:+.1f}%")
            
            status_color = self.get_status_color(status)
            self.diff_labels[component].config(fg=status_color)
            
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
        
        overall_score = self.results['overall_score']
        self.health_score_label.config(text=f"{overall_score}/100")
        
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
        
        scores = {c: self.results[c]['score'] for c in ['cpu', 'ram', 'storage', 'gpu']}
        bottleneck = min(scores, key=scores.get)
        self.bottleneck_label.config(
            text=f"{bottleneck.upper()} is the limiting factor ({scores[bottleneck]}/100)"
        )
    
    def benchmark_complete(self):
        """Benchmark complete"""
        self.progress.stop()
        self.btn_benchmark.config(state=tk.NORMAL, text="Run Benchmarks")
        self.label_status.config(text="Complete", fg=self.colors['accent_green'])
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """Get status color"""
        colors = {
            'ABOVE AVERAGE': '#4CAF50',
            'AVERAGE': '#2196F3',
            'BELOW AVERAGE': '#FF9800'
        }
        return colors.get(status, '#666666')


def main():
    """Main"""
    root = tk.Tk()
    app = ModernDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
