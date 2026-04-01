"""
Diagnostics orchestration for SysOptima
"""

from typing import Dict

try:
    from analysis.diagnostics import SystemDiagnostics
except Exception:
    SystemDiagnostics = None

class DiagnosticsEngine:
    """Runs diagnostics using available data"""
    def __init__(self):
        self.diagnostics = SystemDiagnostics() if SystemDiagnostics else None

    def run(self, hardware_info: Dict, scores: Dict) -> Dict:
        if not self.diagnostics:
            return {}
        return self.diagnostics.generate_full_report(hardware_info or {}, scores or {})
