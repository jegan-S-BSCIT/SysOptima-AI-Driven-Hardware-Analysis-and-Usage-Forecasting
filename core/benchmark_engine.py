"""
Benchmark Engine - Lightweight Safe Benchmarking
Uses non-stressful, quick benchmarks suitable for academic projects
"""

from benchmark.lightweight_benchmark import LightweightBenchmark


class BenchmarkEngine:
    """Runs lightweight benchmarks with progress tracking"""
    
    def __init__(self):
        self.benchmark = LightweightBenchmark()
        self.callback = None
    
    def set_callback(self, callback):
        """Set progress callback function"""
        self.callback = callback
    
    def run_cpu(self):
        """Run CPU benchmark only"""
        return self.benchmark.run_cpu_benchmark(self.callback)
    
    def run_memory(self):
        """Run RAM benchmark only"""
        return self.benchmark.run_ram_benchmark(self.callback)
    
    def run_disk(self):
        """Run disk benchmark only"""
        return self.benchmark.run_disk_benchmark(self.callback)
    
    def run_gpu(self):
        """Run GPU benchmark only"""
        return self.benchmark.run_gpu_benchmark(self.callback)
    
    def run_all(self):
        """Run all benchmarks with progress tracking"""
        return self.benchmark.run_all_benchmarks(self.callback)
    
    def cancel(self):
        """Cancel ongoing benchmark"""
        self.benchmark.cancel()
