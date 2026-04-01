"""
Memory Benchmark Module
Tests RAM performance through read/write operations
"""

import time
import numpy as np

class MemoryBenchmark:
    """RAM performance benchmarking"""
    
    def __init__(self):
        self.results = {}
    
    def run_sequential_read_test(self, size_mb=100):
        """Sequential memory read test"""
        size = size_mb * 1024 * 1024 // 8  # Convert to number of doubles
        data = np.arange(size, dtype=np.float64)
        
        start_time = time.time()
        
        # Sequential read
        total = np.sum(data)
        
        elapsed = time.time() - start_time
        bandwidth_mbps = size_mb / elapsed
        
        self.results['sequential_read'] = {
            'time_seconds': elapsed,
            'bandwidth_mbps': bandwidth_mbps
        }
        return self.results['sequential_read']
    
    def run_sequential_write_test(self, size_mb=100):
        """Sequential memory write test"""
        size = size_mb * 1024 * 1024 // 8
        
        start_time = time.time()
        
        # Sequential write
        data = np.zeros(size, dtype=np.float64)
        data[:] = 1.0
        
        elapsed = time.time() - start_time
        bandwidth_mbps = size_mb / elapsed
        
        self.results['sequential_write'] = {
            'time_seconds': elapsed,
            'bandwidth_mbps': bandwidth_mbps
        }
        return self.results['sequential_write']
    
    def run_random_access_test(self, size_mb=100, accesses=100000):
        """Random memory access test"""
        size = size_mb * 1024 * 1024 // 8
        data = np.arange(size, dtype=np.float64)
        
        # Generate random indices
        indices = np.random.randint(0, size, accesses)
        
        start_time = time.time()
        
        # Random access
        total = 0
        for idx in indices:
            total += data[idx]
        
        elapsed = time.time() - start_time
        accesses_per_second = accesses / elapsed
        
        self.results['random_access'] = {
            'time_seconds': elapsed,
            'accesses_per_second': accesses_per_second
        }
        return self.results['random_access']
    
    def run_full_benchmark(self):
        """Run complete memory benchmark"""
        print("Running sequential read test...")
        self.run_sequential_read_test()
        
        print("Running sequential write test...")
        self.run_sequential_write_test()
        
        print("Running random access test...")
        self.run_random_access_test()
        
        return self.results

def main():
    bench = MemoryBenchmark()
    results = bench.run_full_benchmark()
    print("\nMemory Benchmark Results:")
    for test, metrics in results.items():
        print(f"  {test}:")
        for k, v in metrics.items():
            print(f"    {k}: {v:.2f}")
    return results

if __name__ == "__main__":
    main()
