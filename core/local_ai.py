"""
SysOptima Hybrid Intelligence Engine
Combines Local System Data with Google Gemini AI for advanced reasoning.
"""

import psutil
import platform
import google.generativeai as genai
import sys
import os

# Add project root to path to import core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config import Config

try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

class LocalIntelligenceEngine:
    def __init__(self):
        self.use_gemini = False
        
        # Secure Configuration Check
        if Config.is_ai_enabled():
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.get_model_name())
                self.use_gemini = True
                print(f"Gemini AI Initialized (Model: {Config.get_model_name()})")
            except Exception as e:
                print(f"Gemini configuration failed: {e}. Fallback to Local Rules.")
        else:
             print("Gemini API Key missing in .env. Using Local Rules only.")

    def process_query(self, query):
        """
        Main entry point.
        Strategy:
        1. Gather Context (Metrics + Specs).
        2. Attempt Gemini Call (Hybrid Mode).
        3. Fallback to Local Rules if Gemini fails or is offline.
        """
        query_safe = query.lower()
        context = self._gather_full_context()
        
        # STEP 1: Hybrid Execution (Gemini)
        if self.use_gemini:
            try:
                response = self._call_gemini(query, context)
                if response:
                    return response
            except Exception as e:
                print(f"Gemini Error: {e}")
                # Fallthrough to local

        # STEP 2: Local Rule-Based Fallback
        return self._process_local_rules(query, query_safe)

    def _call_gemini(self, query, context):
        """Send data context + user query to Google AI"""
        prompt = f"""
        You are SysOptima AI – A Google Gemini Powered System Analyst.
        Your goal is to explain system performance like a professional consultant.
        
        LIVE SYSTEM DATA:
        {context}
        
        USER QUERY: "{query}"
        
        INSTRUCTIONS:
        1. Analyze the system data relative to the user's question.
        2. If the user asks about "Is it good?", "Why slow?", "Upgrade", use the data to justify your answer.
        3. Be concise, professional, and helpful. Use bullet points if listing items.
        4. If the data shows high usage (>85%), suggest specific actions (e.g., close apps, upgrade RAM).
        5. For Gaming, classify as Low/Medium/High tier based on the specs provided.
        
        Respond in natural language (no JSON).
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def _gather_full_context(self):
        """Bundle all local sensors for AI context"""
        metrics = self._get_metrics()
        specs = self._get_hardware_specs()
        
        return (f"CPU: {metrics['cpu']}% Load ({specs['cpu_name']}, {specs['cpu_cores']} Cores)\n"
                f"RAM: {metrics['ram_pct']}% Used ({metrics['ram_used_gb']}GB / {metrics['ram_total_gb']}GB)\n"
                f"Disk: {metrics['disk_pct']}% Used\n"
                f"GPU: {specs.get('gpu_name', 'Unknown')} ({specs.get('gpu_vram', 0)} MB VRAM)\n"
                f"GPU Type: {specs.get('gpu_type', 'Unknown')}\n")

    def _process_local_rules(self, query, query_safe):
        """Legacy local rule engine for fallback"""
        intent = self._detect_intent(query_safe)
        
        if intent == "ram": return self._analyze_ram()
        elif intent == "cpu": return self._analyze_cpu()
        elif intent == "gpu": return self._analyze_gpu()
        elif intent == "disk": return self._analyze_disk()
        elif intent == "gaming": return self._analyze_gaming_capability()
        elif intent == "upgrade": return self._analyze_upgrade_advice()
        elif intent == "health": return self._analyze_general_health()
        
        if "hello" in query_safe:
             return "SysOptima AI Online (Local Mode). I can check RAM, CPU, or Gaming specs."
             
        return self._analyze_general_health()

    # --- Local Helpers ---

    def _detect_intent(self, query):
        if any(w in query for w in ["ram", "memory"]): return "ram"
        if any(w in query for w in ["cpu", "processor", "slow", "lag"]): return "cpu"
        if any(w in query for w in ["gpu", "graphics", "video card", "fps"]): return "gpu"
        if any(w in query for w in ["disk", "storage", "space", "drive"]): return "disk"
        if any(w in query for w in ["game", "gaming", "play", "run"]): return "gaming"
        if any(w in query for w in ["upgrade", "suggest", "better", "buy"]): return "upgrade"
        return "health"

    def _get_metrics(self):
        return {
            "cpu": psutil.cpu_percent(interval=0.1),
            "ram_pct": psutil.virtual_memory().percent,
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "disk_pct": psutil.disk_usage('/').percent
        }

    def _get_hardware_specs(self):
        specs = {
            "cpu_name": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "gpu_name": "Integrated Graphics",
            "gpu_vram": 0.0,
            "gpu_type": "Integrated"
        }
        
        if HAS_GPU:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    specs["gpu_name"] = gpus[0].name
                    specs["gpu_type"] = "Dedicated"
                    specs["gpu_vram"] = round(gpus[0].memoryTotal / 1024, 2)
            except: pass
        return specs

    # --- Legacy Rule Analysis Methods (Fallback) ---
    def _analyze_ram(self):
        m = self._get_metrics()
        status = "Normal" if m["ram_pct"] < 70 else "Moderate" if m["ram_pct"] < 85 else "High"
        return f"[Local] RAM Status: {status} ({m['ram_pct']}%) used of {m['ram_total_gb']} GB."

    def _analyze_cpu(self):
        cpu = psutil.cpu_percent(interval=0.1)
        return f"[Local] CPU Load: {cpu}%. {'High load detected.' if cpu > 80 else 'Normal operation.'}"
    
    def _analyze_gpu(self):
        return "[Local] GPU data available in Hardware tab."

    def _analyze_disk(self):
         m = self._get_metrics()
         return f"[Local] Disk Usage: {m['disk_pct']}%."

    def _analyze_gaming_capability(self):
        specs = self._get_hardware_specs()
        tier = "High" if specs["ram_gb"] >= 16 and specs["gpu_type"] == "Dedicated" else "Low"
        return f"[Local] Gaming Tier: {tier}. (Based on {specs['ram_gb']}GB RAM and {specs['gpu_type']} GPU)"

    def _analyze_upgrade_advice(self):
        return "[Local] Consider 16GB RAM and a Dedicated GPU for best performance."

    def _analyze_general_health(self):
        m = self._get_metrics()
        return f"[Local] Health Overview: CPU {m['cpu']}%, RAM {m['ram_pct']}%, Disk {m['disk_pct']}%."
