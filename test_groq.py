import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.gemini_ai_assistant import HybridAILogic

import json
def test_groq():
    ai = HybridAILogic()
    
    out = {
        "status": ai._handle_api_test(),
        "error": getattr(ai.ai_engine, 'error_message', 'No attribute'),
        "connected": getattr(ai.ai_engine, 'connected', 'No attribute')
    }
    
    metrics = {
        'cpu': {'percent': 50, 'status': 'Normal', 'cores': 4, 'logical_cores': 8, 'frequency_ghz': 3.5},
        'ram': {'percent': 60, 'status': 'Normal', 'total_gb': 16, 'used_gb': 9.6, 'available_gb': 6.4},
        'disk': {'percent': 30, 'status': 'Normal', 'total_gb': 500, 'used_gb': 150, 'free_gb': 350},
        'gpu': {'name': 'Test GPU', 'vram_gb': 4, 'vram_used_percent': 20},
        'system_health': 'Good',
        'processes_running': 100
    }
    out["response"] = ai.process_query("What do you think about my CPU?", metrics)
    
    with open('test_out.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    test_groq()
