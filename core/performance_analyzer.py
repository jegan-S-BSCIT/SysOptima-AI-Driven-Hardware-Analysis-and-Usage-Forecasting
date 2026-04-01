"""
Comparison and Performance Analysis Engine
Compares local system performance against reference benchmarks
Generates insights and recommendations for B.Sc. IT project
"""

from core.lightweight_benchmarks import LightweightBenchmark
from typing import Dict, List, Tuple
import json
import os


class PerformanceAnalyzer:
    """Analyzes and compares system performance"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.benchmark = LightweightBenchmark()
        self.results = None
        self.comparisons = None
        self.bottleneck = None
        self.insights = []
    
    def run_analysis(self) -> Dict:
        """Run complete performance analysis"""
        # Run benchmarks
        self.results = self.benchmark.run_all_benchmarks()
        
        # Perform comparisons
        self.comparisons = self._compare_all()
        
        # Identify bottleneck
        self.bottleneck = self._identify_bottleneck()
        
        # Generate insights
        self.insights = self._generate_insights()
        
        return {
            "results": self.results,
            "comparisons": self.comparisons,
            "bottleneck": self.bottleneck,
            "insights": self.insights,
            "overall_health": self._calculate_health()
        }
    
    def _compare_all(self) -> Dict:
        """Compare all components against reference"""
        comparisons = {}
        
        for component in ['cpu', 'ram', 'storage', 'gpu']:
            local_score = self.results[component]['score']
            ref_score = self.results[component]['reference_score']
            
            diff_percent = self.benchmark.get_percent_difference(local_score, ref_score)
            
            if diff_percent > 10:
                status = "ABOVE AVERAGE"
                status_code = 1
            elif diff_percent > -10:
                status = "AVERAGE"
                status_code = 0
            else:
                status = "BELOW AVERAGE"
                status_code = -1
            
            comparisons[component] = {
                "local_score": local_score,
                "reference_score": ref_score,
                "difference_percent": diff_percent,
                "status": status,
                "status_code": status_code
            }
        
        return comparisons
    
    def _identify_bottleneck(self) -> Dict:
        """
        Identify which component is the bottleneck
        Evaluate disk performance based on usage
        
        Rule:
        <70% = score 85
        70-85% = score 60
        >85% = score 40
        """
        scores = {
            'CPU': self.cpu_score,
            'RAM': self.ram_score,
            'Disk': self.disk_score
        }
        return min(scores, key=scores.get)
    
    @staticmethod
    def get_overall_performance_score(cpu_score: float, memory_score: float, 
                                      disk_score: float) -> float:
        """
        Calculate overall performance score (weighted average)
        
        Rule:
        cpu*0.35 + memory*0.35 + disk*0.30
        """
        overall = (
            cpu_score * 0.35 +
            memory_score * 0.35 +
            disk_score * 0.30
        )
        return round(overall, 1)
    
    @staticmethod
    def get_performance_status(overall_score: float) -> tuple:
        """
        Get status text and color based on performance score
        """
        if overall_score >= 75:
            return ("Good", "#00CC88", "System performing optimally")
        elif overall_score >= 55:
            return ("Moderate", "#FFB84D", "System performance is acceptable")
        else:
            return ("Poor", "#FF6B6B", "System performance is degraded")
    
    @staticmethod
    def get_performance_interpretation(cpu_score: float, memory_score: float, 
                                      disk_score: float, overall_score: float) -> str:
        """
        Generate intelligent interpretation of performance status
        """
        insights = []
        
        # CPU insights
        if cpu_score >= 85:
            insights.append("CPU usage is low (<50%), ensuring high responsiveness.")
        elif cpu_score >= 65:
            insights.append("CPU load is moderate (50-75%).")
        else:
            insights.append("High CPU usage detected (>75%), system may feel sluggish.")
        
        # Memory insights
        if memory_score >= 90:
            insights.append("Memory availability is excellent (<60% used).")
        elif memory_score >= 65:
            insights.append("Memory usage is moderate (60-80%).")
        else:
            insights.append("Available memory is low (>80%), multitasking may be affected.")
        
        # Disk insights
        if disk_score >= 85:
            insights.append("Disk space is plentiful (<70% used).")
        elif disk_score >= 60:
            insights.append("Disk usage is moderate (70-85%).")
        else:
            insights.append("Disk space is running low (>85%), consider cleaning up files.")
        
        # Overall assessment template
        if overall_score >= 75:
            intro = "System performance is good."
        elif overall_score >= 55:
            intro = "System performance is moderate."
        else:
            intro = "System performance is poor."
            
        full_text = f"{intro} " + " ".join(insights)
        return full_text
    
    @staticmethod
    def evaluate_system_performance():
        """
        Complete system performance evaluation - FAST, NON-BLOCKING
        Calculated ONCE per call.
        """
        try:
            # Get current metrics - USE NON-BLOCKING CALLS
            # psutil.cpu_percent(interval=None) is non-blocking
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # If first call, it might yield 0.0 or garbage if not measuring since last call.
            # To ensure we get a semi-valid reading without blocking for 1s, we can't do much if interval=None is strict.
            # However, user explicitly requested: "Do NOT use cpu_percent(interval=1). Use cpu_percent(interval=None)"
            # Note: interval=None returns percentage since last call.
            # If we want a valid reading we might need two calls, but user forbids blocking/loops.
            # We will assume the app has called this before or accepts the instantaneous reading.
            # Actually, to make it slightly more robust without blocking, we can rely on background monitoring if available, 
            # but here we strictly follow: "Performance data is calculated ONLY ONCE when the Performance page is opened."
            
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:' if psutil.WINDOWS else '/')
            
            # Get hardware info for scoring (cached, fast)
            # We don't strictly need detailed hardware info for the rule-based logic required, 
            # as it relies on percentages.
            
            # Calculate component scores
            cpu_score = PerformanceAnalyzer.get_cpu_performance_score(cpu_percent)
            memory_score = PerformanceAnalyzer.get_memory_performance_score(mem.percent)
            disk_score = PerformanceAnalyzer.get_disk_performance_score(disk.percent)
            
            # Calculate overall score
            overall_score = PerformanceAnalyzer.get_overall_performance_score(
                cpu_score, memory_score, disk_score
            )
            
            # Get status
            status_text, status_color, status_desc = PerformanceAnalyzer.get_performance_status(overall_score)
            
            # Get interpretation
            interpretation = PerformanceAnalyzer.get_performance_interpretation(
                cpu_score, memory_score, disk_score, overall_score
            )
            
            return {
                "overall_score": overall_score,
                "cpu_score": cpu_score,
                "memory_score": memory_score,
                "disk_score": disk_score,
                "status": status_text,
                "status_color": status_color,
                "status_description": status_desc,
                "interpretation": interpretation,
                "last_updated": "Just now",
                "note": "Performance snapshot captured."
            }
        except Exception as e:
            print(f"Performance evaluation error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "overall_score": 0.0,
                "cpu_score": 0.0,
                "memory_score": 0.0,
                "disk_score": 0.0,
                "status": "Error",
                "status_color": "#666666",
                "status_description": "Evaluation failed",
                "interpretation": f"Error: {str(e)}",
                "last_updated": "Error",
                "note": ""
            }

    """Analyzes system performance using rule-based evaluation"""
    
    @staticmethod
    def get_cpu_performance_score(cpu_usage: float, core_count: int = None) -> float:
        """
        Evaluate CPU performance based on current usage and core count
        
        Args:
            cpu_usage: Current CPU usage percentage
            core_count: Physical core count (optional, for future enhancement)
            
        Returns:
            Performance score (0-100)
        """
        # More cores mean better baseline performance
        baseline = 80 if core_count and core_count >= 8 else 75
        
        # Adjust based on current load
        if cpu_usage < 30:
            # Very light load - excellent headroom
            return min(95, baseline + 5)
        elif cpu_usage < 50:
            # Light load - good performance
            return baseline
        elif cpu_usage < 75:
            # Moderate load - acceptable performance
            return 70
        else:
            # Heavy load - constrained performance
            return 40
    
    @staticmethod
    def get_memory_performance_score(mem_usage: float, total_ram_gb: float = None) -> float:
        """
        Evaluate memory performance based on usage pressure
        
        Args:
            mem_usage: Current memory usage percentage
            total_ram_gb: Total RAM in GB (optional, for future enhancement)
            
        Returns:
            Performance score (0-100)
        """
        # More RAM means better baseline performance
        if total_ram_gb:
            if total_ram_gb >= 32:
                baseline = 85
            elif total_ram_gb >= 16:
                baseline = 80
            else:
                baseline = 75
        else:
            baseline = 80
        
        # Adjust based on usage pressure
        if mem_usage < 40:
            # Very light pressure - excellent
            return min(95, baseline + 10)
        elif mem_usage < 60:
            # Low pressure - good
            return baseline
        elif mem_usage < 80:
            # Moderate pressure - acceptable
            return 65
        else:
            # High pressure - degraded performance
            return 45
    
    @staticmethod
    def get_disk_performance_score(disk_usage: float) -> float:
        """
        Evaluate disk performance based on usage
        
        Args:
            disk_usage: Disk usage percentage
            
        Returns:
            Performance score (0-100)
        """
        if disk_usage < 60:
            # Plenty of free space - excellent performance
            return 85
        elif disk_usage < 80:
            # Moderate usage - acceptable
            return 65
        elif disk_usage < 90:
            # High usage - degraded performance
            return 45
        else:
            # Critical usage - poor performance
            return 30
    
    @staticmethod
    def get_gpu_performance_score(gpu_available: bool) -> float:
        """
        Evaluate GPU performance availability
        
        Args:
            gpu_available: Whether dedicated GPU is available
            
        Returns:
            Performance score (0-100)
        """
        # GPU availability improves performance for graphics-intensive tasks
        return 80 if gpu_available else 50
    
    @staticmethod
    def get_overall_performance_score(cpu_score: float, memory_score: float, 
                                      disk_score: float) -> float:
        """
        Calculate overall performance score (weighted average)
        
        Args:
            cpu_score: CPU performance score
            memory_score: Memory performance score
            disk_score: Disk performance score
            
        Returns:
            Overall performance score (0-100)
        """
        # Weights: CPU and Memory are equally important (35% each), Disk 30%
        overall = (
            cpu_score * 0.35 +
            memory_score * 0.35 +
            disk_score * 0.30
        )
        return round(overall, 1)
    
    @staticmethod
    def get_performance_status(overall_score: float) -> tuple:
        """
        Get status text and color based on performance score
        
        Args:
            overall_score: Overall performance score
            
        Returns:
            Tuple of (status_text, color_code, description)
        """
        if overall_score >= 75:
            return ("Excellent", "#00CC88", "System performing optimally")
        elif overall_score >= 65:
            return ("Good", "#4BA3FF", "System performing well")
        elif overall_score >= 55:
            return ("Moderate", "#FFB84D", "System performance is acceptable")
        else:
            return ("Poor", "#FF6B6B", "System performance is degraded")
    
    @staticmethod
    def get_performance_interpretation(cpu_score: float, memory_score: float, 
                                      disk_score: float, overall_score: float) -> str:
        """
        Generate intelligent interpretation of performance status
        
        Args:
            cpu_score: CPU performance score
            memory_score: Memory performance score
            disk_score: Disk performance score
            overall_score: Overall performance score
            
        Returns:
            Interpretation text explaining the performance state
        """
        insights = []
        
        # CPU insights
        if cpu_score >= 80:
            insights.append("CPU headroom is excellent - system can handle demanding tasks.")
        elif cpu_score >= 70:
            insights.append("CPU is performing well with good capacity for multitasking.")
        elif cpu_score >= 50:
            insights.append("CPU is moderately loaded - consider closing unnecessary applications.")
        else:
            insights.append("CPU is heavily constrained - close background applications to improve performance.")
        
        # Memory insights
        if memory_score >= 80:
            insights.append("Memory is healthy with plenty of available capacity.")
        elif memory_score >= 65:
            insights.append("Memory usage is moderate - adequate for current workload.")
        elif memory_score >= 45:
            insights.append("Memory pressure is higher than optimal - may impact multitasking performance.")
        else:
            insights.append("Memory is critically constrained - consider upgrading or closing applications.")
        
        # Disk insights
        if disk_score >= 80:
            insights.append("Disk space is abundant - no storage concerns.")
        elif disk_score >= 65:
            insights.append("Disk space is adequate for typical use.")
        elif disk_score >= 45:
            insights.append("Disk is getting full - consider freeing up space for better performance.")
        else:
            insights.append("Disk is critically full - this significantly impacts system performance.")
        
        # Overall assessment
        if overall_score >= 75:
            summary = "Overall system performance is excellent. All components are operating optimally."
        elif overall_score >= 65:
            summary = "Overall system performance is good. Consider monitoring resource usage patterns."
        elif overall_score >= 55:
            summary = "Overall system performance is moderate. Optimization opportunities exist."
        else:
            summary = "Overall system performance is degraded. Consider system optimization or hardware upgrade."
        
        return summary + "\n\n" + "\n".join(f"• {insight}" for insight in insights)
    
    @staticmethod
    def evaluate_system_performance():
        """
        Complete system performance evaluation - FAST, NON-BLOCKING
        
        Returns:
            dict: Comprehensive performance analysis including all scores and interpretation
        """
        try:
            # Get current metrics - USE NON-BLOCKING CALLS
            cpu_percent = psutil.cpu_percent(interval=0)  # Non-blocking!
            if cpu_percent == 0:
                cpu_percent = psutil.cpu_percent(interval=0.1)  # Quick sample if needed
            
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:' if psutil.WINDOWS else '/')
            
            # Get hardware info for scoring (cached, fast)
            cpu_info = get_cpu_info()
            mem_info = get_memory_info()
            
            # Calculate component scores
            cpu_score = PerformanceAnalyzer.get_cpu_performance_score(
                cpu_percent, 
                cpu_info["physical_cores"]
            )
            memory_score = PerformanceAnalyzer.get_memory_performance_score(
                mem.percent,
                mem_info["total_gb"]
            )
            disk_score = PerformanceAnalyzer.get_disk_performance_score(
                disk.percent
            )
            
            # Calculate overall score
            overall_score = PerformanceAnalyzer.get_overall_performance_score(
                cpu_score, memory_score, disk_score
            )
            
            # Get status
            status_text, status_color, status_desc = PerformanceAnalyzer.get_performance_status(overall_score)
            
            # Get interpretation
            interpretation = PerformanceAnalyzer.get_performance_interpretation(
                cpu_score, memory_score, disk_score, overall_score
            )
            
            return {
                "overall_score": overall_score,
                "cpu_score": round(cpu_score, 1),
                "memory_score": round(memory_score, 1),
                "disk_score": round(disk_score, 1),
                "status": status_text,
                "status_color": status_color,
                "status_description": status_desc,
                "interpretation": interpretation,
                "last_updated": "On page load",
                "note": "Performance scores are evaluated once when page loads. For real-time metrics, see Dashboard."
            }
        except Exception as e:
            print(f"Performance evaluation error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "overall_score": 0.0,
                "cpu_score": 0.0,
                "memory_score": 0.0,
                "disk_score": 0.0,
                "status": "Evaluation Failed",
                "status_color": "#666666",
                "status_description": "Could not evaluate system performance",
                "interpretation": f"An error occurred during evaluation: {str(e)}",
                "last_updated": "Error",
                "note": "Please check system access permissions."
            }
