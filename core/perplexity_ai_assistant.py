"""
Perplexity AI Integration Module
==================================
Integrates Perplexity AI as the PRIMARY reasoning engine for SysOptima.

Architecture:
1. Fetch real system data from local APIs
2. Build context with system metrics and user query
3. Send to Perplexity API for intelligent reasoning
4. Return formatted response to UI

The Perplexity AI assistant provides:
- Natural language understanding
- System analysis and reasoning
- Actionable recommendations
- Conversational responses based on actual system data
"""

import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import Config
from core.ai_system_api import get_ai_api


class PerplexityAIAssistant:
    """
    Perplexity AI Assistant for SysOptima.
    
    Uses Perplexity API for intelligent system analysis and diagnostics.
    """
    
    def __init__(self):
        """Initialize Perplexity AI Assistant"""
        self.api_key = Config.PERPLEXITY_API_KEY
        self.model = Config.PERPLEXITY_MODEL
        self.api_base = Config.PERPLEXITY_API_BASE_URL
        self.connected = False
        self.error_message = ""
        self.system_api = get_ai_api()
        
        # Verify configuration
        if self._verify_configuration():
            self._test_connection()
        else:
            self.error_message = "Perplexity API not properly configured"
    
    def _verify_configuration(self) -> bool:
        """Verify Perplexity configuration from .env"""
        if not self.api_key or len(self.api_key) < 10:
            self.error_message = "PERPLEXITY_API_KEY not found or invalid in .env"
            return False
        
        if not self.model:
            self.error_message = "PERPLEXITY_MODEL not configured"
            return False
        
        if not self.api_base:
            self.error_message = "PERPLEXITY_API_BASE_URL not configured"
            return False
        
        return True
    
    def _test_connection(self) -> bool:
        """Test Perplexity API connection with a minimal request"""
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "OK"}],
                    "max_tokens": 5,
                    "temperature": 0.7
                },
                timeout=10
            )
            
            if response.status_code == 200:
                self.connected = True
                return True
            else:
                try:
                    error_detail = response.json().get('error', {}).get('message', '')
                    self.error_message = f"API error: {response.status_code} - {error_detail}"
                except:
                    self.error_message = f"API test failed: {response.status_code}"
                return False
                
        except requests.exceptions.Timeout:
            self.error_message = "Connection timeout - Perplexity API not responding"
            return False
        except requests.exceptions.ConnectionError:
            self.error_message = "Connection refused - Cannot reach Perplexity API"
            return False
        except Exception as e:
            self.error_message = f"Test failed: {str(e)}"
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def check_api_connection(self) -> Dict[str, Any]:
        """Check Perplexity API connection status"""
        return {
            'connected': self.connected,
            'model': self.model if self.connected else None,
            'provider': 'Perplexity AI',
            'error': self.error_message
        }
    
    def get_system_context_for_query(self, metrics: Dict[str, Any] = None) -> str:
        """
        Build system context for Perplexity to use in reasoning.
        Fetches real data from local APIs.
        """
        try:
            if not metrics:
                metrics = self.system_api.get_metrics()
            
            hardware = self.system_api.get_hardware_info()
        except:
            metrics = {}
            hardware = {}
        
        context = f"""
SYSTEM STATUS DATA (Real-time):

CPU Performance:
  • Current Usage: {metrics.get('cpu', {}).get('percent', 'N/A')}%
  • Status: {metrics.get('cpu', {}).get('status', 'Unknown')}
  • Cores: {metrics.get('cpu', {}).get('cores', 'N/A')} physical, {metrics.get('cpu', {}).get('logical_cores', 'N/A')} logical
  • Model: {hardware.get('cpu', {}).get('model', 'Unknown')}
  • Frequency: {metrics.get('cpu', {}).get('frequency_ghz', 'N/A')} GHz

Memory (RAM):
  • Usage: {metrics.get('ram', {}).get('percent', 'N/A')}%
  • Status: {metrics.get('ram', {}).get('status', 'Unknown')}
  • Used: {metrics.get('ram', {}).get('used_gb', 'N/A')}GB / {metrics.get('ram', {}).get('total_gb', 'N/A')}GB
  • Available: {metrics.get('ram', {}).get('available_gb', 'N/A')}GB

Storage (Disk):
  • Usage: {metrics.get('disk', {}).get('percent', 'N/A')}%
  • Status: {metrics.get('disk', {}).get('status', 'Unknown')}
  • Used: {metrics.get('disk', {}).get('used_gb', 'N/A')}GB / {metrics.get('disk', {}).get('total_gb', 'N/A')}GB
  • Free: {metrics.get('disk', {}).get('free_gb', 'N/A')}GB

GPU (Graphics):
  • Name: {metrics.get('gpu', {}).get('name', 'Not detected')}
  • VRAM: {metrics.get('gpu', {}).get('vram_gb', 'N/A')}GB
  • Usage: {metrics.get('gpu', {}).get('vram_used_percent', 'N/A')}%

System Health: {metrics.get('system_health', 'Unknown')}
Processes Running: {metrics.get('processes_running', 'N/A')}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return context
    
    def get_perplexity_response(self, query: str, metrics: Dict[str, Any] = None) -> str:
        """
        Get response from Perplexity AI.
        
        Flow:
        1. Build system context with real data
        2. Send query + context to Perplexity
        3. Return formatted response
        """
        if not self.connected:
            return "🔴 AI OFFLINE – Local Diagnostic Mode\n\nPerplexity API is currently unavailable.\nThe system will automatically reconnect when available."
        
        if not query or len(query.strip()) < 2:
            return "Please ask a valid question about your system."
        
        try:
            # Get system context
            system_context = self.get_system_context_for_query(metrics)
            
            # Build the prompt
            system_prompt = f"""You are SysOptima's AI Assistant, powered by Perplexity AI.
You are a knowledgeable system analyst helping users understand and optimize their computer performance.

Your responsibilities:
1. Analyze the provided REAL SYSTEM DATA
2. Answer user questions about their system
3. Provide actionable recommendations
4. Explain technical concepts clearly
5. Be specific and reference actual metrics when relevant

Remember:
- Base all advice on the REAL DATA provided
- Provide concise, clear responses (max 300 words)
- Use simple language when possible
- Be honest about limitations
- Suggest professional help for complex hardware issues
- Focus on education and practical solutions

{system_context}"""
            
            # Make API call to Perplexity
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            # Handle response
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    ai_response = data['choices'][0]['message']['content']
                    return self._format_response(ai_response)
                else:
                    return "Perplexity could not generate a response. Please try again."
            else:
                error = response.json().get('error', {})
                message = error.get('message', f'Status {response.status_code}')
                return f"⚠️ API Error: {message[:150]}"
        
        except requests.exceptions.Timeout:
            return "⚠️ Request timeout. Please try again."
        except requests.exceptions.ConnectionError:
            self.connected = False
            return "❌ Connection lost to Perplexity API. Switching to offline mode."
        except Exception as e:
            return f"⚠️ Error: {str(e)[:150]}"
    
    def _format_response(self, text: str) -> str:
        """Format Perplexity response for UI"""
        text = text.strip()
        # Ensure response is readable
        if len(text) > 2000:
            text = text[:2000] + "...\n\n[Response truncated]"
        return text


# Singleton instance
_perplexity_instance = None

def get_perplexity_ai() -> PerplexityAIAssistant:
    """Get or create singleton Perplexity instance"""
    global _perplexity_instance
    if _perplexity_instance is None:
        _perplexity_instance = PerplexityAIAssistant()
    return _perplexity_instance
