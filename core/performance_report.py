"""
Performance reporting module for SysOptima
Generates and manages system performance reports with analysis
"""

from datetime import datetime, timedelta
from core.performance_analyzer import PerformanceAnalyzer
import psutil


class PerformanceReport:
    """Represents a system performance report"""
    
    def __init__(self, report_type: str = "quick", label: str = ""):
        self.report_type = report_type  # "quick", "full", "weekly"
        self.label = label or self._generate_label()
        self.timestamp = datetime.now()
        self.data = None
        self.status = "Pending"
    
    def _generate_label(self) -> str:
        """Generate report label based on type"""
        if self.report_type == "quick":
            return "Quick Performance Check"
        elif self.report_type == "full":
            return "Full System Scan"
        elif self.report_type == "weekly":
            return "Weekly Performance Summary"
        return "Performance Report"
    
    def generate(self):
        """Generate report data"""
        try:
            self.data = PerformanceAnalyzer.evaluate_system_performance()
            overall_score = self.data.get("overall_score", 0)
            
            if overall_score >= 75:
                self.status = "Excellent"
            elif overall_score >= 65:
                self.status = "Good"
            elif overall_score >= 55:
                self.status = "Moderate"
            else:
                self.status = "Needs Attention"
            
            return self.data
        except Exception as e:
            self.status = "Error"
            self.data = {
                "overall_score": 0,
                "cpu_score": 0,
                "memory_score": 0,
                "disk_score": 0,
                "status": "Error",
                "interpretation": f"Could not generate report: {str(e)}"
            }
            return self.data
    
    def get_summary(self) -> str:
        """Get one-line summary of report"""
        if not self.data:
            return "Report not generated"
        
        # Generate contextual summary
        cpu = self.data.get("cpu_score", 0)
        mem = self.data.get("memory_score", 0)
        disk = self.data.get("disk_score", 0)
        
        issues = []
        if cpu < 60:
            issues.append("High CPU usage")
        if mem < 60:
            issues.append("High memory pressure")
        if disk < 60:
            issues.append("Low disk space")
        
        if issues:
            return " · ".join(issues)
        
        if self.data.get("overall_score", 0) >= 75:
            return "All systems performing optimally"
        
        return "System performing within normal parameters"
    
    def get_status_color(self) -> str:
        """Get status indicator color"""
        status_colors = {
            "Excellent": "#00CC88",
            "Good": "#4BA3FF",
            "Moderate": "#FFB84D",
            "Needs Attention": "#FF6B6B",
            "Error": "#999999"
        }
        return status_colors.get(self.status, "#666666")
    
    def to_dict(self) -> dict:
        """Export report as dictionary"""
        return {
            "type": self.report_type,
            "label": self.label,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "data": self.data
        }


class PerformanceReportManager:
    """Manages collection of performance reports"""
    
    def __init__(self):
        self.reports = []
        self._generate_default_reports()
    
    def _generate_default_reports(self):
        """Generate default report set"""
        # Quick check (current)
        quick_report = PerformanceReport("quick", "Quick Performance Check")
        quick_report.generate()
        self.reports.append(quick_report)
        
        # Full scan (today)
        full_report = PerformanceReport("full", "Full System Scan")
        full_report.timestamp = datetime.now().replace(hour=10, minute=30)
        full_report.generate()
        self.reports.append(full_report)
        
        # Weekly (last week)
        weekly_report = PerformanceReport("weekly", "Weekly Performance Summary")
        weekly_report.timestamp = datetime.now() - timedelta(days=7)
        weekly_report.generate()
        self.reports.append(weekly_report)
    
    def add_report(self, report_type: str = "quick") -> PerformanceReport:
        """Create and add new report"""
        report = PerformanceReport(report_type)
        report.generate()
        self.reports.insert(0, report)  # Add to front
        return report
    
    def get_reports(self) -> list:
        """Get all reports (newest first)"""
        return sorted(self.reports, key=lambda r: r.timestamp, reverse=True)
    
    def get_latest_report(self) -> PerformanceReport:
        """Get most recent report"""
        if self.reports:
            return self.get_reports()[0]
        return None
    
    def get_report_by_index(self, index: int) -> PerformanceReport:
        """Get report by index"""
        reports = self.get_reports()
        if 0 <= index < len(reports):
            return reports[index]
        return None


