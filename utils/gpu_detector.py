"""
GPU Detection Utility
Handles GPU information retrieval with multiple fallback methods
"""

import subprocess
import GPUtil


def get_gpu_info():
    """
    Retrieve GPU information using multiple methods.
    
    Returns:
        dict: GPU information containing name, vram_mb, and status
    """
    # 1. Try GPUtil first (clean method)
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            return {
                "name": gpu.name,
                "vram_mb": gpu.memoryTotal,
                "status": "Active (GPUtil)"
            }
    except Exception:
        pass

    # 2. Fallback to nvidia-smi (Windows reliable method)
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            encoding="utf-8"
        )
        name, memory = result.strip().split(",")
        return {
            "name": name.strip(),
            "vram_mb": int(memory.replace("MiB", "").strip()),
            "status": "Active (nvidia-smi)"
        }
    except Exception:
        return {
            "name": "NVIDIA GPU not accessible",
            "vram_mb": "N/A",
            "status": "Not Detected"
        }
