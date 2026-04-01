"""
CPU Benchmark Module
Tests CPU performance through computational tasks
"""

import time
import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

class CPUBenchmark:
    """CPU performance benchmarking"""
    
    def __init__(self):
        self.results = {}
    
    def run_single_thread_test(self, iterations=1000000):
        """Single-threaded CPU test"""
        start_time = time.time()
        
        result = 0
        for i in range(iterations):
            result += math.sqrt(i) * math.sin(i)
        
        elapsed = time.time() - start_time
        score = iterations / elapsed
        
        self.results['single_thread'] = {
            'time_seconds': elapsed,
            'score': score
        }
        return self.results['single_thread']
    
    def _worker_task(self, iterations):
        """Worker task for multi-threaded test"""
        result = 0
        for i in range(iterations):
            result += math.sqrt(i) * math.sin(i)
        return result
    
    def run_multi_thread_test(self, iterations=1000000):
        """Multi-threaded CPU test"""
        cpu_count = multiprocessing.cpu_count()
        iterations_per_thread = iterations // cpu_count
        
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            futures = [executor.submit(self._worker_task, iterations_per_thread) 
                      for _ in range(cpu_count)]
            results = [f.result() for f in futures]
        
        elapsed = time.time() - start_time
        score = iterations / elapsed
        
        self.results['multi_thread'] = {
            'time_seconds': elapsed,
            'score': score,
            'threads_used': cpu_count
        }
        return self.results['multi_thread']
    
    def run_full_benchmark(self):
        """Run complete CPU benchmark"""
        print("Running single-thread test...")
        self.run_single_thread_test()
        
        print("Running multi-thread test...")
        self.run_multi_thread_test()
        
        return self.results
