"""
Hardware Performance Analyzer
B.Sc. IT Final Year Project: Intelligent Computer Performance Analysis and Guidance System

This module analyzes hardware components and provides performance benchmarks, bottleneck detection,
and diagnostic explanations suitable for non-technical users.
"""

import psutil
import platform
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ComponentScore:
    """Stores benchmark score for a hardware component"""
    name: str
    score: float  # 0-100
    status: str   # Working/Warning/Critical
    health: str   # Good/Average/Poor


class HardwareAnalyzer:
    """Analyzes hardware components and generates performance reports"""
    
    # Standard benchmark reference values for comparison
    BENCHMARK_REFERENCE = {
        'cpu': {
            'excellent': {'cores': 8, 'speed_ghz': 3.5},
            'good': {'cores': 6, 'speed_ghz': 3.0},
            'average': {'cores': 4, 'speed_ghz': 2.5}
        },
        'ram': {
            'excellent': 16,  # GB
            'good': 8,
            'average': 4
        },
        'gpu': {
            'excellent': 8,   # GB VRAM
            'good': 4,
            'average': 2
        },
        'storage': {
            'excellent': {'free_percent': 50},
            'good': {'free_percent': 30},
            'average': {'free_percent': 10}
        }
    }
    
    def __init__(self):
        """Initialize hardware analyzer"""
        self.system_data = {}
        self.scores = {}
        self.bottleneck = None
        self.recommendations = []
        
    def collect_hardware_data(self) -> Dict:
        """Collect all hardware information from system"""
        # CPU Information
        cpu_data = {
            'physical_cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'usage_percent': psutil.cpu_percent(interval=1),
            'frequency': psutil.cpu_freq(),
            'processor': platform.processor()
        }
        
        # RAM Information
        ram_info = psutil.virtual_memory()
        swap_info = psutil.swap_memory()
        ram_data = {
            'total_gb': ram_info.total / (1024**3),
            'used_gb': ram_info.used / (1024**3),
            'available_gb': ram_info.available / (1024**3),
            'percent_used': ram_info.percent,
            'swap_total_gb': swap_info.total / (1024**3),
            'swap_used_gb': swap_info.used / (1024**3)
        }
        
        # Storage Information
        storage_data = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                storage_data[partition.device] = {
                    'mount': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': usage.total / (1024**3),
                    'used_gb': usage.used / (1024**3),
                    'free_gb': usage.free / (1024**3),
                    'percent_used': usage.percent
                }
            except:
                pass
        
        # GPU Information
        gpu_data = {}
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                gpu_data[gpu.id] = {
                    'name': gpu.name,
                    'load_percent': gpu.load * 100,
                    'memory_total_mb': gpu.memoryTotal,
                    'memory_used_mb': gpu.memoryUsed,
                    'memory_free_mb': gpu.memoryFree,
                    'temperature': gpu.temperature if hasattr(gpu, 'temperature') else None
                }
        except:
            gpu_data = None
        
        self.system_data = {
            'cpu': cpu_data,
            'ram': ram_data,
            'storage': storage_data,
            'gpu': gpu_data
        }
        return self.system_data
    
    def analyze_cpu(self) -> ComponentScore:
        """Analyze CPU performance and generate score"""
        cpu = self.system_data['cpu']
        
        cores = cpu['logical_cores']
        speed_ghz = (cpu['frequency'].current / 1000) if cpu['frequency'] else 0
        usage = cpu['usage_percent']
        
        # Calculate score based on cores and speed
        core_score = min((cores / 8) * 50, 50)  # Max 50 points for cores
        speed_score = min((speed_ghz / 4.0) * 50, 50)  # Max 50 points for speed
        
        score = core_score + speed_score
        
        # Determine status
        if usage > 80:
            status = "Warning"
        elif usage > 95:
            status = "Critical"
        else:
            status = "Working"
        
        # Determine health
        if score >= 80:
            health = "Good"
        elif score >= 60:
            health = "Average"
        else:
            health = "Poor"
        
        return ComponentScore(
            name="CPU",
            score=score,
            status=status,
            health=health
        )
    
    def analyze_ram(self) -> ComponentScore:
        """Analyze RAM performance and generate score"""
        ram = self.system_data['ram']
        
        total_gb = ram['total_gb']
        used_percent = ram['percent_used']
        
        # Calculate score based on capacity and usage
        capacity_score = min((total_gb / 16) * 60, 60)  # Max 60 for capacity
        usage_score = max(0, 40 - (used_percent * 0.4))  # Max 40 for low usage
        
        score = capacity_score + usage_score
        
        # Determine status
        if used_percent > 90:
            status = "Critical"
        elif used_percent > 80:
            status = "Warning"
        else:
            status = "Working"
        
        # Determine health
        if score >= 80:
            health = "Good"
        elif score >= 60:
            health = "Average"
        else:
            health = "Poor"
        
        return ComponentScore(
            name="RAM",
            score=score,
            status=status,
            health=health
        )
    
    def analyze_gpu(self) -> ComponentScore:
        """Analyze GPU performance and generate score"""
        gpu_data = self.system_data['gpu']
        
        if gpu_data is None:
            return ComponentScore(
                name="GPU",
                score=0,
                status="Not Available",
                health="N/A"
            )
        
        # Get first GPU
        first_gpu = gpu_data[0]
        vram_gb = first_gpu['memory_total_mb'] / 1024
        usage_percent = first_gpu['load_percent']
        
        # Calculate score
        vram_score = min((vram_gb / 8) * 60, 60)
        usage_score = max(0, 40 - (usage_percent * 0.4))
        
        score = vram_score + usage_score
        
        # Determine status
        if usage_percent > 90:
            status = "Critical"
        elif usage_percent > 70:
            status = "Warning"
        else:
            status = "Working"
        
        # Determine health
        if score >= 80:
            health = "Good"
        elif score >= 60:
            health = "Average"
        else:
            health = "Poor"
        
        return ComponentScore(
            name="GPU",
            score=score,
            status=status,
            health=health
        )
    
    def analyze_storage(self) -> ComponentScore:
        """Analyze storage performance and generate score"""
        storage = self.system_data['storage']
        
        if not storage:
            return ComponentScore(
                name="Storage",
                score=0,
                status="Not Available",
                health="N/A"
            )
        
        # Analyze primary drive (C:)
        primary_drive = storage.get('C:\\', list(storage.values())[0])
        free_percent = 100 - primary_drive['percent_used']
        total_gb = primary_drive['total_gb']
        
        # Calculate score
        capacity_score = min((total_gb / 500) * 40, 40)
        free_space_score = min((free_percent / 100) * 60, 60)
        
        score = capacity_score + free_space_score
        
        # Determine status
        if primary_drive['percent_used'] > 95:
            status = "Critical"
        elif primary_drive['percent_used'] > 85:
            status = "Warning"
        else:
            status = "Working"
        
        # Determine health
        if score >= 80:
            health = "Good"
        elif score >= 60:
            health = "Average"
        else:
            health = "Poor"
        
        return ComponentScore(
            name="Storage",
            score=score,
            status=status,
            health=health
        )
    
    def identify_bottleneck(self) -> Tuple[str, str]:
        """Identify which component is bottlenecking system performance"""
        scores_dict = {
            'cpu': self.scores['cpu'].score,
            'ram': self.scores['ram'].score,
            'gpu': self.scores['gpu'].score if self.scores['gpu'].score > 0 else 100,
            'storage': self.scores['storage'].score
        }
        
        bottleneck_component = min(scores_dict, key=scores_dict.get)
        score = scores_dict[bottleneck_component]
        
        explanations = {
            'cpu': "Your CPU is not fast enough to process tasks efficiently. Consider upgrading to a processor with more cores or higher clock speed.",
            'ram': "Your RAM is full or nearly full, causing system slowdown. Close unnecessary programs or upgrade your RAM.",
            'gpu': "Your GPU has limited VRAM or performance. This affects gaming and video processing tasks.",
            'storage': "Your storage drive is almost full, slowing down file operations. Free up space or upgrade your drive."
        }
        
        return bottleneck_component, explanations[bottleneck_component]
    
    def calculate_overall_health(self) -> float:
        """Calculate overall system health percentage"""
        total_score = sum(
            score.score for score in self.scores.values() 
            if score.score > 0
        )
        num_components = sum(1 for score in self.scores.values() if score.score > 0)
        
        return (total_score / num_components) if num_components > 0 else 0
    
    def classify_system_health(self, health_score: float) -> str:
        """Classify system health as Excellent/Good/Average/Poor"""
        if health_score >= 85:
            return "Excellent"
        elif health_score >= 70:
            return "Good"
        elif health_score >= 50:
            return "Average"
        else:
            return "Poor"
    
    def get_usage_capability(self) -> Dict:
        """Determine system capability for various use cases"""
        overall_health = self.calculate_overall_health()
        gpu_score = self.scores['gpu'].score if self.scores['gpu'].score > 0 else 0
        ram_score = self.scores['ram'].score
        
        capabilities = {
            'gaming': self._classify_gaming(gpu_score, overall_health),
            'video_editing': self._classify_video_editing(overall_health, ram_score),
            'programming': self._classify_programming(overall_health, ram_score)
        }
        
        return capabilities
    
    def _classify_gaming(self, gpu_score: float, overall: float) -> str:
        """Classify gaming capability"""
        if gpu_score >= 80 and overall >= 80:
            return "High (1440p/60fps or 4K/30fps)"
        elif gpu_score >= 60 and overall >= 70:
            return "Medium (1080p/60fps)"
        else:
            return "Low (720p or 1080p with low settings)"
    
    def _classify_video_editing(self, overall: float, ram: float) -> str:
        """Classify video editing capability"""
        if overall >= 80 and ram >= 80:
            return "4K editing"
        elif overall >= 70 and ram >= 70:
            return "1080p editing"
        else:
            return "Not recommended for video editing"
    
    def _classify_programming(self, overall: float, ram: float) -> str:
        """Classify programming capability"""
        if overall >= 70 and ram >= 70:
            return "Suitable for development"
        else:
            return "Limited for development"
    
    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # CPU recommendations
        if self.scores['cpu'].score < 60:
            recommendations.append(
                "CPU Optimization: Close background applications and disable unnecessary startup programs. "
                "Consider upgrading your processor if working with heavy computational tasks."
            )
        
        # RAM recommendations
        ram_score = self.scores['ram']
        if ram_score.score < 60 or self.system_data['ram']['percent_used'] > 80:
            recommendations.append(
                "RAM Management: You are using " + str(int(self.system_data['ram']['percent_used'])) + "% of your RAM. "
                "Close unused programs or upgrade to 16GB RAM for better multitasking."
            )
        
        # Storage recommendations
        storage_score = self.scores['storage']
        if storage_score.score < 60:
            primary = self.system_data['storage'].get('C:\\', list(self.system_data['storage'].values())[0])
            recommendations.append(
                "Storage Cleanup: Your C: drive is " + str(int(primary['percent_used'])) + "% full. "
                "Delete old files, uninstall unused programs, or upgrade to a larger SSD."
            )
        
        # GPU recommendations
        if self.system_data['gpu']:
            gpu_score = self.scores['gpu']
            if gpu_score.score < 60:
                recommendations.append(
                    "GPU Note: Your GPU has limited performance. It's suitable for casual gaming and everyday tasks. "
                    "For gaming or video work, consider a more powerful GPU."
                )
        
        return recommendations
    
    def generate_report(self) -> str:
        """Generate complete hardware performance report"""
        self.collect_hardware_data()
        
        # Analyze all components
        self.scores = {
            'cpu': self.analyze_cpu(),
            'ram': self.analyze_ram(),
            'gpu': self.analyze_gpu(),
            'storage': self.analyze_storage()
        }
        
        # Calculate overall metrics
        overall_health = self.calculate_overall_health()
        health_classification = self.classify_system_health(overall_health)
        bottleneck_name, bottleneck_explanation = self.identify_bottleneck()
        usage_capability = self.get_usage_capability()
        recommendations = self.generate_recommendations()
        
        # Generate report
        report = f"""
{'='*80}
SYSTEM PERFORMANCE REPORT
Intelligent Computer Performance Analysis and Guidance System
{'='*80}

CPU ANALYSIS
{'─'*80}
Status: {self.scores['cpu'].status}
Benchmark Score: {self.scores['cpu'].score:.1f}/100
Health: {self.scores['cpu'].health}
Explanation:
  - Physical Cores: {self.system_data['cpu']['physical_cores']}
  - Logical Cores: {self.system_data['cpu']['logical_cores']}
  - Current Usage: {self.system_data['cpu']['usage_percent']:.1f}%
  - Current Clock Speed: {self.system_data['cpu']['frequency'].current:.0f} MHz
  
  Your CPU is performing at {self.scores['cpu'].health.lower()} levels. 
  {self._get_cpu_explanation()}

RAM ANALYSIS
{'─'*80}
Status: {self.scores['ram'].status}
Benchmark Score: {self.scores['ram'].score:.1f}/100
Health: {self.scores['ram'].health}
Explanation:
  - Total RAM: {self.system_data['ram']['total_gb']:.1f} GB
  - Used RAM: {self.system_data['ram']['used_gb']:.1f} GB ({self.system_data['ram']['percent_used']:.1f}%)
  - Available RAM: {self.system_data['ram']['available_gb']:.1f} GB
  - Swap Memory Used: {self.system_data['ram']['swap_used_gb']:.2f} GB
  
  Your RAM capacity is {self.scores['ram'].health.lower()} for modern multitasking.
  {self._get_ram_explanation()}

GPU ANALYSIS
{'─'*80}"""
        
        if self.system_data['gpu']:
            gpu = self.system_data['gpu'][0]
            report += f"""
Status: {self.scores['gpu'].status}
Benchmark Score: {self.scores['gpu'].score:.1f}/100
Health: {self.scores['gpu'].health}
Explanation:
  - GPU Model: {gpu['name']}
  - VRAM Total: {gpu['memory_total_mb']/1024:.1f} GB
  - VRAM Used: {gpu['memory_used_mb']/1024:.2f} GB
  - GPU Load: {gpu['load_percent']:.1f}%
  - Temperature: {gpu['temperature']:.0f}°C
  
  Your GPU performance is {self.scores['gpu'].health.lower()} for graphics-intensive tasks.
  {self._get_gpu_explanation()}"""
        else:
            report += """
Status: Not Available
Benchmark Score: N/A
Health: N/A
Explanation:
  - No dedicated GPU detected. System using integrated graphics.
  - This is sufficient for everyday tasks and light gaming.
  """
        
        report += f"""

STORAGE ANALYSIS
{'─'*80}
Status: {self.scores['storage'].status}
Benchmark Score: {self.scores['storage'].score:.1f}/100
Health: {self.scores['storage'].health}
Explanation:
"""
        for drive, info in self.system_data['storage'].items():
            report += f"""
  Drive {drive}:
    - File System: {info['fstype']}
    - Total Capacity: {info['total_gb']:.1f} GB
    - Used Space: {info['used_gb']:.1f} GB ({info['percent_used']:.1f}%)
    - Free Space: {info['free_gb']:.1f} GB
"""
        
        report += f"""
  Your storage health is {self.scores['storage'].health.lower()}.
  {self._get_storage_explanation()}

BOTTLENECK ANALYSIS
{'─'*80}
Identified Bottleneck: {bottleneck_name.upper()}
Explanation:
  {bottleneck_explanation}

OVERALL SYSTEM HEALTH
{'─'*80}
Health Score: {overall_health:.1f}/100
Classification: {health_classification}
Status: Your system is performing at a {health_classification.lower()} level.

USAGE CAPABILITY
{'─'*80}
Gaming: {usage_capability['gaming']}
Video Editing: {usage_capability['video_editing']}
Programming & Design: {usage_capability['programming']}

RECOMMENDATIONS
{'─'*80}
"""
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        else:
            report += "Your system is well-optimized. No major upgrades needed.\n"
        
        report += f"""
{'='*80}
Report Generated: {self._get_current_date()}
System: {self.system_data['cpu']['processor']}
{'='*80}
"""
        
        return report
    
    def _get_cpu_explanation(self) -> str:
        """Get CPU status explanation"""
        score = self.scores['cpu'].score
        if score >= 80:
            return "Your processor is modern and powerful, suitable for gaming, video editing, and heavy computing tasks."
        elif score >= 60:
            return "Your processor is adequate for daily computing, web browsing, and moderate office work."
        else:
            return "Your processor is older or has limited cores. Consider upgrading for better performance."
    
    def _get_ram_explanation(self) -> str:
        """Get RAM status explanation"""
        usage = self.system_data['ram']['percent_used']
        if usage > 85:
            return "WARNING: Your RAM is heavily used. Close unnecessary programs to free up memory."
        elif usage > 70:
            return "Your RAM usage is moderately high. You may experience slowdowns during heavy multitasking."
        else:
            return "Your RAM usage is healthy. Plenty of memory available for smooth operation."
    
    def _get_gpu_explanation(self) -> str:
        """Get GPU status explanation"""
        score = self.scores['gpu'].score
        if score >= 80:
            return "Your GPU is excellent for gaming and video processing."
        elif score >= 60:
            return "Your GPU is suitable for 1080p gaming and basic video work."
        else:
            return "Your GPU has limited performance. Suitable for casual gaming and everyday tasks."
    
    def _get_storage_explanation(self) -> str:
        """Get storage status explanation"""
        primary = self.system_data['storage'].get('C:\\', list(self.system_data['storage'].values())[0])
        if primary['percent_used'] > 90:
            return "CRITICAL: Your storage is almost full. This severely impacts system performance. Free up space immediately."
        elif primary['percent_used'] > 80:
            return "Your storage is getting full. Consider deleting old files or upgrading your drive."
        else:
            return "Your storage has adequate free space for normal operations."
    
    @staticmethod
    def _get_current_date() -> str:
        """Get current date as string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Example usage
if __name__ == "__main__":
    analyzer = HardwareAnalyzer()
    report = analyzer.generate_report()
    print(report)
