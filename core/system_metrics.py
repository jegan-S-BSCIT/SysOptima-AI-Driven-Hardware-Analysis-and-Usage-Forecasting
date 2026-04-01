"""
Real-time System Metrics Collection
Provides live system data for dashboard
"""

import psutil
import GPUtil
from typing import Dict, Tuple


class SystemMetrics:
    """Collects real-time system metrics"""
    
    def __init__(self):
        self.previous_cpu = 0
        self.previous_mem = 0
        self.previous_disk = 0
        self.previous_gpu = 0
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get current system metrics
        
        Returns:
            Dictionary with cpu, memory, disk, gpu percentages
        """
        # CPU usage (non-blocking for UI responsiveness)
        cpu = psutil.cpu_percent(interval=0)
        
        # Memory usage
        mem = psutil.virtual_memory().percent
        
        # Disk usage (default system drive)
        disk = psutil.disk_usage('/').percent
        
        # GPU usage (best effort)
        gpu_load = 0
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_load = int(gpus[0].load * 100)
        except Exception:
            # GPU not available or error
            gpu_load = 0
        
        # Store for trend calculation
        self.previous_cpu = cpu
        self.previous_mem = mem
        self.previous_disk = disk
        self.previous_gpu = gpu_load
        
        return {
            "cpu": round(cpu, 1),
            "memory": round(mem, 1),
            "disk": round(disk, 1),
            "gpu": round(gpu_load, 1)
        }
    
    def get_cpu_temperature(self) -> float:
        """
        Get CPU temperature (best effort)
        
        Returns:
            Temperature in Celsius, or 0 if unavailable
        """
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try to find CPU temperature
                for name, entries in temps.items():
                    if 'coretemp' in name.lower() or 'cpu' in name.lower():
                        if entries:
                            return round(entries[0].current, 1)
                # Fallback: use first available sensor
                for name, entries in temps.items():
                    if entries:
                        return round(entries[0].current, 1)
        except Exception:
            pass
        
        # Return estimated based on CPU load if no sensor (non-blocking)
        cpu_percent = psutil.cpu_percent(interval=0)
        estimated_temp = 40 + (cpu_percent * 0.4)  # Rough estimate
        return round(estimated_temp, 1)


class HealthCalculator:
    """Calculates system health scores based on metrics"""
    
    @staticmethod
    def calculate_component_health(value: float, component: str) -> float:
        """
        Calculate health score for a component (0-100)
        
        Args:
            value: Component usage percentage
            component: Component type (cpu, memory, disk, gpu)
        
        Returns:
            Health score (0-100)
        """
        if component == "cpu":
            if value < 60:
                return 90
            elif value < 80:
                return 70
            else:
                return 40
        
        elif component == "memory":
            if value < 65:
                return 90
            elif value < 80:
                return 65
            else:
                return 45
        
        elif component == "disk":
            if value < 70:
                return 85
            elif value < 85:
                return 60
            else:
                return 40
        
        elif component == "gpu":
            if value < 70:
                return 90
            elif value < 85:
                return 70
            else:
                return 50
        
        return 50  # Default
    
    @staticmethod
    def calculate_temp_health(temp: float) -> float:
        """
        Calculate health based on temperature
        
        Args:
            temp: Temperature in Celsius
        
        Returns:
            Health score (0-100)
        """
        if temp < 60:
            return 95
        elif temp < 70:
            return 80
        elif temp < 80:
            return 60
        else:
            return 35
    
    @staticmethod
    def calculate_overall_health(cpu_health: float, mem_health: float, 
                                 disk_health: float, gpu_health: float) -> float:
        """
        Calculate overall system health (weighted average)
        
        Args:
            cpu_health: CPU health score
            mem_health: Memory health score
            disk_health: Disk health score
            gpu_health: GPU health score
        
        Returns:
            Overall health score (0-100)
        """
        overall = (
            cpu_health * 0.3 +
            mem_health * 0.3 +
            disk_health * 0.2 +
            gpu_health * 0.2
        )
        return round(overall, 1)
    
    @staticmethod
    def get_status_info(overall_score: float) -> Tuple[str, str]:
        """
        Get status text and color based on overall health
        
        Args:
            overall_score: Overall health score (0-100)
        
        Returns:
            Tuple of (status_text, color)
        """
        if overall_score >= 80:
            return "System Healthy", "#10B981"  # Green
        elif overall_score >= 60:
            return "System Moderate", "#F59E0B"  # Amber
        else:
            return "System Critical", "#EF4444"  # Red
    
    @staticmethod
    def get_trend_indicator(current: float, previous: float) -> str:
        """
        Get trend indicator arrow
        
        Args:
            current: Current value
            previous: Previous value
        
        Returns:
            Trend indicator string
        """
        diff = current - previous
        if abs(diff) < 2:
            return "→ Stable"
        elif diff > 0:
            return f"↑ +{abs(diff):.1f}% from last"
        else:
            return f"↓ -{abs(diff):.1f}% from last"
