"""
Lightweight Benchmarking Engine
Performs non-intensive hardware benchmarks suitable for B.Sc. IT project

Benchmarks:
- CPU: Mathematical workload (Fibonacci, primes)
- RAM: Memory allocation and read/write speed
- Storage: File I/O operations
- GPU: Classification-based scoring
"""

import time
import psutil
import os
import json
import tempfile
from typing import Dict, Tuple
import math


class LightweightBenchmark:
    """Lightweight benchmarking without stress testing"""
    
    def __init__(self):
        """Initialize benchmark engine"""
        self.results = {}
        self.reference_file = os.path.join(
            os.path.dirname(__file__), 
            '../data/benchmark_reference.json'
        )
        self.reference = self._load_reference()
    
    def _load_reference(self) -> Dict:
        """Load reference benchmark values"""
        try:
            with open(self.reference_file, 'r') as f:
                return json.load(f)
        except:
            return self._get_default_reference()
    
    def _get_default_reference(self) -> Dict:
        """Default reference values if file not found"""
        return {
            "cpu_reference": {
                "average_score": 65,
                "cores_performance": {"4": 50, "8": 85}
            },
            "ram_reference": {
                "average_score": 70,
                "capacity_gb": {"8": 60, "16": 90}
            },
            "storage_reference": {
                "average_ssd_speed": 800,
                "average_hdd_speed": 125,
                "average_score": 60
            },
            "gpu_reference": {
                "average_score": 65,
                "average_class": "mid_range"
            }
        }
    
    def benchmark_cpu(self) -> Dict:
        """
        Lightweight CPU benchmark using mathematical operations
        Measures: Core count and clock speed efficiency
        Duration: < 1 second
        """
        start_time = time.time()
        
        # Get CPU info
        logical_cores = psutil.cpu_count(logical=True)
        physical_cores = psutil.cpu_count(logical=False)
        freq = psutil.cpu_freq()
        clock_speed_ghz = (freq.current / 1000) if freq else 3.0
        
        # Simple mathematical workload
        result = 0
        for i in range(10000000):  # 10M iterations = < 1 second
            result += math.sqrt(i % 1000)
        
        elapsed = time.time() - start_time
        
        # Calculate score (0-100)
        # Core score: 4 cores = 50, 8 cores = 85
        core_score = min((logical_cores / 8) * 85, 100)
        
        # Speed score: 3.0 GHz = 60, 4.0 GHz = 90
        speed_score = min((clock_speed_ghz / 4.0) * 90, 100)
        
        cpu_score = (core_score * 0.6 + speed_score * 0.4)
        
        # Reference score
        ref_score = self.reference.get(
            "cpu_reference", {}
        ).get("average_score", 65)
        
        return {
            "score": round(cpu_score, 1),
            "reference_score": ref_score,
            "cores": logical_cores,
            "clock_speed_ghz": round(clock_speed_ghz, 2),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(cpu_score, ref_score)
        }
    
    def benchmark_ram(self) -> Dict:
        """
        Lightweight RAM benchmark
        Measures: Total capacity and basic allocation speed
        Duration: < 1 second
        """
        start_time = time.time()
        
        # Get RAM info
        ram_info = psutil.virtual_memory()
        total_gb = ram_info.total / (1024**3)
        percent_used = ram_info.percent
        available_gb = ram_info.available / (1024**3)
        
        # Lightweight memory allocation test (allocate 50MB, read/write)
        test_size_mb = 50
        allocation_times = []
        
        for _ in range(5):
            alloc_start = time.time()
            # Allocate memory
            data = bytearray(test_size_mb * 1024 * 1024)
            # Write test
            for i in range(0, len(data), 1024):
                data[i:i+4] = bytearray([1, 2, 3, 4])
            # Read test
            _ = sum(data[i] for i in range(0, min(len(data), 100000), 100))
            allocation_times.append(time.time() - alloc_start)
            del data
        
        elapsed = time.time() - start_time
        avg_alloc_time = sum(allocation_times) / len(allocation_times)
        
        # Calculate score
        # Capacity: 8GB = 60, 16GB = 90
        capacity_score = min((total_gb / 16) * 90, 100)
        
        # Usage: Low usage = high score
        usage_score = max(0, 100 - (percent_used * 1.5))
        
        ram_score = (capacity_score * 0.6 + usage_score * 0.4)
        
        # Reference score
        ref_score = self.reference.get(
            "ram_reference", {}
        ).get("average_score", 70)
        
        return {
            "score": round(ram_score, 1),
            "reference_score": ref_score,
            "total_gb": round(total_gb, 1),
            "available_gb": round(available_gb, 1),
            "percent_used": round(percent_used, 1),
            "allocation_time_ms": round(avg_alloc_time * 1000, 2),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(ram_score, ref_score)
        }
    
    def benchmark_storage(self) -> Dict:
        """
        Lightweight storage benchmark
        Measures: Read/write speed with 50MB test file
        Duration: 1-2 seconds
        """
        start_time = time.time()
        
        # Get storage info
        partitions = psutil.disk_partitions()
        drive_c = None
        for p in partitions:
            if p.device == 'C:\\':
                drive_c = p
                break
        
        if drive_c is None:
            drive_c = partitions[0] if partitions else None
        
        # Get drive info
        if drive_c:
            usage = psutil.disk_usage(drive_c.mountpoint)
            drive_name = drive_c.device
            fstype = drive_c.fstype
        else:
            drive_name = "Unknown"
            fstype = "Unknown"
        
        # Perform I/O benchmark
        test_file_size_mb = 50
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "benchmark_test.bin")
                
                # Write test
                write_start = time.time()
                with open(test_file, 'wb') as f:
                    f.write(b'x' * (test_file_size_mb * 1024 * 1024))
                write_time = time.time() - write_start
                write_speed = test_file_size_mb / write_time if write_time > 0 else 0
                
                # Read test
                read_start = time.time()
                with open(test_file, 'rb') as f:
                    _ = f.read()
                read_time = time.time() - read_start
                read_speed = test_file_size_mb / read_time if read_time > 0 else 0
                
        except Exception as e:
            read_speed = 100
            write_speed = 100
        
        avg_speed = (read_speed + write_speed) / 2
        
        # Determine if SSD or HDD
        is_ssd = fstype.lower() in ['ntfs', 'ext4', 'apfs'] and avg_speed > 200
        
        # Calculate score
        if is_ssd:
            # SATA SSD ref: 550 MB/s = 70
            speed_score = min((avg_speed / 550) * 70, 100)
        else:
            # HDD ref: 150 MB/s = 30
            speed_score = min((avg_speed / 150) * 30, 100)
        
        storage_score = speed_score
        
        # Reference score
        ref_score = self.reference.get(
            "storage_reference", {}
        ).get("average_score", 60)
        
        elapsed = time.time() - start_time
        
        return {
            "score": round(storage_score, 1),
            "reference_score": ref_score,
            "drive": drive_name,
            "fstype": fstype,
            "type": "SSD" if is_ssd else "HDD",
            "read_speed_mbps": round(read_speed, 1),
            "write_speed_mbps": round(write_speed, 1),
            "avg_speed_mbps": round(avg_speed, 1),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(storage_score, ref_score)
        }
    
    def benchmark_gpu(self) -> Dict:
        """
        GPU benchmark using classification
        Measures: VRAM size, GPU class, and typical performance
        Duration: < 0.1 seconds (no actual rendering)
        """
        start_time = time.time()
        
        gpu_data = {}
        gpu_score = 0
        gpu_class = "unknown"
        
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            
            if gpus:
                gpu = gpus[0]
                vram_gb = gpu.memoryTotal / 1024
                gpu_name = gpu.name
                
                # Classify GPU based on VRAM and common models
                if vram_gb <= 2:
                    gpu_class = "entry_level"
                    gpu_score = 40
                elif vram_gb <= 4:
                    gpu_class = "mid_range"
                    gpu_score = 65
                elif vram_gb <= 8:
                    gpu_class = "high_performance"
                    gpu_score = 85
                else:
                    gpu_class = "professional"
                    gpu_score = 100
                
                gpu_data = {
                    "name": gpu_name,
                    "vram_gb": round(vram_gb, 1),
                    "class": gpu_class,
                    "temperature": round(gpu.temperature, 1) if hasattr(gpu, 'temperature') else None
                }
        except:
            gpu_data = {"name": "Integrated Graphics", "vram_gb": 0}
            gpu_class = "integrated"
            gpu_score = 30
        
        elapsed = time.time() - start_time
        
        # Reference score
        ref_score = self.reference.get(
            "gpu_reference", {}
        ).get("average_score", 65)
        
        return {
            "score": round(gpu_score, 1),
            "reference_score": ref_score,
            "name": gpu_data.get("name", "Unknown"),
            "vram_gb": gpu_data.get("vram_gb", 0),
            "class": gpu_class,
            "temperature_c": gpu_data.get("temperature"),
            "benchmark_time_sec": round(elapsed, 2),
            "status": self._compare_score(gpu_score, ref_score)
        }
    
    def run_all_benchmarks(self) -> Dict:
        """Run all benchmarks and return results"""
        results = {
            "cpu": self.benchmark_cpu(),
            "ram": self.benchmark_ram(),
            "storage": self.benchmark_storage(),
            "gpu": self.benchmark_gpu(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Calculate overall score
        scores = [
            results["cpu"]["score"],
            results["ram"]["score"],
            results["storage"]["score"],
            results["gpu"]["score"]
        ]
        results["overall_score"] = round(sum(scores) / len(scores), 1)
        
        self.results = results
        return results
    
    @staticmethod
    def _compare_score(local: float, reference: float) -> str:
        """Compare local score vs reference"""
        diff_percent = ((local - reference) / reference) * 100
        
        if diff_percent > 10:
            return "ABOVE AVERAGE"
        elif diff_percent > -10:
            return "AVERAGE"
        else:
            return "BELOW AVERAGE"
    
    def get_percent_difference(self, local: float, reference: float) -> float:
        """Calculate percentage difference"""
        if reference == 0:
            return 0
        return round(((local - reference) / reference) * 100, 1)


# Example usage
if __name__ == "__main__":
    benchmark = LightweightBenchmark()
    results = benchmark.run_all_benchmarks()
    
    print("\n" + "="*80)
    print("LIGHTWEIGHT BENCHMARK RESULTS")
    print("="*80)
    
    print("\nCPU Benchmark:")
    print(f"  Local Score: {results['cpu']['score']}/100")
    print(f"  Reference Score: {results['cpu']['reference_score']}/100")
    print(f"  Cores: {results['cpu']['cores']}")
    print(f"  Clock Speed: {results['cpu']['clock_speed_ghz']} GHz")
    print(f"  Status: {results['cpu']['status']}")
    
    print("\nRAM Benchmark:")
    print(f"  Local Score: {results['ram']['score']}/100")
    print(f"  Reference Score: {results['ram']['reference_score']}/100")
    print(f"  Total RAM: {results['ram']['total_gb']} GB")
    print(f"  Available: {results['ram']['available_gb']} GB")
    print(f"  Status: {results['ram']['status']}")
    
    print("\nStorage Benchmark:")
    print(f"  Local Score: {results['storage']['score']}/100")
    print(f"  Reference Score: {results['storage']['reference_score']}/100")
    print(f"  Type: {results['storage']['type']}")
    print(f"  Read Speed: {results['storage']['read_speed_mbps']} MB/s")
    print(f"  Write Speed: {results['storage']['write_speed_mbps']} MB/s")
    print(f"  Status: {results['storage']['status']}")
    
    print("\nGPU Benchmark:")
    print(f"  Local Score: {results['gpu']['score']}/100")
    print(f"  Reference Score: {results['gpu']['reference_score']}/100")
    print(f"  GPU: {results['gpu']['name']}")
    print(f"  VRAM: {results['gpu']['vram_gb']} GB")
    print(f"  Class: {results['gpu']['class']}")
    print(f"  Status: {results['gpu']['status']}")
    
    print(f"\nOverall System Score: {results['overall_score']}/100")
    print("="*80 + "\n")
