"""
Performance Predictor Module
Predicts FPS and workload capabilities based on system performance
"""

class PerformancePredictor:
    """Predicts gaming performance and workload capabilities"""
    
    def __init__(self):
        # Reference FPS data for different game types
        self.game_requirements = {
            'light': {'cpu': 30, 'memory': 30, 'gpu': 20},  # e.g., indie games
            'medium': {'cpu': 50, 'memory': 50, 'gpu': 40},  # e.g., esports titles
            'heavy': {'cpu': 70, 'memory': 70, 'gpu': 60},  # e.g., AAA games
            'ultra': {'cpu': 85, 'memory': 85, 'gpu': 80}   # e.g., latest AAA games
        }
    
    def predict_fps(self, cpu_score, memory_score, gpu_score, game_type='medium'):
        """
        Predict FPS for a given game type
        
        Args:
            cpu_score: CPU performance score (0-100)
            memory_score: Memory performance score (0-100)
            gpu_score: GPU performance score (0-100)
            game_type: Type of game ('light', 'medium', 'heavy', 'ultra')
        
        Returns:
            Predicted FPS range
        """
        if game_type not in self.game_requirements:
            game_type = 'medium'
        
        requirements = self.game_requirements[game_type]
        
        # Calculate performance ratio for each component
        cpu_ratio = cpu_score / requirements['cpu']
        memory_ratio = memory_score / requirements['memory']
        gpu_ratio = gpu_score / requirements['gpu'] if gpu_score > 0 else 0.5
        
        # GPU is most important for gaming (60%), CPU (30%), Memory (10%)
        overall_ratio = (gpu_ratio * 0.6 + cpu_ratio * 0.3 + memory_ratio * 0.1)
        
        # Base FPS targets
        base_fps = {
            'light': 120,
            'medium': 90,
            'heavy': 60,
            'ultra': 45
        }
        
        predicted_fps = int(base_fps[game_type] * overall_ratio)
        
        # Determine quality settings
        if overall_ratio >= 1.5:
            quality = "Ultra"
        elif overall_ratio >= 1.0:
            quality = "High"
        elif overall_ratio >= 0.7:
            quality = "Medium"
        else:
            quality = "Low"
        
        return {
            'game_type': game_type,
            'predicted_fps': predicted_fps,
            'recommended_quality': quality,
            'performance_ratio': overall_ratio
        }
    
    def predict_workload_capability(self, cpu_score, memory_score, disk_score):
        """
        Predict capability for different workload types
        
        Args:
            cpu_score: CPU performance score
            memory_score: Memory performance score
            disk_score: Disk performance score
        
        Returns:
            Capability ratings for different workload types
        """
        workloads = {
            'office_productivity': {
                'weights': {'cpu': 0.3, 'memory': 0.5, 'disk': 0.2},
                'threshold': 40
            },
            'photo_editing': {
                'weights': {'cpu': 0.4, 'memory': 0.4, 'disk': 0.2},
                'threshold': 55
            },
            'video_editing': {
                'weights': {'cpu': 0.5, 'memory': 0.3, 'disk': 0.2},
                'threshold': 65
            },
            '3d_rendering': {
                'weights': {'cpu': 0.6, 'memory': 0.3, 'disk': 0.1},
                'threshold': 70
            },
            'programming_compiling': {
                'weights': {'cpu': 0.5, 'memory': 0.3, 'disk': 0.2},
                'threshold': 50
            },
            'virtual_machines': {
                'weights': {'cpu': 0.4, 'memory': 0.5, 'disk': 0.1},
                'threshold': 60
            }
        }
        
        capabilities = {}
        
        for workload, config in workloads.items():
            score = (
                cpu_score * config['weights']['cpu'] +
                memory_score * config['weights']['memory'] +
                disk_score * config['weights']['disk']
            )
            
            # Determine capability level
            if score >= config['threshold'] * 1.3:
                capability = "Excellent"
            elif score >= config['threshold']:
                capability = "Good"
            elif score >= config['threshold'] * 0.7:
                capability = "Fair"
            else:
                capability = "Limited"
            
            capabilities[workload] = {
                'score': round(score, 1),
                'capability': capability,
                'meets_requirements': score >= config['threshold']
            }
        
        return capabilities
    
    def predict_multitasking(self, cpu_info, memory_score):
        """
        Predict multitasking capability
        
        Args:
            cpu_info: CPU information
            memory_score: Memory performance score
        
        Returns:
            Multitasking capability assessment
        """
        cores = cpu_info.get('cores', 2)
        threads = cpu_info.get('threads', 2)
        
        # Score based on cores and memory
        core_score = min((cores / 8) * 100, 100)  # 8 cores = 100%
        thread_score = min((threads / 16) * 100, 100)  # 16 threads = 100%
        
        combined_score = (core_score * 0.4 + thread_score * 0.3 + memory_score * 0.3)
        
        if combined_score >= 80:
            level = "Excellent - Handle many concurrent tasks"
        elif combined_score >= 60:
            level = "Good - Handle moderate multitasking"
        elif combined_score >= 40:
            level = "Fair - Basic multitasking possible"
        else:
            level = "Limited - Focus on single tasks"
        
        return {
            'score': round(combined_score, 1),
            'level': level,
            'recommended_concurrent_apps': max(1, int(combined_score / 20))
        }