def get_component_reason(component: str, score: float) -> str:
    """Get explanation for component score"""
    if component == "cpu":
        if score >= 80:
            return "CPU load is within optimal range"
        elif score >= 70:
            return "CPU performing well with good capacity"
        elif score >= 50:
            return "CPU load is moderate, may impact demanding tasks"
        else:
            return "CPU is heavily constrained"
    
    elif component == "memory":
        if score >= 80:
            return "Memory pressure is low, abundant capacity available"
        elif score >= 65:
            return "Memory usage is moderate and acceptable"
        elif score >= 45:
            return "High memory usage detected, may affect multitasking"
        else:
            return "Memory is critically constrained"
    
    elif component == "disk":
        if score >= 80:
            return "Ample free disk space available"
        elif score >= 65:
            return "Disk usage is adequate"
        elif score >= 45:
            return "Disk usage exceeds recommended threshold"
        else:
            return "Disk is critically full"
    
    return "Unable to assess"


def get_performance_interpretation(cpu_score, memory_score, disk_score, overall_score) -> str:
    """Generate detailed interpretation of performance status"""
    
    # Determine overall status
    if overall_score >= 75:
        status = "excellent"
        status_text = "The system performance is excellent."
    elif overall_score >= 65:
        status = "good"
        status_text = "The system performance is good."
    elif overall_score >= 55:
        status = "moderate"
        status_text = "The system performance is moderate."
    else:
        status = "poor"
        status_text = "The system performance needs attention."
    
    # Count issues
    issues = []
    if cpu_score < 65:
        issues.append("CPU performance is constrained")
    if memory_score < 65:
        issues.append("memory usage is higher than optimal")
    if disk_score < 65:
        issues.append("disk usage is concerning")
    
    # Build interpretation
    if issues:
        interpretation = status_text + " " + ", ".join(issues) + ", which may affect multitasking and application responsiveness."
    else:
        interpretation = status_text + " All components are performing within normal parameters."
    
    return interpretation


def get_usage_capability_forecast(cpu_score, memory_score, disk_score, overall_score) -> dict:
    """Generate capability forecast for different use cases"""
    
    # Determine suitability based on scores
    def get_suitability(score):
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 55:
            return "Moderate"
        else:
            return "Not Recommended"
    
    # General use is always possible
    general = "Excellent"
    
    # Programming depends on memory and CPU
    programming_score = (cpu_score * 0.5 + memory_score * 0.5)
    programming = get_suitability(programming_score)
    
    # Gaming needs good GPU and CPU
    gaming_score = (cpu_score * 0.6 + disk_score * 0.4)  # Disk for load times
    gaming = get_suitability(gaming_score)
    
    # Video editing 1080p
    video_1080_score = (memory_score * 0.4 + disk_score * 0.3 + cpu_score * 0.3)
    video_1080 = get_suitability(video_1080_score)
    
    # Video editing 4K (demanding)
    video_4k_score = (memory_score * 0.4 + disk_score * 0.3 + cpu_score * 0.3) - 10
    video_4k = get_suitability(video_4k_score)
    
    return {
        "General Use": general,
        "Programming": programming,
        "Gaming": gaming,
        "Video Editing (1080p)": video_1080,
        "Video Editing (4K)": video_4k
    }


def get_optimization_hints(cpu_score, memory_score, disk_score) -> list:
    """Generate optimization recommendations (2-3 max)"""
    hints = []
    
    if memory_score < 65:
        hints.append("Close unnecessary background applications to reduce memory pressure")
    
    if cpu_score < 65:
        hints.append("Monitor CPU usage during multitasking to identify resource-heavy processes")
    
    if disk_score < 60:
        hints.append("Consider freeing up disk space - performance may improve with more available storage")
    
    return hints[:3]  # Return max 3 hints
