"""
Performance prediction facade for SysOptima
"""

from typing import Dict

try:
    from analysis.predictor import PerformancePredictor
except Exception:
    PerformancePredictor = None

class Predictor:
    """Wraps PerformancePredictor for convenience"""
    def __init__(self):
        self.predictor = PerformancePredictor() if PerformancePredictor else None

    def predict_fps(self, cpu_score: float, memory_score: float, gpu_score: float, game_type: str = 'medium') -> Dict:
        if not self.predictor:
            return {}
        return self.predictor.predict_fps(cpu_score, memory_score, gpu_score, game_type)

    def predict_workloads(self, cpu_score: float, memory_score: float, disk_score: float) -> Dict:
        if not self.predictor:
            return {}
        return self.predictor.predict_workload_capability(cpu_score, memory_score, disk_score)

    def predict_multitasking(self, cpu_info: Dict, memory_score: float) -> Dict:
        if not self.predictor:
            return {}
        return self.predictor.predict_multitasking(cpu_info, memory_score)
