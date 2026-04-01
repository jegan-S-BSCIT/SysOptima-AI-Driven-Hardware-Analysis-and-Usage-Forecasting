"""
AI System API Integration Layer
================================
Provides local system data APIs for the AI Assistant:
- /metrics: Real-time system metrics (CPU, RAM, GPU, Disk)
- /hardware: Hardware information and specifications
- /benchmark: Latest benchmark results
- /gaming: Gaming performance assessment

This module bridges the AI with actual system data.
"""

import psutil
import json
from typing import Dict, Any, List
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.hardware_info import HardwareInfo
    HAS_HARDWARE_INFO = True
except:
    HAS_HARDWARE_INFO = False


class AISystemAPI:
    """Provides APIs for AI to access system data"""
    
    def __init__(self):
        """Initialize API layer"""
        self.hardware = HardwareInfo() if HAS_HARDWARE_INFO else None
        self.last_benchmark = None
    
    # ======================================================================
    # /metrics API - Real-time system metrics
    # ======================================================================
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        GET /api/metrics
        Returns real-time system performance metrics
        """
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # GPU info if available
            gpu_info = self._get_gpu_info()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu,
                    'cores': cpu_count,
                    'logical_cores': cpu_count_logical,
                    'frequency_ghz': psutil.cpu_freq().current / 1000.0 if psutil.cpu_freq() else None,
                    'status': self._classify_cpu_usage(cpu)
                },
                'ram': {
                    'percent': ram.percent,
                    'used_gb': round(ram.used / (1024**3), 2),
                    'total_gb': round(ram.total / (1024**3), 2),
                    'available_gb': round(ram.available / (1024**3), 2),
                    'status': self._classify_ram_usage(ram.percent)
                },
                'disk': {
                    'percent': disk.percent,
                    'used_gb': round(disk.used / (1024**3), 2),
                    'total_gb': round(disk.total / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'status': self._classify_disk_usage(disk.percent)
                },
                'gpu': gpu_info,
                'processes_running': len(psutil.pids()),
                'system_health': self._calculate_system_health(cpu, ram.percent, disk.percent)
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    # ======================================================================
    # /hardware API - Hardware information and specifications
    # ======================================================================
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """
        GET /api/hardware
        Returns detailed hardware information
        """
        try:
            if not self.hardware:
                return {'error': 'Hardware info not available'}
            
            hw_info = self.hardware.get_full_info()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'model': hw_info.get('cpu_model', 'Unknown'),
                    'cores': hw_info.get('cpu_cores', 'Unknown'),
                    'threads': hw_info.get('cpu_threads', 'Unknown'),
                    'frequency_ghz': hw_info.get('cpu_frequency', 'Unknown')
                },
                'ram': {
                    'total_gb': hw_info.get('ram_total', 'Unknown'),
                    'type': hw_info.get('ram_type', 'Unknown')
                },
                'gpu': {
                    'name': hw_info.get('gpu_name', 'Unknown'),
                    'vram_gb': hw_info.get('gpu_vram', 'Unknown'),
                    'driver_version': hw_info.get('gpu_driver', 'Unknown')
                },
                'disk': {
                    'capacity_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                    'type': self._detect_disk_type()
                },
                'motherboard': hw_info.get('motherboard', 'Unknown'),
                'os': {
                    'name': hw_info.get('os_name', 'Unknown'),
                    'version': hw_info.get('os_version', 'Unknown')
                }
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    # ======================================================================
    # /benchmark API - Latest benchmark results
    # ======================================================================
    
    def get_benchmark_results(self) -> Dict[str, Any]:
        """
        GET /api/benchmark
        Returns latest benchmark results if available
        """
        if not self.last_benchmark:
            return {
                'available': False,
                'message': 'No benchmark data available. Run a benchmark first.',
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'available': True,
            'timestamp': self.last_benchmark.get('timestamp', datetime.now().isoformat()),
            'results': self.last_benchmark
        }
    
    def set_benchmark_results(self, results: Dict[str, Any]):
        """Store latest benchmark results"""
        self.last_benchmark = results
        self.last_benchmark['timestamp'] = datetime.now().isoformat()
    
    # ======================================================================
    # /gaming API - Gaming performance assessment
    # ======================================================================
    
    def assess_gaming_performance(self) -> Dict[str, Any]:
        """
        GET /api/gaming
        Returns gaming performance assessment based on hardware
        """
        try:
            metrics = self.get_metrics()
            hardware = self.get_hardware_info()
            
            gpu_name = hardware.get('gpu', {}).get('name', '').lower()
            gpu_vram = hardware.get('gpu', {}).get('vram_gb', 0)
            cpu_cores = metrics.get('cpu', {}).get('cores', 1)
            ram_gb = metrics.get('ram', {}).get('total_gb', 0)
            
            # Gaming tier classification
            gaming_tier = self._classify_gaming_tier(gpu_name, gpu_vram, cpu_cores, ram_gb)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'tier': gaming_tier['tier'],
                'description': gaming_tier['description'],
                'estimated_fps_1080p': gaming_tier['fps_1080p'],
                'estimated_fps_1440p': gaming_tier['fps_1440p'],
                'estimated_fps_4k': gaming_tier['fps_4k'],
                'vram_sufficient': gpu_vram >= gaming_tier['recommended_vram'],
                'cpu_cores_sufficient': cpu_cores >= gaming_tier['recommended_cores'],
                'ram_sufficient': ram_gb >= gaming_tier['recommended_ram'],
                'recommendations': gaming_tier['recommendations']
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    # ======================================================================
    # Helper Methods - Classification and Detection
    # ======================================================================
    
    def _classify_cpu_usage(self, percent: float) -> str:
        """Classify CPU usage level"""
        if percent < 20:
            return "Idle"
        elif percent < 50:
            return "Light"
        elif percent < 80:
            return "Moderate"
        else:
            return "Heavy"
    
    def _classify_ram_usage(self, percent: float) -> str:
        """Classify RAM usage level"""
        if percent < 50:
            return "Healthy"
        elif percent < 75:
            return "Moderate"
        elif percent < 90:
            return "High"
        else:
            return "Critical"
    
    def _classify_disk_usage(self, percent: float) -> str:
        """Classify disk usage level"""
        if percent < 50:
            return "Healthy"
        elif percent < 80:
            return "Moderate"
        elif percent < 95:
            return "High"
        else:
            return "Critical"
    
    def _calculate_system_health(self, cpu: float, ram: float, disk: float) -> str:
        """Calculate overall system health"""
        avg = (cpu + ram + disk) / 3
        if avg < 50:
            return "Excellent"
        elif avg < 65:
            return "Good"
        elif avg < 80:
            return "Fair"
        else:
            return "Poor"
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.name,
                    'vram_mb': gpu.memoryTotal,
                    'vram_gb': round(gpu.memoryTotal / 1024, 1),
                    'vram_used_mb': gpu.memoryUsed,
                    'vram_used_percent': round((gpu.memoryUsed / gpu.memoryTotal) * 100, 1),
                    'status': 'Available'
                }
        except:
            pass
        
        return {
            'name': 'Not detected',
            'vram_gb': 0,
            'status': 'Unavailable'
        }
    
    def _detect_disk_type(self) -> str:
        """Attempt to detect if disk is SSD or HDD"""
        try:
            # Simple heuristic: check for SSD-like naming
            import platform
            if platform.system() == 'Windows':
                import subprocess
                result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], 
                                      capture_output=True, text=True)
                if 'SSD' in result.stdout:
                    return 'SSD'
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _classify_gaming_tier(self, gpu_name: str, gpu_vram: float, 
                             cpu_cores: int, ram_gb: float) -> Dict[str, Any]:
        """Classify gaming performance tier"""
        
        # Define GPU tiers
        if any(x in gpu_name for x in ['RTX 4090', 'RTX 3090']):
            base_tier = 'Ultra'
            base_fps_1080p = 240
            base_fps_1440p = 165
            base_fps_4k = 60
        elif any(x in gpu_name for x in ['RTX 4080', 'RTX 4070', 'RTX 3080', 'RTX 3070']):
            base_tier = 'High'
            base_fps_1080p = 165
            base_fps_1440p = 120
            base_fps_4k = 60
        elif any(x in gpu_name for x in ['RTX 4060', 'RTX 3060', 'GTX 1660']):
            base_tier = 'Medium'
            base_fps_1080p = 100
            base_fps_1440p = 60
            base_fps_4k = 30
        else:
            base_tier = 'Entry'
            base_fps_1080p = 60
            base_fps_1440p = 30
            base_fps_4k = 0
        
        # Build recommendations
        recommendations = []
        if gpu_vram < 4:
            recommendations.append("Upgrade GPU VRAM to 6GB+ for better gaming")
        if cpu_cores < 4:
            recommendations.append("CPU cores below recommended for modern games")
        if ram_gb < 16:
            recommendations.append("RAM upgrade to 16GB recommended for smoother gaming")
        
        if not recommendations:
            recommendations.append("System is well-suited for gaming")
        
        return {
            'tier': base_tier,
            'description': f"{base_tier}-tier gaming capable",
            'fps_1080p': base_fps_1080p,
            'fps_1440p': base_fps_1440p,
            'fps_4k': base_fps_4k,
            'recommended_vram': 6,
            'recommended_cores': 4,
            'recommended_ram': 16,
            'recommendations': recommendations
        }


# Singleton instance
_api_instance = None

def get_ai_api() -> AISystemAPI:
    """Get or create singleton API instance"""
    global _api_instance
    if _api_instance is None:
        _api_instance = AISystemAPI()
    return _api_instance
