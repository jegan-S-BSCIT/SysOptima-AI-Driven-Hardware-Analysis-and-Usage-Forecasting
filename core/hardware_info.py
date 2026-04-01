"""
Real hardware detection module for SysOptima
Provides actual system information without hardcoded values
"""

import platform
import psutil
try:
    import cpuinfo
except ImportError:
    cpuinfo = None
import GPUtil


def get_cpu_info():
    """
    Detect actual CPU information from the system
    
    Returns:
        dict: CPU details including name, cores, threads, frequencies
    """
    try:
        # Try py-cpuinfo first for detailed CPU name
        if cpuinfo:
            info = cpuinfo.get_cpu_info()
            cpu_name = info.get("brand_raw", platform.processor())
        else:
            cpu_name = platform.processor()
        
        # Get core counts
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        
        # Get frequency information
        freq = psutil.cpu_freq()
        if freq:
            base_freq = round(freq.min / 1000, 2) if freq.min > 0 else round(freq.current / 1000, 2)
            max_freq = round(freq.max / 1000, 2) if freq.max > 0 else round(freq.current / 1000, 2)
        else:
            base_freq = 0.0
            max_freq = 0.0
        
        return {
            "name": cpu_name or "Unknown Processor",
            "physical_cores": physical_cores or 0,
            "logical_cores": logical_cores or 0,
            "base_freq": base_freq,
            "max_freq": max_freq
        }
    except Exception as e:
        print(f"CPU detection error: {e}")
        return {
            "name": "Detection Failed",
            "physical_cores": 0,
            "logical_cores": 0,
            "base_freq": 0.0,
            "max_freq": 0.0
        }


def get_memory_info():
    """
    Detect actual memory information from the system
    
    Returns:
        dict: Memory details including total, available, used
    
    Note: RAM type (DDR4/DDR5) cannot be reliably detected using Python.
    This is a known limitation of OS-level APIs.
    """
    try:
        mem = psutil.virtual_memory()
        
        return {
            "total_gb": round(mem.total / (1024**3), 1),
            "available_gb": round(mem.available / (1024**3), 1),
            "used_gb": round(mem.used / (1024**3), 1),
            "percent": mem.percent,
            "type": "Unknown (OS limitation)"  # Cannot detect DDR type via Python
        }
    except Exception as e:
        print(f"Memory detection error: {e}")
        return {
            "total_gb": 0.0,
            "available_gb": 0.0,
            "used_gb": 0.0,
            "percent": 0.0,
            "type": "Detection Failed"
        }


def get_storage_info():
    """
    Detect actual storage information from the system
    
    Returns:
        dict: Storage details for the primary disk
    """
    try:
        # Use C: for Windows, / for Unix-like systems
        disk_path = 'C:' if platform.system() == 'Windows' else '/'
        disk = psutil.disk_usage(disk_path)
        
        return {
            "total_gb": round(disk.total / (1024**3), 1),
            "used_gb": round(disk.used / (1024**3), 1),
            "free_gb": round(disk.free / (1024**3), 1),
            "percent": disk.percent,
            "path": disk_path
        }
    except Exception as e:
        print(f"Storage detection error: {e}")
        return {
            "total_gb": 0.0,
            "used_gb": 0.0,
            "free_gb": 0.0,
            "percent": 0.0,
            "path": "Unknown"
        }


def get_gpu_info():
    """
    Detect GPU information (best effort)
    
    Returns:
        dict: GPU details or indication if no dedicated GPU found
    """
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {
                "name": "No dedicated GPU detected",
                "memory_total_mb": 0,
                "driver": "N/A",
                "available": False
            }
        
        gpu = gpus[0]  # Use first GPU
        return {
            "name": gpu.name,
            "memory_total_mb": gpu.memoryTotal,
            "driver": gpu.driver,
            "available": True
        }
    except Exception as e:
        print(f"GPU detection error: {e}")
        return {
            "name": "Detection Failed",
            "memory_total_mb": 0,
            "driver": "N/A",
            "available": False
        }


def get_os_info():
    """
    Detect operating system information
    
    Returns:
        dict: OS details including name, version, architecture
    """
    try:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "platform": platform.platform()
        }
    except Exception as e:
        print(f"OS detection error: {e}")
        return {
            "system": "Unknown",
            "release": "Unknown",
            "version": "Unknown",
            "architecture": "Unknown",
            "platform": "Unknown"
        }


def get_all_hardware_info():
    """
    Get complete hardware information in one call
    
    Returns:
        dict: Complete hardware profile
    """
    return {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "storage": get_storage_info(),
        "gpu": get_gpu_info(),
        "os": get_os_info()
    }
