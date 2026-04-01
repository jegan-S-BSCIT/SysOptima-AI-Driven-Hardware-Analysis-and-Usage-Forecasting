"""
Lightweight Benchmark Engine - Safe & Non-Stressful
Designed for academic project and safe system evaluation
"""

import time
import math
import os
import tempfile
import psutil
from typing import Dict, Any


class LightweightBenchmark:
    """Lightweight benchmark system - safe, quick, and non-stressful"""
    
    def __init__(self):
        self.results = {}
        self.cancelled = False
    
    def cancel(self):
        """Allow user to cancel benchmark"""
        self.cancelled = True
    
    # ========== CPU BENCHMARK ==========
    def run_cpu_benchmark(self, callback=None) -> Dict[str, Any]:
        """
        Lightweight CPU benchmark
        - Short duration (2-3 seconds total)
        - Controlled workload
        - Single-threaded measurement
        - Returns 0-100 score
        """
        if self.cancelled:
            return {}
        
        try:
            callback and callback("Starting CPU benchmark...")
            
            # Single-threaded CPU test (2 seconds)
            iterations = 100_000  # Reduced from 1M for safety
            start_time = time.time()
            result = 0
            
            for i in range(iterations):
                if self.cancelled:
                    return {}
                result += math.sqrt(i % 1000) * math.sin(i % 360)
            
            cpu_elapsed = time.time() - start_time
            cpu_score = self._normalize_cpu_score(cpu_elapsed, iterations)
            
            callback and callback(f"CPU benchmark: {cpu_elapsed:.2f}s")
            
            self.results['cpu'] = {
                'score': cpu_score,
                'elapsed': cpu_elapsed,
                'iterations': iterations,
                'status': self._get_status(cpu_score)
            }
            return self.results['cpu']
        
        except Exception as e:
            return {'error': str(e)}
    
    def _normalize_cpu_score(self, elapsed: float, iterations: int) -> int:
        """
        Convert CPU time to 0-100 score
        Reference: 100 = ~0.8 seconds for 100k iterations
        """
        if elapsed <= 0:
            return 100
        
        # Reference time for "excellent" performance
        reference_time = 0.8
        score = (reference_time / elapsed) * 100
        
        # Cap at 100, floor at 10
        return min(int(score), 100) if score > 10 else 10
    
    # ========== RAM BENCHMARK ==========
    def run_ram_benchmark(self, callback=None) -> Dict[str, Any]:
        """
        Lightweight RAM benchmark
        - Allocate small memory blocks (50 MB)
        - Measure read speed only
        - Quick access test
        - Returns 0-100 score
        """
        if self.cancelled:
            return {}
        
        try:
            callback and callback("Starting RAM benchmark...")
            
            size_mb = 50  # Small, safe allocation
            size_bytes = size_mb * 1024 * 1024
            
            # Allocate test data
            callback and callback("Allocating memory...")
            data = bytearray(size_bytes)
            
            # Fill with pattern
            for i in range(0, len(data), 1024):
                data[i:i+10] = b'0123456789'
            
            # Sequential read test (1 second)
            callback and callback("Reading memory...")
            start_time = time.time()
            total = 0
            
            for i in range(0, len(data), 64):
                if self.cancelled:
                    return {}
                total += sum(data[i:i+64])
            
            ram_elapsed = time.time() - start_time
            ram_bandwidth = size_mb / ram_elapsed if ram_elapsed > 0 else 0
            ram_score = self._normalize_ram_score(ram_bandwidth)
            
            callback and callback(f"RAM benchmark: {ram_bandwidth:.0f} MB/s")
            
            # Clean up
            del data
            
            self.results['ram'] = {
                'score': ram_score,
                'bandwidth_mbps': ram_bandwidth,
                'elapsed': ram_elapsed,
                'status': self._get_status(ram_score)
            }
            return self.results['ram']
        
        except Exception as e:
            return {'error': str(e)}
    
    def _normalize_ram_score(self, bandwidth_mbps: float) -> int:
        """
        Convert RAM bandwidth to 0-100 score
        Reference: 100 = ~10,000 MB/s (modern DDR4/5)
        """
        if bandwidth_mbps <= 0:
            return 10
        
        reference_bandwidth = 10000  # MB/s
        score = (bandwidth_mbps / reference_bandwidth) * 100
        
        return min(int(score), 100) if score > 10 else 10
    
    # ========== DISK BENCHMARK ==========
    def run_disk_benchmark(self, callback=None) -> Dict[str, Any]:
        """
        Lightweight disk benchmark
        - Small test file (10 MB)
        - Sequential write + read
        - Quick cleanup
        - Returns 0-100 score
        """
        if self.cancelled:
            return {}
        
        temp_file = None
        try:
            callback and callback("Starting disk benchmark...")
            
            # Create small temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            test_size_mb = 10
            chunk_size = 1024 * 1024  # 1 MB chunks
            
            # Sequential write
            callback and callback("Writing test data...")
            write_start = time.time()
            data = b'0' * chunk_size
            
            for _ in range(test_size_mb):
                if self.cancelled:
                    return {}
                temp_file.write(data)
            
            temp_file.flush()
            os.fsync(temp_file.fileno())
            write_elapsed = time.time() - write_start
            write_speed = test_size_mb / write_elapsed if write_elapsed > 0 else 0
            
            # Sequential read
            callback and callback("Reading test data...")
            temp_file.seek(0)
            read_start = time.time()
            
            bytes_read = 0
            while True:
                if self.cancelled:
                    return {}
                chunk = temp_file.read(chunk_size)
                if not chunk:
                    break
                bytes_read += len(chunk)
            
            read_elapsed = time.time() - read_start
            read_speed = (bytes_read / (1024 * 1024)) / read_elapsed if read_elapsed > 0 else 0
            
            avg_speed = (write_speed + read_speed) / 2
            disk_score = self._normalize_disk_score(avg_speed)
            
            callback and callback(f"Disk benchmark: Write {write_speed:.0f} MB/s, Read {read_speed:.0f} MB/s")
            
            self.results['disk'] = {
                'score': disk_score,
                'write_mbps': write_speed,
                'read_mbps': read_speed,
                'avg_mbps': avg_speed,
                'elapsed': write_elapsed + read_elapsed,
                'status': self._get_status(disk_score)
            }
            return self.results['disk']
        
        except Exception as e:
            return {'error': str(e)}
        
        finally:
            # Clean up
            if temp_file:
                try:
                    temp_file.close()
                    os.unlink(temp_file.name)
                except:
                    pass
    
    def _normalize_disk_score(self, avg_speed_mbps: float) -> int:
        """
        Convert disk speed to 0-100 score
        Reference: 100 = ~500 MB/s (SSD baseline)
        """
        if avg_speed_mbps <= 0:
            return 10
        
        reference_speed = 500  # MB/s SSD
        score = (avg_speed_mbps / reference_speed) * 100
        
        return min(int(score), 100) if score > 10 else 10
    
    # ========== GPU BENCHMARK ==========
    def run_gpu_benchmark(self, callback=None) -> Dict[str, Any]:
        """
        Lightweight GPU benchmark
        - NO rendering or stress test
        - Hardware capability classification only
        - Quick detection
        - Returns 0-100 score based on VRAM + type
        """
        if self.cancelled:
            return {}
        
        try:
            callback and callback("Detecting GPU...")
            
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                
                if not gpus:
                    callback and callback("No discrete GPU detected")
                    self.results['gpu'] = {
                        'score': 50,  # Integrated graphics baseline
                        'type': 'Integrated',
                        'vram_gb': 0,
                        'status': 'Average'
                    }
                    return self.results['gpu']
                
                gpu = gpus[0]
                vram_gb = gpu.memoryTotal / 1024
                
                # Classify GPU by VRAM and name
                gpu_score = self._classify_gpu(gpu.name, vram_gb)
                
                callback and callback(f"GPU: {gpu.name} ({vram_gb:.1f} GB VRAM)")
                
                self.results['gpu'] = {
                    'score': gpu_score,
                    'name': gpu.name,
                    'vram_gb': vram_gb,
                    'status': self._get_status(gpu_score)
                }
                return self.results['gpu']
            
            except ImportError:
                callback and callback("GPU detection library not available")
                self.results['gpu'] = {
                    'score': 40,
                    'type': 'Unknown',
                    'status': 'Cannot Detect'
                }
                return self.results['gpu']
        
        except Exception as e:
            return {'error': str(e)}
    
    def _classify_gpu(self, name: str, vram_gb: float) -> int:
        """Classify GPU into performance tier (0-100)"""
        # RTX/RTX Ti/Quadro (Professional/Gaming High-End)
        if any(x in name.upper() for x in ['RTX 4090', 'RTX 3090', 'A100']):
            return 100
        elif any(x in name.upper() for x in ['RTX 40', 'RTX 30', 'A6000']):
            return 85
        elif any(x in name.upper() for x in ['RTX 20', 'RTX 16', 'A5000']):
            return 75
        
        # Gaming Mid-Range
        elif any(x in name.upper() for x in ['GTX 1080', 'RTX 2070', 'RTX 3070']):
            return 70
        elif any(x in name.upper() for x in ['GTX 1060', 'RTX 2060', 'RTX 3060']):
            return 55
        
        # Entry Level / Integrated
        elif any(x in name.upper() for x in ['UHD', 'IRIS', 'VEGA', 'RADEON']):
            return 40
        
        # Fallback: score by VRAM
        if vram_gb >= 24:
            return 80
        elif vram_gb >= 12:
            return 70
        elif vram_gb >= 8:
            return 60
        elif vram_gb >= 4:
            return 45
        elif vram_gb >= 2:
            return 35
        else:
            return 25
    
    # ========== OVERALL SCORE ==========
    def get_overall_score(self) -> int:
        """Calculate overall system score (average of all components)"""
        scores = [v['score'] for v in self.results.values() if isinstance(v, dict) and 'score' in v]
        if not scores:
            return 0
        return int(sum(scores) / len(scores))
    
    def _get_status(self, score: int) -> str:
        """Map score to status label"""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Average"
        elif score >= 35:
            return "Below Average"
        else:
            return "Poor"
    
    # ========== RUN ALL BENCHMARKS ==========
    def run_all_benchmarks(self, callback=None) -> Dict[str, Any]:
        """Run all benchmarks with progress callback"""
        self.cancelled = False
        
        callback and callback("Benchmark started", 0)
        
        # CPU
        self.run_cpu_benchmark(callback)
        callback and callback("CPU benchmark complete", 25)
        
        if self.cancelled:
            return self.results
        
        # RAM
        self.run_ram_benchmark(callback)
        callback and callback("RAM benchmark complete", 50)
        
        if self.cancelled:
            return self.results
        
        # Disk
        self.run_disk_benchmark(callback)
        callback and callback("Disk benchmark complete", 75)
        
        if self.cancelled:
            return self.results
        
        # GPU
        self.run_gpu_benchmark(callback)
        callback and callback("GPU benchmark complete", 100)
        
        # Add overall score
        self.results['overall'] = {
            'score': self.get_overall_score(),
            'status': self._get_status(self.get_overall_score())
        }
        
        callback and callback("Benchmark complete!", 100)
        
        return self.results
