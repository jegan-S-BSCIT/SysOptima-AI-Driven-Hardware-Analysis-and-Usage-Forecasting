"""
Score Normalizer Module
Converts raw benchmark metrics to normalized 0-100 scores
"""

class ScoreNormalizer:
    """Normalizes benchmark scores to 0-100 scale"""
    
    def __init__(self):
        # Reference values for normalization (can be updated from benchmark_reference.json)
        self.reference_values = {
            'cpu_single_thread': {'min': 10000, 'max': 1000000},
            'cpu_multi_thread': {'min': 50000, 'max': 5000000},
            'memory_read': {'min': 100, 'max': 50000},
            'memory_write': {'min': 100, 'max': 50000},
            'memory_random': {'min': 10000, 'max': 10000000},
            'disk_read': {'min': 10, 'max': 5000},
            'disk_write': {'min': 10, 'max': 5000},
            'disk_iops': {'min': 100, 'max': 100000}
        }
    
    def normalize_score(self, value, metric_name):
        """
        Normalize a raw metric value to 0-100 scale
        
        Args:
            value: Raw metric value
            metric_name: Name of the metric (must be in reference_values)
        
        Returns:
            Normalized score (0-100)
        """
        if metric_name not in self.reference_values:
            raise ValueError(f"Unknown metric: {metric_name}")
        
        ref = self.reference_values[metric_name]
        min_val = ref['min']
        max_val = ref['max']
        
        # Linear normalization
        if value <= min_val:
            return 0
        elif value >= max_val:
            return 100
        else:
            return ((value - min_val) / (max_val - min_val)) * 100
    
    def normalize_cpu_scores(self, cpu_results):
        """Normalize CPU benchmark results"""
        scores = {}
        
        if 'single_thread' in cpu_results:
            scores['single_thread'] = self.normalize_score(
                cpu_results['single_thread']['score'],
                'cpu_single_thread'
            )
        
        if 'multi_thread' in cpu_results:
            scores['multi_thread'] = self.normalize_score(
                cpu_results['multi_thread']['score'],
                'cpu_multi_thread'
            )
        
        # Overall CPU score (weighted average)
        if scores:
            scores['overall'] = (scores.get('single_thread', 0) * 0.4 + 
                               scores.get('multi_thread', 0) * 0.6)
        
        return scores
    
    def normalize_memory_scores(self, memory_results):
        """Normalize memory benchmark results"""
        scores = {}
        
        if 'sequential_read' in memory_results:
            scores['sequential_read'] = self.normalize_score(
                memory_results['sequential_read']['bandwidth_mbps'],
                'memory_read'
            )
        
        if 'sequential_write' in memory_results:
            scores['sequential_write'] = self.normalize_score(
                memory_results['sequential_write']['bandwidth_mbps'],
                'memory_write'
            )
        
        if 'random_access' in memory_results:
            scores['random_access'] = self.normalize_score(
                memory_results['random_access']['accesses_per_second'],
                'memory_random'
            )
        
        # Overall memory score
        if scores:
            scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def normalize_disk_scores(self, disk_results):
        """Normalize disk benchmark results"""
        scores = {}
        
        if 'sequential_read' in disk_results:
            scores['sequential_read'] = self.normalize_score(
                disk_results['sequential_read']['speed_mbps'],
                'disk_read'
            )
        
        if 'sequential_write' in disk_results:
            scores['sequential_write'] = self.normalize_score(
                disk_results['sequential_write']['speed_mbps'],
                'disk_write'
            )
        
        if 'random_access' in disk_results:
            scores['random_access'] = self.normalize_score(
                disk_results['random_access']['iops'],
                'disk_iops'
            )
        
        # Overall disk score
        if scores:
            scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def calculate_system_score(self, cpu_score, memory_score, disk_score):
        """
        Calculate overall system performance score
        
        Args:
            cpu_score: CPU overall score
            memory_score: Memory overall score
            disk_score: Disk overall score
        
        Returns:
            Overall system score (0-100)
        """
        # Weighted average: CPU 50%, Memory 30%, Disk 20%
        return (cpu_score * 0.5 + memory_score * 0.3 + disk_score * 0.2)
