"""
SysOptima AI Assistant Module
=============================
Primary AI Integration - Now uses Perplexity AI

This module provides HybridAILogic that coordinates AI assistance:
1. Uses Perplexity AI for reasoning and analysis (PRIMARY)
2. Uses local system APIs for real-time data
3. Graceful fallback when APIs unavailable

All responses are AI-generated using real system data.
"""

import os
import sys
from typing import Optional, Dict, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import Config
from core.ai_system_api import get_ai_api
from core.perplexity_ai_assistant import get_perplexity_ai
from core.groq_ai_assistant import get_groq_ai


class HybridAILogic:
    """
    AI Logic Controller: Perplexity AI + Graceful Fallback
    
    Priority:
    1. Special Commands (help, status, clear, test API)
    2. Perplexity API for intelligent responses using real system data
    3. Fallback diagnostics if Perplexity unavailable
    
    This is the ONLY AI interface in SysOptima.
    All responses go through this controller.
    """
    
    def __init__(self):
        self.ai_mode = Config.AI_MODE
        if self.ai_mode == "groq":
            self.ai_engine = get_groq_ai()
        else:
            self.ai_engine = get_perplexity_ai()
        self.system_api = get_ai_api()
    
    def process_query(self, query: str, system_metrics: Dict[str, Any] = None) -> str:
        """
        Process user query using Perplexity AI.
        
        Flow:
        1. Handle special commands
        2. Fetch real system metrics
        3. Send to Perplexity with context
        4. Return intelligent response
        """
        if not query:
            return "Please ask a question about your system."
        
        query_lower = query.lower().strip()
        
        # ====================================================
        # Special Commands (Non-AI)
        # ====================================================
        
        if query_lower == "help":
            return self._handle_help()
        
        if query_lower == "status":
            return self._handle_status()
        
        if query_lower == "clear":
            # Handled by UI, just acknowledge
            return "Chat cleared."
        
        if any(x in query_lower for x in ['hello perplexity', 'test perplexity', 'hello ai', 'test ai', 'check api', 'ai status']):
            return self._handle_api_test()
        
        # ====================================================
        # Main AI Processing - Perplexity
        # ====================================================
        
        try:
            # Fetch real system metrics for context
            if system_metrics is None:
                system_metrics = self.system_api.get_metrics()
            
            # Use configured AI for intelligent response
            if self.ai_engine.connected:
                if self.ai_mode == "groq":
                    return self.ai_engine.get_groq_response(query, system_metrics)
                else:
                    return self.ai_engine.get_perplexity_response(query, system_metrics)
            else:
                # Graceful fallback when offline
                return self._provide_fallback_response(query, system_metrics)
        
        except Exception as e:
            return f"Error processing query: {str(e)[:100]}"
    
    def _handle_help(self) -> str:
        """Show help information"""
        ai_name = "Perplexity AI" if self.ai_mode == "perplexity" else ("Groq AI" if self.ai_mode == "groq" else "Google Gemini")
        return f"""🤖 SysOptima AI Assistant (Powered by {ai_name})

I'm your intelligent system optimization assistant using {ai_name} reasoning.

WHAT I CAN HELP WITH:
  • Why is my CPU/RAM/GPU usage high?
  • What processes are using most resources?
  • Is my system performance good?
  • How can I improve performance?
  • Should I upgrade any components?
  • Is my PC good for gaming?
  • What's causing my system to lag?
  • How much RAM/storage do I need?
  • Memory leak diagnostics
  • Disk optimization advice
  • GPU performance analysis
  • System bottleneck identification

SPECIAL COMMANDS:
  • "status" - Show current system metrics
  • "hello perplexity" - Test AI connection
  • "help" - Show this help message
  • "clear" - Clear chat history

I use REAL SYSTEM DATA to analyze your specific situation
and provide actionable, personalized recommendations."""
    
    def _handle_status(self) -> str:
        """Show current system status with metrics"""
        try:
            metrics = self.system_api.get_metrics()
            
            # Determine overall health emoji
            health = metrics.get('system_health', 'Unknown')
            health_emoji = {
                'Excellent': '✅',
                'Good': '✅',
                'Fair': '⚠️',
                'Poor': '🔴'
            }.get(health, '❓')
            
            status = f"""{health_emoji} CURRENT SYSTEM STATUS

📊 CPU:
   • Usage: {metrics.get('cpu', {}).get('percent', 'N/A')}% ({metrics.get('cpu', {}).get('status', 'Unknown')})
   • Cores: {metrics.get('cpu', {}).get('cores', 'N/A')} physical / {metrics.get('cpu', {}).get('logical_cores', 'N/A')} logical
   • Frequency: {metrics.get('cpu', {}).get('frequency_ghz', 'N/A')} GHz

💾 MEMORY (RAM):
   • Usage: {metrics.get('ram', {}).get('percent', 'N/A')}% ({metrics.get('ram', {}).get('status', 'Unknown')})
   • Used: {metrics.get('ram', {}).get('used_gb', 'N/A')}GB / {metrics.get('ram', {}).get('total_gb', 'N/A')}GB
   • Available: {metrics.get('ram', {}).get('available_gb', 'N/A')}GB

💽 STORAGE (DISK):
   • Usage: {metrics.get('disk', {}).get('percent', 'N/A')}% ({metrics.get('disk', {}).get('status', 'Unknown')})
   • Used: {metrics.get('disk', {}).get('used_gb', 'N/A')}GB / {metrics.get('disk', {}).get('total_gb', 'N/A')}GB
   • Free: {metrics.get('disk', {}).get('free_gb', 'N/A')}GB

🎮 GPU:
   • {metrics.get('gpu', {}).get('name', 'Not detected')}
   • VRAM: {metrics.get('gpu', {}).get('vram_gb', '?')}GB (Usage: {metrics.get('gpu', {}).get('vram_used_percent', '?')}%)

⚡ SYSTEM HEALTH: {health}
   Processes Running: {metrics.get('processes_running', 'Unknown')}
   Updated: {datetime.now().strftime('%H:%M:%S')}"""
            
            return status
        except Exception as e:
            return f"Error retrieving status: {str(e)}"
    
    def _handle_api_test(self) -> str:
        """Test AI API connection"""
        status = self.ai_engine.check_api_connection()
        
        if status['connected']:
            return f"""✅ AI System Status: ONLINE

           Provider: {status['provider']}
   Model: {status['model']}
   Status: Ready for intelligent analysis
   
{status['provider']} is actively connected and ready to analyze your system."""
        else:
            return f"""❌ AI System Status: OFFLINE

   Provider: {status['provider']}
   Error: {status['error']}
   Mode: Fallback diagnostics (limited capability)
   
The AI will automatically reconnect when available."""
    
    def _provide_fallback_response(self, query: str, metrics: Dict[str, Any]) -> str:
        """
        Provide fallback diagnostic guidance when AI is unavailable.
        This is a limited, rule-based fallback.
        """
        
        query_lower = query.lower()
        ai_name = "Perplexity AI" if self.ai_mode == "perplexity" else ("Groq AI" if self.ai_mode == "groq" else "Google Gemini")
        
        # Extract metrics
        cpu_pct = metrics.get('cpu', {}).get('percent', 50)
        ram_pct = metrics.get('ram', {}).get('percent', 50)
        disk_pct = metrics.get('disk', {}).get('percent', 50)
        
        # Pattern matching for common questions
        if any(x in query_lower for x in ['cpu', 'processor', 'usage high', 'slow']):
            if cpu_pct > 80:
                return f"""⚠️ HIGH CPU USAGE ({cpu_pct}%)

Your CPU is under heavy load. Suggestions:
  • Close unnecessary programs
  • Check Task Manager for resource-heavy processes
  • Disable startup programs
  • Restart your computer if needed

Status: AI is offline - using basic diagnostics
Connect to {ai_name} for detailed analysis."""
            else:
                return f"""📊 CPU Status: {cpu_pct}% - Normal

Your CPU is performing adequately.

Status: AI is offline - limited analysis available
Connect to {ai_name} for full diagnostic report."""
        
        if any(x in query_lower for x in ['ram', 'memory', 'memory usage', 'memory leak']):
            if ram_pct > 85:
                return f"""⚠️ HIGH MEMORY USAGE ({ram_pct}%)

Your RAM is almost full. Try:
  • Close unused browser tabs
  • Close memory-intensive applications
  • Check for memory leaks in Task Manager
  • Restart your computer
  • Consider upgrading RAM

Status: AI is offline - basic guidance only
Enable AI for detailed memory analysis."""
            else:
                return f"""💾 Memory Status: {ram_pct}% - Healthy

Your RAM usage is within normal range.

Status: AI is offline - limited analysis
Reconnect to {ai_name} for optimization tips."""
        
        if any(x in query_lower for x in ['gaming', 'games', 'fps', 'gaming performance']):
            try:
                gaming = self.system_api.assess_gaming_performance()
                return f"""🎮 GAMING PERFORMANCE TIER: {gaming.get('tier', 'Unknown')}

Estimated Performance:
  • 1080p: ~{gaming.get('estimated_fps_1080p', '?')} fps
  • 1440p: ~{gaming.get('estimated_fps_1440p', '?')} fps
  • 4K: ~{gaming.get('estimated_fps_4k', '?')} fps

Recommendations:
  • {chr(10).join(['  • ' + r for r in gaming.get('recommendations', ['Check AI for details'])])}

Status: AI is offline - basic assessment
Reconnect {ai_name} for detailed gaming analysis."""
            except:
                return f"""🎮 Gaming Assessment Unavailable

Unable to assess gaming performance at this moment.
Reconnect to {ai_name} for detailed analysis."""
        
        # Default fallback
        return """ℹ️ AI OFFLINE – Limited Diagnostic Mode

I'm currently operating in offline mode with reduced capability.

What you can still do:
  • View system metrics with "status"
  • Get basic CPU/RAM/Disk guidance
  • Simple resource diagnostics

What you CANNOT do (AI offline):
  • Intelligent system analysis
  • Detailed performance recommendations
  • Context-aware optimization
  • Complex diagnostics

To restore full AI capability:
  • Check your internet connection
  • Verify {ai_name} API is accessible
  • Ensure API key is set in .env
  • Restart the application

The AI will automatically reconnect when available."""
