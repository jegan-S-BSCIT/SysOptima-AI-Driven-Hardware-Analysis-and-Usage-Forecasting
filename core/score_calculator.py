"""
Score calculation facade for SysOptima
"""

from typing import Dict

try:
    from analysis.score_normalizer import ScoreNormalizer
except Exception:
    ScoreNormalizer = None

class ScoreCalculator:
    """Calculates component and overall scores"""
    def __init__(self):
        self.normalizer = ScoreNormalizer() if ScoreNormalizer else None

    def compute(self, cpu_results: Dict, memory_results: Dict, disk_results: Dict) -> Dict[str, Dict]:
        if not self.normalizer:
            return {}
        cpu_scores = self.normalizer.normalize_cpu_scores(cpu_results or {})
        memory_scores = self.normalizer.normalize_memory_scores(memory_results or {})
        disk_scores = self.normalizer.normalize_disk_scores(disk_results or {})
        overall = {}
        if cpu_scores and memory_scores and disk_scores:
            overall['system'] = self.normalizer.calculate_system_score(
                cpu_scores.get('overall', 0),
                memory_scores.get('overall', 0),
                disk_scores.get('overall', 0)
            )
        return {
            'cpu': cpu_scores,
            'memory': memory_scores,
            'disk': disk_scores,
            'overall': overall,
        }
