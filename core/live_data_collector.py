"""
Live monitoring data collection module for SysOptima
Collects and maintains rolling buffers of system metrics for visualization
"""

import psutil
import time
from collections import deque
from datetime import datetime
try:
    import GPUtil
except ImportError:
    GPUtil = None


class LiveDataCollector:
    """Collects and maintains rolling buffers of system metrics"""
    
    def __init__(self, history_size: int = 60):
        """
        Initialize data collector with rolling buffers
        
        Args:
            history_size: Number of samples to maintain (default 60 for 60 seconds at 1Hz)
        """
        self.history_size = history_size
        
        # CPU data (percentages)
        self.cpu_history = deque(maxlen=history_size)
        
        # Memory data (GB)
        self.memory_history = deque(maxlen=history_size)
        
        # GPU data (percentage)
        self.gpu_history = deque(maxlen=history_size)
        self.gpu_temp_history = deque(maxlen=history_size)
        
        # Disk I/O (MB/s)
        self.disk_read_history = deque(maxlen=history_size)
        self.disk_write_history = deque(maxlen=history_size)
        
        # Last timestamp for disk I/O calculation
        self.last_disk_io = None
        self.last_disk_io_time = None
        
        # Current values
        self.current_cpu = 0.0
        self.current_memory = 0.0
        self.current_memory_total = 0.0
        self.current_gpu = 0.0
        self.current_gpu_temp = 0.0
        self.gpu_available = False
        self.current_disk_read = 0.0
        self.current_disk_write = 0.0
    
    def collect_cpu_data(self):
        """Collect CPU usage percentage (non-blocking)"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0)
            self.current_cpu = cpu_percent
            self.cpu_history.append(cpu_percent)
            return cpu_percent
        except Exception as e:
            print(f"CPU collection error: {e}")
            return 0.0
    
    def collect_memory_data(self):
        """Collect memory usage"""
        try:
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024**3)
            self.current_memory = used_gb
            self.current_memory_total = mem.total / (1024**3)
            self.memory_history.append(used_gb)
            return used_gb, mem.total / (1024**3)
        except Exception as e:
            print(f"Memory collection error: {e}")
            return 0.0, 0.0
    
    def collect_gpu_data(self):
        """Collect GPU usage and temperature"""
        try:
            if not GPUtil:
                return 0.0, 0.0, False
            
            gpus = GPUtil.getGPUs()
            if not gpus:
                self.gpu_available = False
                return 0.0, 0.0, False
            
            gpu = gpus[0]
            gpu_load = gpu.load * 100  # Convert to percentage
            gpu_temp = gpu.temperature if hasattr(gpu, 'temperature') else 0.0
            
            self.current_gpu = gpu_load
            self.current_gpu_temp = gpu_temp
            self.gpu_available = True
            
            self.gpu_history.append(gpu_load)
            self.gpu_temp_history.append(gpu_temp)
            
            return gpu_load, gpu_temp, True
        except Exception as e:
            print(f"GPU collection error: {e}")
            self.gpu_available = False
            return 0.0, 0.0, False
    
    def collect_disk_io_data(self):
        """Collect disk I/O speed (MB/s)"""
        try:
            current_io = psutil.disk_io_counters()
            current_time = time.time()
            
            if self.last_disk_io is None:
                # First measurement
                self.last_disk_io = current_io
                self.last_disk_io_time = current_time
                self.disk_read_history.append(0.0)
                self.disk_write_history.append(0.0)
                return 0.0, 0.0
            
            # Calculate speeds
            time_delta = current_time - self.last_disk_io_time
            if time_delta > 0:
                read_bytes_delta = current_io.read_bytes - self.last_disk_io.read_bytes
                write_bytes_delta = current_io.write_bytes - self.last_disk_io.write_bytes
                
                # Convert to MB/s
                read_speed = (read_bytes_delta / (1024**2)) / time_delta
                write_speed = (write_bytes_delta / (1024**2)) / time_delta
            else:
                read_speed = 0.0
                write_speed = 0.0
            
            self.current_disk_read = max(0, read_speed)  # Clamp to non-negative
            self.current_disk_write = max(0, write_speed)
            
            self.disk_read_history.append(self.current_disk_read)
            self.disk_write_history.append(self.current_disk_write)
            
            self.last_disk_io = current_io
            self.last_disk_io_time = current_time
            
            return self.current_disk_read, self.current_disk_write
        except Exception as e:
            print(f"Disk I/O collection error: {e}")
            self.disk_read_history.append(0.0)
            self.disk_write_history.append(0.0)
            return 0.0, 0.0
    
    def collect_all(self):
        """Collect all metrics in one call"""
        return {
            "cpu": self.collect_cpu_data(),
            "memory": self.collect_memory_data(),
            "gpu": self.collect_gpu_data(),
            "disk_io": self.collect_disk_io_data(),
            "timestamp": datetime.now()
        }
    
    def get_cpu_stats(self) -> dict:
        """Get CPU statistics"""
        if not self.cpu_history:
            return {"current": 0, "avg": 0, "max": 0, "min": 0}
        
        cpu_list = list(self.cpu_history)
        return {
            "current": round(cpu_list[-1], 1),
            "avg": round(sum(cpu_list) / len(cpu_list), 1),
            "max": round(max(cpu_list), 1),
            "min": round(min(cpu_list), 1),
            "history": cpu_list
        }
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics"""
        if not self.memory_history:
            return {"current": 0, "avg": 0, "max": 0, "min": 0, "total": 0}
        
        mem_list = list(self.memory_history)
        return {
            "current": round(mem_list[-1], 2),
            "avg": round(sum(mem_list) / len(mem_list), 2),
            "max": round(max(mem_list), 2),
            "min": round(min(mem_list), 2),
            "total": round(self.current_memory_total, 1),
            "history": mem_list
        }
    
    def get_gpu_stats(self) -> dict:
        """Get GPU statistics"""
        if not self.gpu_history:
            return {"current": 0, "avg": 0, "max": 0, "available": False, "temp": 0}
        
        gpu_list = list(self.gpu_history)
        return {
            "current": round(gpu_list[-1], 1),
            "avg": round(sum(gpu_list) / len(gpu_list), 1),
            "max": round(max(gpu_list), 1),
            "available": self.gpu_available,
            "temp": round(self.current_gpu_temp, 1),
            "history": gpu_list
        }
    
    def get_disk_io_stats(self) -> dict:
        """Get disk I/O statistics"""
        if not self.disk_read_history:
            return {"read": 0, "write": 0, "read_history": [], "write_history": []}
        
        read_list = list(self.disk_read_history)
        write_list = list(self.disk_write_history)
        
        return {
            "read": round(read_list[-1], 1),
            "write": round(write_list[-1], 1),
            "read_avg": round(sum(read_list) / len(read_list), 1),
            "write_avg": round(sum(write_list) / len(write_list), 1),
            "read_history": read_list,
            "write_history": write_list
        }
    
    def reset(self):
        """Reset all data"""
        self.cpu_history.clear()
        self.memory_history.clear()
        self.gpu_history.clear()
        self.gpu_temp_history.clear()
        self.disk_read_history.clear()
        self.disk_write_history.clear()
        self.last_disk_io = None
        self.last_disk_io_time = None
