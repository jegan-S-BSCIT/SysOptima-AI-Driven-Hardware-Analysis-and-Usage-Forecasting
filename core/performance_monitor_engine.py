"""
Real-Time Performance Monitor Engine
=========================================
Thread-safe, non-blocking data collection for live system metrics.

This module handles:
- Live CPU, RAM, GPU, and Disk I/O monitoring
- Thread-safe data buffering (30-second sliding window)
- Diagnostic flags for anomalies
- GPU detection with graceful fallback

For B.Sc. IT Project: "Intelligent Computer Performance Analysis and Guidance System"
=========================================
"""

import psutil
import time
from threading import Thread, Lock, Event
from collections import deque
from datetime import datetime
import subprocess


class PerformanceMonitorEngine:
    """
    Thread-safe real-time performance monitoring engine.
    
    Collects system metrics every 1 second and maintains a 30-second sliding window.
    Designed for academic demonstration and production use.
    
    Attributes:
        data_buffer: Deque of timestamped metric snapshots
        diagnostics: Dictionary of active diagnostic flags
        monitoring: Boolean indicating if collection is active
    """

    def __init__(self, buffer_size=30, collection_interval=1.0):
        """
        Initialize the performance monitor.
        
        Args:
            buffer_size (int): Number of seconds of historical data to maintain (default: 30)
            collection_interval (float): Seconds between data collections (default: 1.0)
        """
        self.buffer_size = buffer_size
        self.collection_interval = collection_interval
        
        # Thread-safe data storage
        self.data_buffer = deque(maxlen=buffer_size)  # Automatically maintains 30-second window
        self.data_lock = Lock()
        
        # Monitoring control
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        
        # Diagnostic state tracking
        self.diagnostics = {
            'high_cpu_load': False,
            'high_cpu_duration': 0,
            'memory_pressure': False,
            'disk_bottleneck': False,
            'gpu_unavailable': False
        }
        
        # Previous disk I/O state (for delta calculation)
        self._disk_io_prev = psutil.disk_io_counters()
        self._prev_sample_time = time.time()
        
        # GPU availability check (cached)
        self._gpu_available = self._check_gpu_available()

    def _check_gpu_available(self):
        """
        Check if GPU is available on the system.
        
        Returns:
            bool: True if NVIDIA GPU detected, False otherwise
        """
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return len(gpus) > 0
        except Exception:
            pass

        try:
            subprocess.check_output(
                ["nvidia-smi", "--query-gpu=name"],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        return False

    def _get_gpu_usage(self):
        """
        Safely retrieve GPU utilization percentage.
        
        Returns:
            tuple: (gpu_percent: float, gpu_memory: float)
                   Returns (0.0, 0.0) if GPU unavailable
        """
        # Method 1: GPUtil (recommended for Python)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return gpu.load * 100, gpu.memoryUsed / gpu.memoryTotal * 100
        except Exception:
            pass

        # Method 2: nvidia-smi command-line tool
        try:
            result = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,utilization.memory",
                    "--format=csv,noheader,nounits"
                ],
                encoding="utf-8",
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            parts = result.strip().split(",")
            if len(parts) == 2:
                return float(parts[0].strip()), float(parts[1].strip())
        except Exception:
            pass

        # GPU unavailable
        if not self.diagnostics['gpu_unavailable']:
            self.diagnostics['gpu_unavailable'] = True
        return 0.0, 0.0

    def _collect_metrics(self):
        """
        Collect a single snapshot of system metrics.
        
        Returns:
            dict: Timestamped metrics dictionary
        """
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time)

        # CPU Metrics
        cpu_percent = psutil.cpu_percent(interval=0)
        cpu_count = psutil.cpu_count(logical=True)

        # RAM Metrics
        ram_info = psutil.virtual_memory()
        ram_percent = ram_info.percent
        ram_used_mb = ram_info.used / (1024**2)
        ram_total_mb = ram_info.total / (1024**2)

        # GPU Metrics
        gpu_percent, gpu_memory_percent = self._get_gpu_usage()

        # Disk I/O Metrics (delta from previous sample)
        disk_io = psutil.disk_io_counters()
        time_delta = max(current_time - self._prev_sample_time, 0.001)  # Avoid division by zero

        disk_read_mb = (disk_io.read_bytes - self._disk_io_prev.read_bytes) / (1024**2) / time_delta
        disk_write_mb = (disk_io.write_bytes - self._disk_io_prev.write_bytes) / (1024**2) / time_delta

        self._disk_io_prev = disk_io
        self._prev_sample_time = current_time

        # Cap negative values (can occur on system reboot)
        disk_read_mb = max(disk_read_mb, 0)
        disk_write_mb = max(disk_write_mb, 0)

        return {
            'timestamp': timestamp,
            'timestamp_unix': current_time,
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'ram_percent': ram_percent,
            'ram_used_mb': ram_used_mb,
            'ram_total_mb': ram_total_mb,
            'gpu_percent': gpu_percent,
            'gpu_memory_percent': gpu_memory_percent,
            'disk_read_mb': disk_read_mb,
            'disk_write_mb': disk_write_mb,
        }

    def _update_diagnostics(self):
        """
        Update diagnostic flags based on recent metrics.
        
        Flags triggered:
        - High CPU Load: CPU > 85% for 10+ consecutive seconds
        - Memory Pressure: RAM > 80%
        - Disk Bottleneck: Sustained high disk activity
        """
        if not self.data_buffer:
            return

        # Get latest sample
        latest = self.data_buffer[-1]

        # Diagnostic 1: High CPU Load (sustained for 10 seconds)
        if latest['cpu_percent'] > 85:
            self.diagnostics['high_cpu_duration'] += self.collection_interval
            if self.diagnostics['high_cpu_duration'] >= 10:
                self.diagnostics['high_cpu_load'] = True
        else:
            self.diagnostics['high_cpu_duration'] = 0
            self.diagnostics['high_cpu_load'] = False

        # Diagnostic 2: Memory Pressure
        self.diagnostics['memory_pressure'] = latest['ram_percent'] > 80

        # Diagnostic 3: Disk Bottleneck (continuous high activity)
        # Threshold: > 50 MB/s sustained for 5+ seconds
        if len(self.data_buffer) >= 5:
            recent_samples = list(self.data_buffer)[-5:]
            high_disk_count = sum(
                1 for s in recent_samples
                if (s['disk_read_mb'] + s['disk_write_mb']) > 50
            )
            self.diagnostics['disk_bottleneck'] = high_disk_count >= 4

    def _monitor_loop(self):
        """
        Main monitoring loop (runs in separate thread).
        
        Collects metrics every collection_interval seconds and updates diagnostics.
        """
        while not self.stop_event.is_set():
            try:
                # Collect metrics
                snapshot = self._collect_metrics()

                # Thread-safe buffer update
                with self.data_lock:
                    self.data_buffer.append(snapshot)
                    self._update_diagnostics()

                # Sleep until next collection
                time.sleep(self.collection_interval)

            except Exception as e:
                # Log error but continue monitoring
                print(f"[PerformanceMonitor] Error during collection: {e}")
                time.sleep(self.collection_interval)

    def start_monitoring(self):
        """Start the monitoring thread."""
        if not self.monitoring:
            self.monitoring = True
            self.stop_event.clear()
            self.monitor_thread = Thread(
                target=self._monitor_loop,
                daemon=True,
                name="PerformanceMonitorThread"
            )
            self.monitor_thread.start()
            print("[PerformanceMonitor] Monitoring started")

    def stop_monitoring(self):
        """Stop the monitoring thread."""
        if self.monitoring:
            self.monitoring = False
            self.stop_event.set()
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2)
            print("[PerformanceMonitor] Monitoring stopped")

    def get_latest_snapshot(self):
        """
        Get the most recent metrics snapshot.
        
        Returns:
            dict: Latest metrics or None if no data collected yet
        """
        with self.data_lock:
            return self.data_buffer[-1] if self.data_buffer else None

    def get_buffer_copy(self):
        """
        Get a safe copy of the entire data buffer.
        
        Returns:
            list: Copy of all buffered metrics (thread-safe)
        """
        with self.data_lock:
            return list(self.data_buffer)

    def get_diagnostics(self):
        """
        Get current diagnostic state.
        
        Returns:
            dict: Diagnostic flags and status information
        """
        with self.data_lock:
            return self.diagnostics.copy()

    def get_statistics(self):
        """
        Calculate statistics from buffered data.
        
        Returns:
            dict: Min/max/avg statistics for all metrics
        """
        with self.data_lock:
            if not self.data_buffer:
                return None

            buffer_list = list(self.data_buffer)

            def safe_calc(key):
                values = [s[key] for s in buffer_list if key in s]
                if not values:
                    return {'min': 0, 'max': 0, 'avg': 0}
                return {
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values)
                }

            return {
                'cpu': safe_calc('cpu_percent'),
                'ram': safe_calc('ram_percent'),
                'gpu': safe_calc('gpu_percent'),
                'disk_read': safe_calc('disk_read_mb'),
                'disk_write': safe_calc('disk_write_mb'),
            }
