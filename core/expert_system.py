"""
Expert System Module
Rule-based logic for the AI Chatbot
"""

class SystemExpert:
    """
    Determininstic Rule-Based Expert System for System Analysis.
    Does NOT use Neural Networks or LLMs.
    Uses IF-ELSE logic based on hardware thresholds.
    """
    
    def __init__(self):
        # Knowledge Base: Defined thresholds
        self.RAM_HIGH_THRESHOLD = 85.0  # %
        self.CPU_HIGH_THRESHOLD = 80.0  # %
        self.GAMING_min_RAM_GB = 8
        self.GAMING_min_CORES = 4
    
    def get_response(self, user_query, context):
        """
        Analyze the query and current system context to generate a response.
        
        Args:
            user_query (str): The question asked by the user.
            context (dict): Dictionary containing 'hardware' (static) and 'monitor' (live) data.
            
        Returns:
            str: The expert explanation.
        """
        query = user_query.lower()
        hardware = context.get('hardware', {})
        monitor = context.get('monitor', {})
        
        # --- Rule 1: Health Check ---
        if "health" in query or "healthy" in query or "status" in query:
            return self._analyze_health(monitor)

        # --- Rule 2: High Usage Analysis ---
        if "usage" in query or "high" in query:
            if "ram" in query or "memory" in query:
                return self._analyze_ram_usage(hardware, monitor)
            if "cpu" in query or "processor" in query:
                return self._analyze_cpu_usage(hardware, monitor)

        # --- Rule 3: Gaming Capability ---
        if "game" in query or "gaming" in query:
            return self._analyze_gaming_readiness(hardware)

        # --- Rule 4: Upgrade Advice ---
        if "upgrade" in query or "improve" in query:
            return self._analyze_upgrade_path(hardware, monitor)
            
        # --- Fallback ---
        return (
            "I am a rule-based system specialized in hardware analysis.\n"
            "I didn't understand that query. Try asking:\n"
            "- 'Is my system healthy?'\n"
            "- 'Can I run modern games?'\n"
            "- 'Why is my RAM usage high?'\n"
            "- 'What should I upgrade?'"
        )

    def _analyze_health(self, monitor):
        cpu_usage = monitor.get('cpu_percent', 0)
        ram_usage = monitor.get('ram_percent', 0)
        
        status = "Healthy"
        issues = []
        
        if cpu_usage > self.CPU_HIGH_THRESHOLD:
            status = "Under Heavy Load"
            issues.append(f"CPU usage is critical ({cpu_usage:.1f}%)")
            
        if ram_usage > self.RAM_HIGH_THRESHOLD:
            status = "Under Heavy Load"
            issues.append(f"RAM usage is critical ({ram_usage:.1f}%)")
            
        if not issues:
            return (
                f"Status: {status}\n\n"
                f"Your system is running normally.\n"
                f"CPU Load: {cpu_usage}%\n"
                f"RAM Load: {ram_usage}%\n"
                "Result: No immediate action required."
            )
        else:
            return (
                f"Status: {status}\n\n"
                f"Issues Detected:\n- " + "\n- ".join(issues) + "\n\n"
                "Recommendation: Close unused applications to free up resources."
            )

    def _analyze_ram_usage(self, hardware, monitor):
        ram_usage = monitor.get('ram_percent', 0)
        total_ram = hardware.get('ram', {}).get('total_gb', 0)
        
        explanation = f"Your RAM usage is currently at {ram_usage:.1f}%.\n"
        
        if ram_usage > self.RAM_HIGH_THRESHOLD:
            reason = "multitasking or memory-intensive applications"
            if total_ram < 8:
                reason = "having a low amount of total physical memory"
                
            explanation += (
                f"\nWhy: This high usage is likely due to {reason}.\n"
                f"Context: You have {total_ram} GB of total RAM.\n"
                "Action: Close browser tabs or background apps."
            )
        else:
            explanation += "\nThis is a normal level for daily tasks."
            
        return explanation

    def _analyze_cpu_usage(self, hardware, monitor):
        cpu_usage = monitor.get('cpu_percent', 0)
        cpu_name = hardware.get('cpu', {}).get('name', 'Unknown')
        
        return (
            f"CPU: {cpu_name}\n"
            f"Current Load: {cpu_usage:.1f}%\n\n"
            "Analysis: " + ("The processor is under heavy stress." if cpu_usage > self.CPU_HIGH_THRESHOLD 
                            else "The processor is handling current tasks comfortably.")
        )

    def _analyze_gaming_readiness(self, hardware):
        gpu = hardware.get('gpu', {})
        ram = hardware.get('ram', {})
        cpu = hardware.get('cpu', {})
        
        gpu_name = gpu.get('name', 'Unknown')
        ram_total = ram.get('total_gb', 0)
        
        # Simple keyword heuristic for GPU tiers
        is_dedicated = any(x in gpu_name.upper() for x in ['RTX', 'GTX', 'RADEON', 'RX', 'ARC'])
        is_high_end = 'RTX' in gpu_name.upper() or 'RX 6' in gpu_name.upper() or 'RX 7' in gpu_name.upper()
        
        verdict = "Entry-Level / Casual Gaming"
        if is_dedicated:
            verdict = "Capable of Mainstream Gaming"
        if is_high_end:
            verdict = "High-End Gaming Ready"
        if ram_total < self.GAMING_min_RAM_GB:
            verdict = "Not Recommended for Modern Gaming (Low RAM)"
            
        return (
            f"Gaming Capability Analysis\n"
            f"--------------------------\n"
            f"GPU: {gpu_name}\n"
            f"RAM: {ram_total} GB\n\n"
            f"Verdict: {verdict}\n\n"
            f"Reasoning:\n"
            f"1. GPU Type: {'Discrete/Dedicated' if is_dedicated else 'Integrated'}\n"
            f"2. RAM Capacity: {'Sufficient (>8GB)' if ram_total >= 8 else 'Insufficient (<8GB)'}"
        )

    def _analyze_upgrade_path(self, hardware, monitor):
        suggestions = []
        
        ram_total = hardware.get('ram', {}).get('total_gb', 0)
        if ram_total < 8:
            suggestions.append("RAM: Upgrade to at least 8GB (ideally 16GB) for smoother multitasking.")
        elif ram_total < 16:
             suggestions.append("RAM: Upgrading to 16GB would benefit heavy gaming or video editing.")
             
        disk = hardware.get('disk', {})
        # Heuristic: Small primary drive often implies generic SSD or old HDD
        if disk.get('total_gb', 0) < 250:
             suggestions.append("Storage: Your main drive is small. Consider adding a larger SSD.")
             
        if not suggestions:
            suggestions.append("Your core hardware (RAM/Storage) seems sufficient for general use.")
            suggestions.append("For performance, ensure you keep drivers updated.")
            
        return "Upgrade Recommendations:\n\n" + "\n\n".join(suggestions)
