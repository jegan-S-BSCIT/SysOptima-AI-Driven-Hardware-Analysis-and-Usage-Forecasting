"""
GPU Detection Module
Best-effort GPU detection across different platforms
"""

import platform

class GPUDetector:
    """Detects GPU information (best effort)"""
    
    def __init__(self):
        self.gpu_info = None
    
    def detect_gpu(self):
        """Detect GPU information using available methods"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                self.gpu_info = [{
                    'id': gpu.id,
                    'name': gpu.name,
                    'memory_total_mb': gpu.memoryTotal,
                    'memory_used_mb': gpu.memoryUsed,
                    'memory_free_mb': gpu.memoryFree,
                    'gpu_load': gpu.load * 100,
                    'temperature': gpu.temperature
                } for gpu in gpus]
                return self.gpu_info
        except Exception as e:
            pass
        
        # Fallback for Windows
        if platform.system() == "Windows":
            try:
                return self._detect_gpu_windows()
            except:
                pass
        
        # No GPU detected
        self.gpu_info = [{'name': 'No GPU detected or unsupported', 'available': False}]
        return self.gpu_info
    
    def _detect_gpu_windows(self):
        """Windows-specific GPU detection using WMI"""
        try:
            import wmi
            w = wmi.WMI()
            gpus = []
            for gpu in w.Win32_VideoController():
                gpus.append({
                    'name': gpu.Name,
                    'adapter_ram_mb': int(gpu.AdapterRAM) / (1024**2) if gpu.AdapterRAM else 0,
                    'driver_version': gpu.DriverVersion,
                    'status': gpu.Status
                })
            return gpus if gpus else None
        except Exception as e:
            return None
