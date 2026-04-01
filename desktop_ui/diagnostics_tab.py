"""
Diagnostics Tab - Rule-based System Diagnostics
Detects performance issues and provides recommendations
"""

import tkinter as tk
from tkinter import ttk
import psutil
import sys
import os
from desktop_ui.styles import COLORS, FONTS, SPACING

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import GPUtil
    HAS_GPUTIL = True
except ImportError:
    HAS_GPUTIL = False


class DiagnosticsTab:
    """Rule-based system diagnostics and recommendations"""
    
    def __init__(self, parent):
        """Initialize diagnostics tab"""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        self.create_widgets()
        self.update_diagnostics()
    
    def create_widgets(self):
        """Create UI widgets"""
        
        # Create main scrollable area
        main_frame = tk.Frame(self.frame, bg=COLORS["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING["lg"], pady=SPACING["md"])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_frame, yscrollcommand=scrollbar.set, bg=COLORS["bg_main"], highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Frame inside canvas
        self.content_frame = tk.Frame(canvas, bg=COLORS["bg_main"])
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Bind canvas configure event
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.content_frame.bind("<Configure>", on_frame_configure)
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def update_diagnostics(self):
        """Analyze system and update diagnostics display"""
        
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Collect system information
        metrics = self.collect_system_metrics()
        
        # Run diagnostics
        issues = self.run_diagnostics(metrics)
        
        # Display results
        self.display_diagnostics(issues)
    
    def collect_system_metrics(self):
        """Collect current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu_percent': cpu_percent,
            'cpu_cores': psutil.cpu_count(logical=False),
            'ram_percent': ram.percent,
            'ram_total_gb': round(ram.total / (1024**3), 2),
            'ram_used_gb': round(ram.used / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_total_gb': round(disk.total / (1024**3), 2),
            'disk_used_gb': round(disk.used / (1024**3), 2),
        }
        
        # Add GPU info if available
        if HAS_GPUTIL:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    metrics['gpu_percent'] = gpu.load * 100
                    metrics['gpu_name'] = gpu.name
                    metrics['gpu_memory_total'] = gpu.memoryTotal
                    metrics['gpu_memory_used'] = gpu.memoryUsed
            except:
                pass
        
        return metrics
    
    def run_diagnostics(self, metrics):
        """Run rule-based diagnostics"""
        issues = []
        
        # CPU Diagnostics
        cpu_issues = self.diagnose_cpu(metrics)
        issues.extend(cpu_issues)
        
        # RAM Diagnostics
        ram_issues = self.diagnose_ram(metrics)
        issues.extend(ram_issues)
        
        # Disk Diagnostics
        disk_issues = self.diagnose_disk(metrics)
        issues.extend(disk_issues)
        
        # GPU Diagnostics
        if 'gpu_percent' in metrics:
            gpu_issues = self.diagnose_gpu(metrics)
            issues.extend(gpu_issues)
        
        # Performance Summary
        if not issues:
            issues.append({
                'severity': 'good',
                'category': 'Overall',
                'title': '✓ System Running Normally',
                'description': 'All performance metrics are within normal ranges.',
                'recommendation': 'Continue monitoring for optimal performance.'
            })
        
        return issues
    
    def diagnose_cpu(self, metrics):
        """Diagnose CPU performance"""
        issues = []
        cpu = metrics['cpu_percent']
        cores = metrics.get('cpu_cores', 0)
        
        # Rule 1: Critical CPU usage
        if cpu > 90:
            issues.append({
                'severity': 'critical',
                'category': 'CPU',
                'title': '🔴 Critical CPU Usage Detected',
                'description': f'CPU is running at {cpu}% capacity - extremely high.',
                'what_is_problem': 'Your processor is severely overloaded.',
                'why_happens': 'Too many applications running simultaneously or a single process using excessive resources.',
                'what_caused': 'Check Task Manager for high CPU processes. Virus/malware might be present.',
                'how_fix': [
                    'Close unnecessary applications',
                    'Check for malware with antivirus',
                    'Update drivers and BIOS',
                    'Check for runaway processes in Task Manager',
                    'Disable startup programs'
                ]
            })
        
        # Rule 2: High CPU usage
        elif cpu > 70:
            issues.append({
                'severity': 'warning',
                'category': 'CPU',
                'title': '⚠ High CPU Usage',
                'description': f'CPU is running at {cpu}% - consistently high.',
                'what_is_problem': 'Your processor is heavily loaded.',
                'why_happens': 'Multiple demanding applications or background processes.',
                'what_caused': 'Check running applications and services.',
                'how_fix': [
                    'Close unused applications',
                    'Monitor background services',
                    'Disable unnecessary startup items',
                    'Check for resource-intensive processes'
                ]
            })
        
        # Rule 3: Low CPU core count
        if cores < 4:
            issues.append({
                'severity': 'info',
                'category': 'CPU',
                'title': 'ℹ Low Core Count',
                'description': f'Your CPU has only {cores} cores - may limit multitasking.',
                'what_is_problem': 'Limited parallel processing capability.',
                'why_happens': 'Older CPU or budget processor.',
                'what_caused': 'Hardware limitation.',
                'how_fix': [
                    'Consider upgrading to multi-core CPU',
                    'Use 64-bit OS for better utilization',
                    'Close background processes'
                ]
            })
        
        return issues
    
    def diagnose_ram(self, metrics):
        """Diagnose RAM performance"""
        issues = []
        ram_percent = metrics['ram_percent']
        ram_used = metrics['ram_used_gb']
        ram_total = metrics['ram_total_gb']
        
        # Rule 1: Critical RAM usage
        if ram_percent > 90:
            issues.append({
                'severity': 'critical',
                'category': 'RAM',
                'title': '🔴 Critical RAM Usage',
                'description': f'RAM is at {ram_percent}% ({ram_used}GB of {ram_total}GB used).',
                'what_is_problem': 'System memory is almost exhausted.',
                'why_happens': 'Too many applications or memory leaks.',
                'what_caused': 'Check running applications or search for memory leaks.',
                'how_fix': [
                    'Close memory-intensive applications',
                    'Restart browser to clear cache',
                    'Check for memory leak in applications',
                    'Upgrade RAM to at least 8GB',
                    'Use 64-bit OS'
                ]
            })
        
        # Rule 2: High RAM usage
        elif ram_percent > 75:
            issues.append({
                'severity': 'warning',
                'category': 'RAM',
                'title': '⚠ High RAM Usage',
                'description': f'RAM usage is high at {ram_percent}% ({ram_used}GB used).',
                'what_is_problem': 'Limited memory available for new tasks.',
                'why_happens': 'Multiple applications consuming memory.',
                'what_caused': 'Browser tabs, background apps, or large files.',
                'how_fix': [
                    'Close unused applications',
                    'Reduce browser tabs',
                    'Restart to clear memory',
                    'Consider RAM upgrade to 16GB'
                ]
            })
        
        # Rule 3: Low total RAM
        if ram_total < 8:
            issues.append({
                'severity': 'warning',
                'category': 'RAM',
                'title': '⚠ Low Total RAM',
                'description': f'Total RAM is only {ram_total}GB - below modern standards.',
                'what_is_problem': 'Insufficient memory for multitasking.',
                'why_happens': 'Older system configuration.',
                'what_caused': 'Hardware specification.',
                'how_fix': [
                    'Upgrade RAM to 16GB minimum',
                    'Use RAM upgrade (DDR4 or DDR5)',
                    'Check motherboard compatibility',
                    'Enable virtual memory as temporary workaround'
                ]
            })
        
        return issues
    
    def diagnose_disk(self, metrics):
        """Diagnose disk performance"""
        issues = []
        disk_percent = metrics['disk_percent']
        disk_used = metrics['disk_used_gb']
        disk_total = metrics['disk_total_gb']
        
        # Rule 1: Disk nearly full
        if disk_percent > 95:
            issues.append({
                'severity': 'critical',
                'category': 'Disk',
                'title': '🔴 Disk Almost Full',
                'description': f'Disk is at {disk_percent}% capacity ({disk_used}GB of {disk_total}GB).',
                'what_is_problem': 'Very little free space - system may crash or slow down.',
                'why_happens': 'Large files accumulated or insufficient drive space.',
                'what_caused': 'Downloads, temp files, or large applications.',
                'how_fix': [
                    'Delete unnecessary files and folders',
                    'Clear temporary files (Disk Cleanup)',
                    'Uninstall unused applications',
                    'Move files to external drive',
                    'Upgrade to larger SSD'
                ]
            })
        
        # Rule 2: Disk getting full
        elif disk_percent > 80:
            issues.append({
                'severity': 'warning',
                'category': 'Disk',
                'title': '⚠ Low Disk Space',
                'description': f'Disk usage is {disk_percent}% ({disk_used}GB used).',
                'what_is_problem': 'Reduced free space affects performance.',
                'why_happens': 'Accumulation of files over time.',
                'what_caused': 'Downloads, caches, and applications.',
                'how_fix': [
                    'Clean up temporary files',
                    'Uninstall unused programs',
                    'Archive old files',
                    'Consider larger storage device'
                ]
            })
        
        return issues
    
    def diagnose_gpu(self, metrics):
        """Diagnose GPU performance"""
        issues = []
        gpu_percent = metrics.get('gpu_percent', 0)
        gpu_name = metrics.get('gpu_name', 'Unknown')
        
        # Rule 1: High GPU usage
        if gpu_percent > 80:
            issues.append({
                'severity': 'info',
                'category': 'GPU',
                'title': 'ℹ High GPU Usage',
                'description': f'GPU ({gpu_name}) is at {gpu_percent}% - likely gaming or rendering.',
                'what_is_problem': 'GPU is heavily utilized.',
                'why_happens': 'Graphics-intensive task running.',
                'what_caused': 'Game, video editing, or 3D rendering.',
                'how_fix': [
                    'Lower in-game graphics settings',
                    'Reduce render quality',
                    'Close other applications',
                    'Update GPU drivers',
                    'Improve ventilation for cooling'
                ]
            })
        
        return issues
    
    def display_diagnostics(self, issues):
        """Display diagnostics results in UI"""
        
        # Group by severity
        severity_order = {'critical': 0, 'warning': 1, 'info': 2, 'good': 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get('severity'), 999))
        
        for issue in sorted_issues:
            self.display_issue(issue)
    
    def display_issue(self, issue):
        """Display a single diagnostic issue"""

        severity = issue.get("severity", "info")
        icon_map = {
            "critical": "⚠",
            "warning": "⚠",
            "info": "ℹ",
            "good": "✔"
        }
        color_map = {
            "critical": COLORS["danger"],
            "warning": COLORS["warning"],
            "info": COLORS["info"],
            "good": COLORS["success"]
        }
        icon = icon_map.get(severity, "ℹ")
        accent = color_map.get(severity, "#2563eb")

        # Card container
        card = tk.Frame(
            self.content_frame,
            bg=COLORS["bg_card"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        card.pack(fill=tk.X, pady=SPACING["sm"], padx=SPACING["sm"])

        header = tk.Frame(card, bg=COLORS["bg_card"])
        header.pack(fill=tk.X, padx=SPACING["md"], pady=(SPACING["sm"], SPACING["xs"]))

        title_label = tk.Label(
            header,
            text=f"{icon} {issue['title']}",
            font=FONTS["h2"],
            fg=accent,
            bg=COLORS["bg_card"],
            anchor=tk.W
        )
        title_label.pack(fill=tk.X)

        desc_label = tk.Label(
            card,
            text=issue.get("description", ""),
            font=FONTS["body"],
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=900
        )
        desc_label.pack(fill=tk.X, padx=SPACING["md"], pady=(0, SPACING["sm"]))

        if "what_is_problem" in issue:
            self._add_section(card, "What is the problem?", issue.get("what_is_problem", ""))
            self._add_section(card, "Why it happens", issue.get("why_happens", ""))
            self._add_section(card, "Root cause", issue.get("what_caused", ""))
            self._add_fixes(card, issue.get("how_fix", []))
        elif "recommendation" in issue:
            self._add_section(card, "Recommendation", issue.get("recommendation", ""))

    def _add_section(self, parent, title, body):
        section = tk.Frame(parent, bg=COLORS["bg_card"])
        section.pack(fill=tk.X, padx=SPACING["md"], pady=(0, SPACING["sm"]))

        title_label = tk.Label(
            section,
            text=title,
            font=FONTS["small"],
            fg=COLORS["text_main"],
            bg=COLORS["bg_card"],
            anchor=tk.W
        )
        title_label.pack(fill=tk.X)

        body_label = tk.Label(
            section,
            text=body,
            font=FONTS["body"],
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=900
        )
        body_label.pack(fill=tk.X)

    def _add_fixes(self, parent, fixes):
        section = tk.Frame(parent, bg=COLORS["bg_card"])
        section.pack(fill=tk.X, padx=SPACING["md"], pady=(0, SPACING["md"]))

        title_label = tk.Label(
            section,
            text="Actionable fixes",
            font=FONTS["small"],
            fg=COLORS["text_main"],
            bg=COLORS["bg_card"],
            anchor=tk.W
        )
        title_label.pack(fill=tk.X)

        if not fixes:
            fixes = ["No specific fixes available."]

        for fix in fixes:
            fix_label = tk.Label(
                section,
                text=f"• {fix}",
                font=FONTS["body"],
                fg=COLORS["text_dim"],
                bg=COLORS["bg_card"],
                anchor=tk.W,
                justify=tk.LEFT,
                wraplength=900
            )
            fix_label.pack(fill=tk.X)
    
    def cleanup(self):
        """Cleanup resources"""
        pass
