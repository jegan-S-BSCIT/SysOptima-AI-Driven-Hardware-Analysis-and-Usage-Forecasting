"""
Diagnostics Module
Rule-based problem detection and recommendations
"""

class SystemDiagnostics:
    """Analyzes system performance and provides recommendations"""
    
    def __init__(self):
        self.issues = []
        self.recommendations = []
    
    def analyze_cpu(self, cpu_info, cpu_score):
        """Analyze CPU performance and detect issues"""
        issues = []
        recommendations = []
        
        # Check CPU score
        if cpu_score < 30:
            issues.append("CPU performance is below average")
            recommendations.append("Consider upgrading to a newer CPU")
        elif cpu_score < 50:
            issues.append("CPU performance is moderate")
            recommendations.append("Close background applications to free up CPU resources")
        
        # Check CPU usage
        if cpu_info.get('cores', 0) < 4:
            issues.append("Low core count may limit multitasking")
            recommendations.append("Consider upgrading to a CPU with more cores")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def analyze_memory(self, ram_info, memory_score):
        """Analyze memory performance and detect issues"""
        issues = []
        recommendations = []
        
        total_gb = ram_info.get('total_gb', 0)
        used_percent = ram_info.get('percent', 0)
        
        # Check RAM capacity
        if total_gb < 8:
            issues.append("Low RAM capacity (< 8GB)")
            recommendations.append("Upgrade to at least 8GB RAM for better performance")
        elif total_gb < 16:
            issues.append("Moderate RAM capacity")
            recommendations.append("Consider upgrading to 16GB+ for demanding applications")
        
        # Check RAM usage
        if used_percent > 90:
            issues.append("Critical RAM usage (>90%)")
            recommendations.append("Close unnecessary applications or add more RAM")
        elif used_percent > 75:
            issues.append("High RAM usage (>75%)")
            recommendations.append("Monitor memory-intensive applications")
        
        # Check memory score
        if memory_score < 40:
            issues.append("Memory performance is below average")
            recommendations.append("Check for slow RAM speeds or consider upgrading")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def analyze_disk(self, disk_info, disk_score):
        """Analyze disk performance and detect issues"""
        issues = []
        recommendations = []
        
        # Check disk score
        if disk_score < 30:
            issues.append("Disk performance is slow")
            recommendations.append("Consider upgrading to an SSD if using HDD")
        elif disk_score < 50:
            issues.append("Disk performance is moderate")
            recommendations.append("Ensure disk is not fragmented (HDD) or nearly full")
        
        # Check disk space
        for disk in disk_info:
            if disk.get('percent', 0) > 90:
                issues.append(f"Disk {disk.get('device')} is almost full (>90%)")
                recommendations.append(f"Free up space on {disk.get('device')}")
            elif disk.get('percent', 0) > 80:
                issues.append(f"Disk {disk.get('device')} is getting full (>80%)")
                recommendations.append(f"Consider cleaning up {disk.get('device')}")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def analyze_gpu(self, gpu_info):
        """Analyze GPU and detect issues"""
        issues = []
        recommendations = []
        
        if not gpu_info or not gpu_info[0].get('available', True):
            issues.append("No dedicated GPU detected")
            recommendations.append("Consider adding a dedicated GPU for gaming/graphics work")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def generate_full_report(self, hardware_info, benchmark_scores):
        """Generate comprehensive diagnostic report"""
        report = {
            'cpu': self.analyze_cpu(
                hardware_info.get('cpu', {}),
                benchmark_scores.get('cpu', {}).get('overall', 0)
            ),
            'memory': self.analyze_memory(
                hardware_info.get('ram', {}),
                benchmark_scores.get('memory', {}).get('overall', 0)
            ),
            'disk': self.analyze_disk(
                hardware_info.get('disk', []),
                benchmark_scores.get('disk', {}).get('overall', 0)
            ),
            'gpu': self.analyze_gpu(hardware_info.get('gpu', []))
        }
        
        # Compile all issues and recommendations
        all_issues = []
        all_recommendations = []
        
        for component, analysis in report.items():
            all_issues.extend(analysis['issues'])
            all_recommendations.extend(analysis['recommendations'])
        
        report['summary'] = {
            'total_issues': len(all_issues),
            'all_issues': all_issues,
            'all_recommendations': all_recommendations
        }
        
        return report
