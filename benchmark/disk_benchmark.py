"""
Disk Benchmark Module
Tests disk performance through read/write operations
"""

import time
import os
import tempfile

class DiskBenchmark:
    """Disk performance benchmarking"""
    
    def __init__(self):
        self.results = {}
        self.test_file = None
    
    def run_sequential_write_test(self, size_mb=100):
        """Sequential disk write test"""
        chunk_size = 1024 * 1024  # 1MB chunks
        total_bytes = size_mb * chunk_size
        data = b'0' * chunk_size
        
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        
        start_time = time.time()
        
        bytes_written = 0
        while bytes_written < total_bytes:
            self.test_file.write(data)
            bytes_written += chunk_size
        
        self.test_file.flush()
        os.fsync(self.test_file.fileno())
        
        elapsed = time.time() - start_time
        speed_mbps = size_mb / elapsed
        
        self.results['sequential_write'] = {
            'time_seconds': elapsed,
            'speed_mbps': speed_mbps
        }
        return self.results['sequential_write']
    
    def run_sequential_read_test(self):
        """Sequential disk read test"""
        if not self.test_file:
            raise ValueError("Must run write test first")
        
        self.test_file.seek(0)
        chunk_size = 1024 * 1024
        
        start_time = time.time()
        
        bytes_read = 0
        while True:
            data = self.test_file.read(chunk_size)
            if not data:
                break
            bytes_read += len(data)
        
        elapsed = time.time() - start_time
        size_mb = bytes_read / (1024 * 1024)
        speed_mbps = size_mb / elapsed
        
        self.results['sequential_read'] = {
            'time_seconds': elapsed,
            'speed_mbps': speed_mbps
        }
        return self.results['sequential_read']
    
    def run_random_access_test(self, accesses=1000):
        """Random disk access test"""
        if not self.test_file:
            raise ValueError("Must run write test first")
        
        file_size = os.path.getsize(self.test_file.name)
        chunk_size = 4096  # 4KB chunks
        
        start_time = time.time()
        
        for _ in range(accesses):
            pos = (os.urandom(4)[0] % (file_size // chunk_size)) * chunk_size
            self.test_file.seek(pos)
            self.test_file.read(chunk_size)
        
        elapsed = time.time() - start_time
        iops = accesses / elapsed
        
        self.results['random_access'] = {
            'time_seconds': elapsed,
            'iops': iops
        }
        return self.results['random_access']
    
    def cleanup(self):
        """Clean up test files"""
        if self.test_file:
            self.test_file.close()
            try:
                os.unlink(self.test_file.name)
            except:
                pass
    
    def run_full_benchmark(self):
        """Run complete disk benchmark"""
        try:
            print("Running sequential write test...")
            self.run_sequential_write_test()
            
            print("Running sequential read test...")
            self.run_sequential_read_test()
            
            print("Running random access test...")
            self.run_random_access_test()
            
            return self.results
        finally:
            self.cleanup()
