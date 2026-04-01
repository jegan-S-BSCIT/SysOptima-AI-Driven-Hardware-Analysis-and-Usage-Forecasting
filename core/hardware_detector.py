"""
Hardware Detection Module
Provides CPU, RAM, and Disk snapshots using psutil and platform.
"""

import os
import platform
import subprocess
import psutil


class HardwareDetector:
    """Detects and reports core system hardware information"""

    def __init__(self):
        self.cpu_info = None
        self.ram_info = None
        self.disk_info = None
        self.gpu_info = None
        self.cached_gpu_info = None

    def detect_cpu(self):
        """Detect CPU name, core counts, and current usage percentage"""
        name = platform.processor() or platform.uname().processor or "Unknown CPU"
        self.cpu_info = {
            "name": name,
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_threads": psutil.cpu_count(logical=True) or 0,
            "usage_percent": psutil.cpu_percent(interval=0),
        }
        return self.cpu_info

    def detect_ram(self):
        """Detect total, used, and percentage RAM usage (in GB)"""
        memory = psutil.virtual_memory()
        self.ram_info = {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "usage_percent": memory.percent,
        }
        return self.ram_info

    def detect_disk(self):
        """Detect root disk total, used, and percentage usage (in GB)"""
        root_path = os.path.abspath(os.sep)
        usage = psutil.disk_usage(root_path)
        self.disk_info = {
            "mountpoint": root_path,
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "usage_percent": usage.percent,
        }
        return self.disk_info

    def detect_gpu(self):
        """
        Detect GPU efficiently. Caches result if slow methods (WMIC) are used.
        """
        # Return cached result if available (for static/slow methods)
        if self.cached_gpu_info:
            return self.cached_gpu_info

        name = "Unknown GPU"
        total_mb = 0
        used_mb = 0
        status = "Not Detected"

        # Step 1: Try GPUtil first (Fast, supports usage)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                self.gpu_info = {
                    "name": gpu.name if gpu.name else "Unknown GPU",
                    "memory_total_mb": round(gpu.memoryTotal) if gpu.memoryTotal else 0,
                    "memory_used_mb": round(gpu.memoryUsed) if gpu.memoryUsed else 0,
                    "status": "Active (GPUtil)",
                }
                return self.gpu_info
        except (ImportError, Exception):
            pass

        # Step 2: Fallback to nvidia-smi (Medium speed, supports usage)
        try:
            result = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader,nounits"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            )
            parts = result.strip().split(",")
            if len(parts) >= 2:
                name = parts[0].strip()
                try:
                    total_mb = int(float(parts[1].strip()))
                except (ValueError, IndexError): total_mb = 0
                try:
                    used_mb = int(float(parts[2].strip())) if len(parts) >= 3 else 0
                except (ValueError, IndexError): used_mb = 0
                
                self.gpu_info = {
                    "name": name,
                    "memory_total_mb": total_mb,
                    "memory_used_mb": used_mb,
                    "status": "Active (nvidia-smi)",
                }
                return self.gpu_info
        except (FileNotFoundError, subprocess.CalledProcessError, Exception):
            pass

        # Step 3: Last resort - WMIC (Very Slow, Static info only)
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["wmic", "path", "win32_videocontroller", "get", "Name,AdapterRAM", "/format:list"],
                    capture_output=True, text=True, check=True
                )
                lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
                current = {}
                for ln in lines:
                    if ln.startswith("Name="):
                        current["name"] = ln.split("=", 1)[1].strip()
                    elif ln.startswith("AdapterRAM="):
                        try:
                            current["total"] = int(ln.split("=", 1)[1].strip()) / (1024 ** 2)
                        except ValueError: pass
                    
                    if "name" in current:
                        name = current["name"]
                        total_mb = current.get("total", 0)
                        status = "Active (WMIC)"
                        break # Take first GPU
                
                # Cache this result since it's slow and static
                self.cached_gpu_info = {
                    "name": name,
                    "memory_total_mb": round(total_mb, 0),
                    "memory_used_mb": 0, # WMIC doesn't give usage
                    "status": status,
                }
                self.gpu_info = self.cached_gpu_info
                return self.gpu_info
            except Exception:
                pass

        self.gpu_info = {
            "name": name,
            "memory_total_mb": round(total_mb, 0),
            "memory_used_mb": used_mb,
            "status": status,
        }
        return self.gpu_info

    def detect_all(self):
        """Detect CPU, RAM, and Disk information in a single call"""
        return {
            "cpu": self.detect_cpu(),
            "ram": self.detect_ram(),
            "disk": self.detect_disk(),
            "gpu": self.detect_gpu(),
        }
