"""
Real-time System Monitoring Module
Monitors CPU, RAM, Disk, and Network usage in real-time
"""

import psutil
import time
import subprocess
from threading import Thread, Event

class SystemMonitor:
    """Real-time system resource monitoring"""
    
    def __init__(self, interval=1.0):
        self.interval = interval
        self.monitoring = False
        self.monitor_thread = None
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        self.callback = None
        
        self.current_data = {
            'cpu_percent': 0,
            'ram_percent': 0,
            'gpu_percent': 0,
            'disk_read_mb': 0,
            'disk_write_mb': 0,
            'network_sent_mb': 0,
            'network_recv_mb': 0,
            'timestamp': 0
        }

    def _get_gpu_usage(self):
        """Safely get GPU usage if available"""
        # Method 1: GPUtil (Python native)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
        except Exception:
            pass

        # Method 2: nvidia-smi (Command line)
        try:
            result = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            )
            # Output is like "45" or "0"
            return float(result.strip())
        except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
            pass
            
        return 0.0

    def set_callback(self, callback):
        """Set a function to be called on each update"""
        self.callback = callback
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        if not self.monitoring:
            self.monitoring = True
            self.stop_event.clear()
            self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        if self.monitoring:
            self.monitoring = False
            self.stop_event.set()
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        disk_io_prev = psutil.disk_io_counters()
        net_io_prev = psutil.net_io_counters()
        
        while not self.stop_event.is_set():
            # CPU usage (non-blocking)
            self.current_data['cpu_percent'] = psutil.cpu_percent(interval=0)
            
            # RAM usage
            self.current_data['ram_percent'] = psutil.virtual_memory().percent
            
            # GPU usage
            self.current_data['gpu_percent'] = self._get_gpu_usage()
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            self.current_data['disk_read_mb'] = (disk_io.read_bytes - disk_io_prev.read_bytes) / (1024**2)
            self.current_data['disk_write_mb'] = (disk_io.write_bytes - disk_io_prev.write_bytes) / (1024**2)
            disk_io_prev = disk_io
            
            # Network I/O
            net_io = psutil.net_io_counters()
            self.current_data['network_sent_mb'] = (net_io.bytes_sent - net_io_prev.bytes_sent) / (1024**2)
            self.current_data['network_recv_mb'] = (net_io.bytes_recv - net_io_prev.bytes_recv) / (1024**2)
            net_io_prev = net_io
            
            self.current_data['timestamp'] = time.time()
            
            if self.callback:
                try:
                    self.callback(self.current_data.copy())
                except Exception:
                    pass
            
            time.sleep(self.interval)
    
    def get_current_data(self):
        """Get the latest monitoring data"""
        return self.current_data.copy()
