"""
Diagnostics Module for SysOptima
==================================
- Rule-based diagnostics engine (no ML, no APIs)
- Explainable AI chat assistant
- Offline operation only
- Academic-grade implementation

For B.Sc. IT Project: "AI-Driven Hardware Analysis and Usage Forecasting"
"""

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psutil
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Optional OpenAI (cloud) client
try:
    from openai import OpenAI  # type: ignore
except Exception:
    OpenAI = None

# Optional Google Gemini (cloud) client
try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None

# Optional GPUtil
try:
    import GPUtil
except Exception:
    GPUtil = None


class DiagnosticsEngine:
    """
    Rule-based diagnostics engine (explainable, no APIs).
    
    Collects metrics and applies threshold-based rules to identify issues.
    Generates human-readable diagnostic reports with explanations.
    """
    
    def __init__(self):
        """Initialize diagnostics engine."""
        self.last_run = None
        self.current_metrics = {}
        self.diagnostics = []
    
    def run_diagnostics(self):
        """
        Collect metrics and run rule-based diagnostics.
        
        Returns:
            dict: {'metrics': {...}, 'diagnostics': [...], 'timestamp': ...}
        """
        self.last_run = datetime.now()
        self.current_metrics = self._collect_metrics()
        self.diagnostics = self._analyze_metrics()
        
        return {
            'metrics': self.current_metrics,
            'diagnostics': self.diagnostics,
            'timestamp': self.last_run
        }
    
    def _collect_metrics(self):
        """Collect current system metrics."""
        # Use interval=0 for non-blocking. 
        # First call may be 0.0, but subsequent calls will be accurate since last call.
        cpu_percent = psutil.cpu_percent(interval=0)
        # If we get 0.0 and it's the very first call, we might want a tiny sample, 
        # but for UI smoothness, we prefer 0 over lag.
        if cpu_percent == 0:
             # Fallback to a very short 0.1s sample ONLY if we got 0 (likely first run)
             # This maxes lag at 100ms which is acceptable for "Run Diagnostics" action
             cpu_percent = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        gpu_percent = 0.0
        gpu_available = False
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_percent = float(gpus[0].load * 100)
                    gpu_available = True
            except Exception:
                pass
        
        disk_io = psutil.disk_io_counters()
        
        return {
            'cpu_percent': cpu_percent,
            'ram_percent': ram.percent,
            'ram_available_gb': ram.available / (1024 ** 3),
            'ram_total_gb': ram.total / (1024 ** 3),
            'gpu_percent': gpu_percent,
            'gpu_available': gpu_available,
            'disk_percent': disk.percent,
            'disk_free_gb': disk.free / (1024 ** 3),
            'disk_total_gb': disk.total / (1024 ** 3),
        }
    
    def _analyze_metrics(self):
        """Apply rule-based logic to detect issues."""
        issues = []
        m = self.current_metrics
        
        # Rule 1: High CPU usage
        if m['cpu_percent'] > 80:
            issues.append({
                'severity': 'HIGH' if m['cpu_percent'] > 90 else 'MEDIUM',
                'category': 'CPU',
                'issue': f"High CPU Usage ({m['cpu_percent']:.1f}%)",
                'what': f"Your CPU is working at {m['cpu_percent']:.1f}% capacity.",
                'why': "This means the processor is handling a heavy workload.",
                'caused_by': [
                    "Multiple applications running simultaneously",
                    "A single demanding program (game, video editor, compiler)",
                    "Background processes or system updates",
                    "Insufficient CPU cores for your tasks"
                ],
                'solutions': [
                    "Close unused applications to free CPU",
                    "Check Task Manager for resource-heavy processes",
                    "Reduce graphics settings in games or applications",
                    "Upgrade to a more powerful CPU if this is consistent"
                ]
            })
        
        # Rule 2: High RAM usage
        if m['ram_percent'] > 75:
            issues.append({
                'severity': 'HIGH' if m['ram_percent'] > 90 else 'MEDIUM',
                'category': 'RAM',
                'issue': f"High Memory Usage ({m['ram_percent']:.1f}%)",
                'what': f"You are using {m['ram_percent']:.1f}% of your total RAM ({m['ram_total_gb']:.1f} GB).",
                'why': "Your system has less available memory, which can slow down operations.",
                'caused_by': [
                    "Too many browser tabs or applications open",
                    "Memory leak in a running application",
                    "Large files being processed (video, 3D models)",
                    "Virtual memory being used (slower than RAM)"
                ],
                'solutions': [
                    f"You have {m['ram_available_gb']:.1f} GB free. Close unused apps.",
                    "Close web browsers with many tabs",
                    "Restart your computer to clear cache",
                    f"Consider upgrading RAM (current: {m['ram_total_gb']:.1f} GB)"
                ]
            })
        
        # Rule 3: GPU overload (if available)
        if m['gpu_available'] and m['gpu_percent'] > 85:
            issues.append({
                'severity': 'MEDIUM',
                'category': 'GPU',
                'issue': f"GPU Overload ({m['gpu_percent']:.1f}%)",
                'what': f"Your GPU is running at {m['gpu_percent']:.1f}% utilization.",
                'why': "The graphics processor is heavily loaded, which may cause frame drops.",
                'caused_by': [
                    "Running demanding games or 3D applications",
                    "Video encoding/decoding",
                    "AI/ML model training",
                    "Multiple GPU-intensive tasks"
                ],
                'solutions': [
                    "Lower graphics quality or resolution in games",
                    "Close other GPU-intensive applications",
                    "Improve room ventilation for better cooling",
                    "Upgrade your GPU if frame rates are consistently low"
                ]
            })
        
        # Rule 4: Disk space low
        if m['disk_percent'] > 90:
            issues.append({
                'severity': 'HIGH',
                'category': 'DISK',
                'issue': f"Low Disk Space ({m['disk_percent']:.1f}% used)",
                'what': f"Your disk is {m['disk_percent']:.1f}% full with only {m['disk_free_gb']:.1f} GB free.",
                'why': "Low disk space can slow down your system and prevent new installations.",
                'caused_by': [
                    "Large files (videos, games, backups) accumulating",
                    "Temporary files not being cleaned",
                    "Application cache growing over time",
                    "System files taking too much space"
                ],
                'solutions': [
                    f"Delete unnecessary files to free up space",
                    "Move large files to external storage",
                    "Run Disk Cleanup to remove temporary files",
                    "Uninstall unused applications"
                ]
            })
        
        # If no issues detected, return a positive diagnostic
        if not issues:
            issues.append({
                'severity': 'GOOD',
                'category': 'SYSTEM',
                'issue': "System Running Smoothly ✓",
                'what': "Your system is operating within normal parameters.",
                'why': "All hardware metrics are within healthy ranges.",
                'caused_by': [],
                'solutions': []
            })
        
        return issues


class AIAssistant:
    """
    AI assistant for answering system-related questions.
    
    Primary mode: rule-based, offline, explainable.
    Optional mode: cloud (OpenAI) if OPENAI_API_KEY is set and openai package is installed.
    """
    
    def __init__(self, diagnostics_engine):
        """
        Initialize AI assistant.
        
        Args:
            diagnostics_engine: DiagnosticsEngine instance for metric access
        """
        self.engine = diagnostics_engine
        self.chat_history = []
        self.response_variants = 0  # Track response variety
        self.openai_client = None
        self.use_openai = False
        self.gemini_model = None
        self.use_gemini = False
        
        # Intent keywords organized by category
        self.intents = {
            'cpu': ['cpu', 'processor', 'processor usage', 'processor load', 'cpu load', 'cpu high'],
            'ram': ['ram', 'memory', 'mem', 'slow', 'sluggish', 'laggy'],
            'gpu': ['gpu', 'graphics', 'video', 'graphics card', 'nvidia', 'amd'],
            'disk': ['disk', 'storage', 'space', 'full', 'ssd', 'hdd', 'hard drive'],
            'gaming': ['game', 'gaming', 'play', 'run game', 'fps', 'frames', 'minecraft', 'fortnite'],
            'performance': ['performance', 'improve', 'faster', 'speed', 'boost', 'optimize'],
            'fix': ['fix', 'problem', 'issue', 'crash', 'hang', 'freeze', 'not working', 'error'],
            'upgrade': ['upgrade', 'should i', 'need', 'worth', 'better', 'faster cpu', 'more ram']
        }

        # Initialize OpenAI client if configured
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and OpenAI:
            try:
                # OpenAI is optional; the rule engine stays primary when this fails or is absent.
                self.openai_client = OpenAI(api_key=api_key)
                self.use_openai = True
            except Exception:
                # Fallback silently to rule-based mode
                self.openai_client = None
                self.use_openai = False

        # Initialize Gemini client if configured (optional; rules remain primary)
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and genai:
            try:
                genai.configure(api_key=gemini_key)
                
                # List of models to try in order of preference
                candidates = ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro"]
                valid_model = None
                
                # Simple check logic: just pick the first one, runtime errors are handled in get_gemini_response.
                # But to avoid 404 at startup, we can just default to a known safe one. 
                # Let's pick 'gemini-pro' if 'flash' was giving trouble, or stick to 'gemini-1.5-flash' if we think it was just a transient issue?
                # The user explicitly saw a 404. Let's force 'gemini-pro' as it is widely available.
                # Actually, let's use the list_models() to find a valid one dynamically!
                
                try:
                    available_models = [m.name for m in genai.list_models()]
                    # Mapping of simplified names to full API names if needed
                    preferred_order = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-pro-latest"]
                    
                    found_model = None
                    for pref in preferred_order:
                        if pref in available_models:
                            found_model = pref
                            break
                    
                    if not found_model:
                        # Fallback: search for ANY 'gemini' model containing 'generateContent'
                        for m in genai.list_models():
                            if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name:
                                found_model = m.name
                                break
                    
                    model_name = found_model if found_model else "gemini-1.5-flash"
                except Exception:
                    model_name = "gemini-1.5-flash" # Fallback if list_models fails

                self.gemini_model = genai.GenerativeModel(model_name)
                self.use_gemini = True
            except Exception:
                self.gemini_model = None
                self.use_gemini = False

    def check_openai_connection(self):
        """Tiny connectivity check for the optional OpenAI client."""
        if not self.use_openai or not self.openai_client:
            return False, "OpenAI not configured; staying in offline rule-based mode."

        try:
            ping = self.openai_client.responses.create(
                model="gpt-4o-mini",
                input=[{"role": "user", "content": "Reply with pong"}],
            )

            text_out = None
            try:
                text_out = ping.output_text
            except Exception:
                pass
            if not text_out and hasattr(ping, "content") and isinstance(ping.content, list):
                text_out = str(ping.content[0].get("text", "")).strip()

            if text_out and "pong" in text_out.lower():
                return True, "Received pong from OpenAI."
            return False, "Unexpected response while checking OpenAI."
        except Exception as exc:  # Network/auth/rate-limit issues fall here
            return False, str(exc)

    def check_gemini_connection(self):
        """Minimal connectivity check for optional Gemini client."""
        if not self.use_gemini or not self.gemini_model:
            return False, "Gemini not configured; staying in offline rule-based mode."

        try:
            ping = self.gemini_model.generate_content("Return the word pong")
            text_out = getattr(ping, "text", "") or "".join(getattr(ping, "candidates", []))
            if "pong" in text_out.lower():
                return True, "Received pong from Gemini."
            return False, "Unexpected response while checking Gemini."
        except Exception as exc:
            return False, str(exc)
    
    def respond(self, user_query):
        """
        Backwards-compatible entry point used by the UI.
        Delegates to ai_chat_response() which keeps rule-based logic primary.
        """
        return self.ai_chat_response(user_query)

    def ai_chat_response(self, user_query):
        """
        Hybrid AI chat flow (rule-first, OpenAI optional).

        Order:
        1) Rule-based response using local metrics/diagnostics.
        2) If no intent matches, optionally query Gemini, then OpenAI.
        3) Special trigger: "hello open ai/openai" or "hello gemini/google ai" runs connectivity test.
        """
        if not user_query.strip():
            return "Please ask me a question about your system!"

        self.chat_history.append(('user', user_query))
        normalized = user_query.lower().strip()

        # Quick API connectivity test keywords
        if normalized in ("hello open ai", "hello openai"):
            ok, detail = self.check_openai_connection()
            response = "✅ OpenAI API is working correctly." if ok else "❌ OpenAI API connection failed."
            if detail and not ok:
                response = f"{response} ({detail})"
            self.chat_history.append(('ai', response))
            return response

        if normalized in ("hello gemini", "hello google ai"):
            ok, detail = self.check_gemini_connection()
            response = "✅ Gemini API is working correctly." if ok else "❌ Gemini API connection failed."
            if detail and not ok:
                response = f"{response} ({detail})"
            self.chat_history.append(('ai', response))
            return response

        if not self.engine.current_metrics:
            offline_msg = "Please run diagnostics first so I can reference your system state."
            self.chat_history.append(('ai', offline_msg))
            return offline_msg

        # Rule-based path (primary)
        intent = self._detect_intent(normalized.rstrip('?!.'))
        if intent:
            response = self._generate_response_by_intent(normalized)
            self.chat_history.append(('ai', response))
            return response

        # No clear intent: try Gemini first (optional) as conversational helper; rules stay primary.
        if self.use_gemini and self.gemini_model:
            try:
                response = self.get_gemini_response(user_query, self.engine.current_metrics)
                if response:
                    self.chat_history.append(('ai', response))
                    return response
            except Exception:
                pass

        # If Gemini not available, try OpenAI as a helper with guardrails (optional).
        # OpenAI complements the rule engine and only runs when rules cannot answer.
        if self.use_openai and self.openai_client:
            try:
                response = self.get_openai_response(user_query, self.engine.current_metrics)
                if response:
                    self.chat_history.append(('ai', response))
                    return response
            except Exception:
                # Network/auth errors fall through to local fallback
                pass

        # Offline fallback when OpenAI is unavailable or fails
        response = self._answer_unclear(self.engine.current_metrics)
        self.chat_history.append(('ai', response))
        return response
    
    def _detect_intent(self, query):
        """
        Detect user intent from keywords.
        
        Returns:
            str: Intent category or None if no clear match
        """
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in query:
                    return intent
        return None

    def get_openai_response(self, user_query, system_metrics):
        """
        Forward query to OpenAI with guardrails. OpenAI is optional and only complements rules.
        """
        if not self.use_openai or not self.openai_client:
            return None

        diags = self.engine.diagnostics or []
        diag_summary = []
        for d in diags:
            diag_summary.append(
                f"{d['category']}: {d['issue']} | why: {d['why']} | fixes: {', '.join(d['solutions'][:2]) if d['solutions'] else 'n/a'}"
            )
        diag_text = "\n".join(diag_summary) if diag_summary else "No issues detected."

        # Add guardrails with the new "SysOptima AI" persona
        system_prompt = (
            "You are SysOptima AI, an intelligent system assistant inside a desktop application called "
            "“SysOptima – System Intelligence Platform”.\n\n"
            "Your purpose is to:\n"
            "- Analyze system health data based on the provided metrics\n"
            "- Answer user questions about CPU, RAM, GPU, disk, performance, gaming, AI workloads, and upgrades\n"
            "- Provide clear explanations, impact analysis, and prioritized recommendations\n"
            "- Act like a professional system engineer + AI assistant\n\n"
            "Rules:\n"
            "- Always use the latest system diagnostics data provided in the user message\n"
            "- Never guess or hallucinate hardware values; strict adherence to provided metrics\n"
            "- If a question is unclear, infer the most relevant system-related intent\n"
            "- Keep responses concise (<120 words), structured, and actionable\n"
            "- Match a professional, calm, enterprise tone\n"
            "- Label the reply as 'AI Assistant Response'"
        )

        user_payload = (
            f"User question: {user_query}\n\n"
            f"Metrics snapshot: CPU {system_metrics['cpu_percent']:.1f}%, RAM {system_metrics['ram_percent']:.1f}% "
            f"({system_metrics['ram_available_gb']:.1f}/{system_metrics['ram_total_gb']:.1f} GB free/total), "
            f"Disk {system_metrics['disk_percent']:.1f}% used ({system_metrics['disk_free_gb']:.1f}/{system_metrics['disk_total_gb']:.1f} GB free/total), "
            f"GPU available: {system_metrics['gpu_available']}, GPU load: {system_metrics['gpu_percent']:.1f}%.\n"
            f"Diagnostics summary:\n{diag_text}\n"
            "Respond with supportive guidance only."
        )

        try:
            resp = self.openai_client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_payload},
                ],
            )

            text_out = None
            try:
                text_out = resp.output_text
            except Exception:
                pass
            if not text_out and hasattr(resp, "content") and isinstance(resp.content, list):
                text_out = str(resp.content[0].get("text", "")).strip()

            if not text_out:
                return None

            return f"AI Assistant Response (OpenAI): {text_out.strip()}"
        except Exception as exc:
            # Graceful fallback messages for network/auth/rate limits
            return (
                "AI Assistant Response (OpenAI): Unable to fetch cloud help right now. "
                f"Reason: {exc}"
            )

    def get_gemini_response(self, user_query, system_metrics):
        """
        Forward query to Gemini with guardrails. Gemini is optional and only complements rules.
        """
        if not self.use_gemini or not self.gemini_model:
            return None

        diags = self.engine.diagnostics or []
        diag_summary = []
        for d in diags:
            diag_summary.append(
                f"{d['category']}: {d['issue']} | why: {d['why']} | fixes: {', '.join(d['solutions'][:2]) if d['solutions'] else 'n/a'}"
            )
        diag_text = "\n".join(diag_summary) if diag_summary else "No issues detected."

        prompt = (
            "You are SysOptima AI, an intelligent system assistant inside a desktop application called "
            "“SysOptima – System Intelligence Platform”.\n\n"
            "Your purpose is to:\n"
            "- Analyze system health data based on the provided metrics\n"
            "- Answer user questions about CPU, RAM, GPU, disk, performance, gaming, AI workloads, and upgrades\n"
            "- Provide clear explanations, impact analysis, and prioritized recommendations\n"
            "- Act like a professional system engineer + AI assistant\n\n"
            "Rules:\n"
            "- Always use the latest system diagnostics data provided below\n"
            "- Never guess or hallucinate hardware values; strict adherence to provided metrics\n"
            "- If a question is unclear, infer the most relevant system-related intent\n"
            "- Keep responses concise (<110 words), structured, and actionable\n"
            "- Match a professional, calm, enterprise tone\n"
            "- Label your answer as 'AI Assistant (Gemini)'\n\n"
            f"User question: {user_query}\n"
            f"Metrics snapshot: CPU {system_metrics['cpu_percent']:.1f}%, RAM {system_metrics['ram_percent']:.1f}% "
            f"({system_metrics['ram_available_gb']:.1f}/{system_metrics['ram_total_gb']:.1f} GB free/total), "
            f"Disk {system_metrics['disk_percent']:.1f}% used ({system_metrics['disk_free_gb']:.1f}/{system_metrics['disk_total_gb']:.1f} GB free/total), "
            f"GPU available: {system_metrics['gpu_available']}, GPU load: {system_metrics['gpu_percent']:.1f}%\n"
            f"Diagnostics summary:\n{diag_text}"
        )

        try:
            resp = self.gemini_model.generate_content(prompt)
            text_out = getattr(resp, "text", "") or ""
            if not text_out:
                return None
            return f"AI Assistant (Gemini): {text_out.strip()}"
        except Exception as exc:
            return (
                "AI Assistant (Gemini): Unable to fetch cloud help right now. "
                f"Reason: {exc}"
            )
    
    def _generate_response_by_intent(self, query):
        """
        Generate response based on detected intent and current diagnostics.
        
        This method contextualizes responses using:
        1. Current system metrics
        2. Detected diagnostic issues
        3. Intent-specific rules
        4. Response variation to avoid repetition
        """
        intent = self._detect_intent(query)
        m = self.engine.current_metrics
        diags = self.engine.diagnostics
        
        # Get high-level diagnostics status
        has_high_cpu = any(d['category'] == 'CPU' for d in diags)
        has_high_ram = any(d['category'] == 'RAM' for d in diags)
        has_high_disk = any(d['category'] == 'DISK' for d in diags)
        has_gpu = m['gpu_available']
        
        # Route to intent handler
        if intent == 'cpu':
            return self._answer_cpu(m, has_high_cpu, query)
        elif intent == 'ram':
            return self._answer_ram(m, has_high_ram, query)
        elif intent == 'gpu':
            return self._answer_gpu(m, has_gpu)
        elif intent == 'disk':
            return self._answer_disk(m, has_high_disk, query)
        elif intent == 'gaming':
            return self._answer_gaming(m, has_high_cpu, has_high_ram, has_gpu)
        elif intent == 'performance':
            return self._answer_performance(m, has_high_cpu, has_high_ram, has_high_disk)
        elif intent == 'fix':
            return self._answer_troubleshooting(m, diags)
        elif intent == 'upgrade':
            return self._answer_upgrade(m, diags)
        else:
            # No clear intent - provide helpful fallback
            return self._answer_unclear(m)
    
    def _answer_cpu(self, m, has_issue, query):
        """Answer CPU-related questions with varied responses."""
        cpu = m['cpu_percent']
        
        if "why" in query or "high" in query:
            if cpu > 85:
                return (f"Your CPU is at {cpu:.1f}% - quite high! This could be from heavy applications, "
                       "background processes, or system updates. Try: (1) Close unnecessary apps, "
                       "(2) Check Task Manager for resource hogs, (3) Disable startup programs.")
            elif cpu > 70:
                return (f"CPU at {cpu:.1f}% - moderate. This is typical during work. "
                       "If it stays high, check what processes are running.")
            else:
                return f"Your CPU is at {cpu:.1f}% - very healthy. No concerns here!"
        else:
            # Generic CPU question
            if has_issue:
                return (f"CPU usage: {cpu:.1f}% (currently elevated). I'd recommend checking what's "
                       "consuming resources. Want me to help troubleshoot?")
            else:
                return f"Your CPU is running at {cpu:.1f}% - all good!"
    
    def _answer_ram(self, m, has_issue, query):
        """Answer RAM-related questions with varied responses."""
        ram = m['ram_percent']
        free = m['ram_available_gb']
        total = m['ram_total_gb']
        
        if "why" in query or "slow" in query or "high" in query:
            if ram > 80:
                return (f"Memory is at {ram:.1f}% ({free:.1f} GB free). This is critical! "
                       "Close browser tabs, applications, or consider restarting to clear cache. "
                       f"You have {total:.1f} GB total - may need upgrade if this persists.")
            elif ram > 70:
                return (f"Memory at {ram:.1f}% - getting tight with {free:.1f} GB free. "
                       "Close unused apps and browser tabs to improve responsiveness.")
            else:
                return f"Memory at {ram:.1f}% - plenty available ({free:.1f} GB free). Not a bottleneck."
        else:
            # Generic memory question
            if has_issue:
                return (f"RAM usage: {ram:.1f}% with {free:.1f} GB available. Consider reducing "
                       "open applications if you're experiencing slowness.")
            else:
                return f"Memory: {ram:.1f}% used ({free:.1f} GB free) - comfortable level."
    
    def _answer_gpu(self, m, has_gpu):
        """Answer GPU-related questions."""
        if has_gpu:
            gpu = m['gpu_percent']
            return (f"GPU Status: ✓ Dedicated GPU detected. Current load: {gpu:.1f}%. "
                   "Your system can handle graphics-intensive tasks well.")
        else:
            return ("GPU Status: Integrated only (no dedicated GPU). "
                   "This limits heavy graphics work. Consider dedicated GPU if gaming/3D is important.")
    
    def _answer_disk(self, m, has_issue, query):
        """Answer disk/storage questions with varied responses."""
        disk = m['disk_percent']
        free = m['disk_free_gb']
        total = m['disk_total_gb']
        
        if "why" in query or "full" in query:
            if disk > 90:
                return (f"Disk is {disk:.0f}% full - critical! Only {free:.1f} GB free. "
                       "Delete old files, move media to external storage, or uninstall unused software. "
                       "System performance suffers when disk is nearly full.")
            elif disk > 80:
                return (f"Disk usage: {disk:.0f}% ({free:.1f} GB free). Getting tight. "
                       "Clean up downloads, temporary files, or old backups.")
            else:
                return f"Disk: {disk:.0f}% used - good headroom with {free:.1f} GB available."
        else:
            # Generic disk question
            if has_issue:
                return (f"Storage: {disk:.0f}% full. {free:.1f} GB of {total:.1f} GB available. "
                       "Consider freeing up space to maintain performance.")
            else:
                return f"Storage: {disk:.0f}% used ({free:.1f} GB free). Healthy."
    
    def _answer_gaming(self, m, has_cpu_issue, has_ram_issue, has_gpu):
        """Answer gaming capability questions."""
        cpu = m['cpu_percent']
        ram = m['ram_percent']
        gpu = m['gpu_percent']
        
        if not has_gpu:
            return ("Gaming: ⚠ Your system uses integrated graphics (no dedicated GPU). "
                   "Light games (Solitaire, Minecraft on low) might work, but demanding titles won't perform well. "
                   "For serious gaming, consider a GPU upgrade.")
        
        # Assess capability based on current resources
        if has_cpu_issue or has_ram_issue:
            return ("Gaming: Possible but not ideal right now. CPU and/or RAM are stressed. "
                   "Close background apps first. For better experience: (1) Lower graphics settings, "
                   "(2) Reduce game resolution, or (3) Upgrade components.")
        elif cpu < 60 and ram < 70:
            return ("Gaming: ✓ Your system looks good! CPU: {:.0f}%, RAM: {:.0f}%, GPU ready. "
                   "Start with medium-quality games and adjust settings based on performance.".format(cpu, ram))
        else:
            return ("Gaming: Possible. Current load is moderate. Recommended: "
                   "Start with medium graphics settings and monitor performance.")
    
    def _answer_performance(self, m, has_cpu_issue, has_ram_issue, has_disk_issue):
        """Answer 'how to improve performance' questions."""
        suggestions = []
        
        # Prioritize fixes by severity
        if has_disk_issue or m['disk_percent'] > 80:
            suggestions.append("🔴 Free up disk space (delete old files, clear temp)")
        if has_ram_issue or m['ram_percent'] > 75:
            suggestions.append("🟡 Close browser tabs and unused applications")
        if has_cpu_issue or m['cpu_percent'] > 80:
            suggestions.append("🟡 Disable startup programs and background services")
        
        if not suggestions:
            suggestions.append("✓ System is running well! Consider: (1) Regular disk cleanup, "
                            "(2) Restart monthly, (3) Update drivers")
        
        return "Performance optimization steps:\n" + "\n".join(suggestions)
    
    def _answer_troubleshooting(self, m, diags):
        """Answer 'fix/troubleshooting' questions."""
        if not diags or (len(diags) == 1 and diags[0]['severity'] == 'GOOD'):
            return ("No major issues detected. If you're experiencing problems:\n"
                   "1. Restart your system\n"
                   "2. Update drivers and Windows\n"
                   "3. Run antivirus scan\n"
                   "4. Clear browser cache")
        
        # Reference detected issues
        issues_str = "\n".join([f"• {d['issue']}" for d in diags if d['severity'] != 'GOOD'])
        return (f"Detected issues:\n{issues_str}\n\n"
               "Quick fixes:\n"
               "1. Run Disk Cleanup\n"
               "2. Close unused applications\n"
               "3. Restart your system\n"
               "4. Update software")
    
    def _answer_upgrade(self, m, diags):
        """Answer upgrade recommendation questions."""
        bottlenecks = []
        
        # Analyze bottlenecks from metrics
        if m['cpu_percent'] > 75:
            bottlenecks.append("CPU (consider i5/i7 or Ryzen 5/7)")
        if m['ram_percent'] > 75:
            bottlenecks.append("RAM (add 8GB+ stick)")
        if m['disk_percent'] > 85:
            bottlenecks.append("Storage (upgrade to larger SSD)")
        if not m['gpu_available']:
            bottlenecks.append("GPU (add dedicated graphics card)")
        
        if bottlenecks:
            return (f"Upgrade recommendations based on current usage:\n"
                   "• " + "\n• ".join(bottlenecks) + "\n\n"
                   "Priority: Start with the most-stressed component.")
        else:
            return ("Your current system looks adequate for typical use. "
                   "No urgent upgrades needed. Upgrade when you outgrow current performance.")
    
    def _answer_unclear(self, m):
        """Fallback response when intent is unclear."""
        # Provide current status and suggest topics
        return (f"I'm not sure what you're asking, but here's your system status:\n"
               f"• CPU: {m['cpu_percent']:.0f}%\n"
               f"• RAM: {m['ram_percent']:.0f}%\n"
               f"• Disk: {m['disk_percent']:.0f}%\n\n"
               "You can ask me about: CPU, RAM, GPU, disk space, gaming, "
               "performance, issues, or upgrades.")


class DiagnosticsView(ttk.Frame):
    """
    Diagnostics UI with results display and AI chat assistant.
    
    Layout:
    - Header with "Run Diagnostics" button
    - Diagnostics results panel (scrollable)
    - AI Chat section (scrollable chat + input)
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Initialize engines
        self.diag_engine = DiagnosticsEngine()
        self.ai_assistant = AIAssistant(self.diag_engine)
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the complete diagnostics UI with improved layout."""
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("Section.TLabelframe", padding=12)
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 6))

        # Header frame with title and primary run button
        header_frame = ttk.Frame(self, padding=(12, 12, 12, 6))
        header_frame.pack(fill="x")

        title = ttk.Label(
            header_frame,
            text="System Diagnostics & AI Assistant",
            style="Header.TLabel"
        )
        title.pack(side="left", anchor="w")

        self.run_btn = ttk.Button(
            header_frame,
            text="🔍 Run Diagnostics",
            style="Primary.TButton",
            command=self._handle_run_diagnostics
        )
        self.run_btn.pack(side="right", anchor="e")
        
        # Main content: 2-column layout with visual separation
        content_frame = ttk.Frame(self, padding=(12, 6, 12, 12))
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=3, uniform="cols")
        content_frame.columnconfigure(1, weight=2, uniform="cols")

        # ===== LEFT PANEL: Diagnostics Results =====
        left_frame = ttk.LabelFrame(content_frame, text="System Diagnostics Report", style="Section.TLabelframe")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 4))
        left_frame.columnconfigure(0, weight=1)
        
        # Diagnostics scrolled text with better formatting
        self.results_text = scrolledtext.ScrolledText(
            left_frame,
            height=20,
            width=50,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#F8F9FA",
            fg="#111827",
            padx=8,
            pady=8
        )
        self.results_text.pack(fill="both", expand=True)
        self.results_text.insert(tk.END, "Click 'Run Diagnostics' to scan your system...")
        self.results_text.config(state="disabled")
        
        # Configure text tags for formatting
        self._configure_text_tags(self.results_text)
        
        # ===== RIGHT PANEL: AI Assistant =====
        right_frame = ttk.LabelFrame(content_frame, text="AI Assistant", style="Section.TLabelframe")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=0)
        
        # Chat display area (read-only)
        chat_scroll = ttk.Frame(right_frame, padding=(2, 2, 2, 6))
        chat_scroll.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(chat_scroll)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_display = tk.Text(
            chat_scroll,
            height=18,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#111827",
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.chat_display.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure chat tags for user/AI styling
        self.chat_display.tag_config("user", foreground="#1d4ed8", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_config("ai", foreground="#0f5132", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_config("user_msg", foreground="#0f172a", background="#e8f2ff", lmargin2=18, rmargin=8, spacing1=2, spacing3=6)
        self.chat_display.tag_config("ai_msg", foreground="#0f172a", background="#e6f7ed", lmargin2=18, rmargin=8, spacing1=2, spacing3=6)
        
        # Input frame for user query
        input_frame = ttk.Frame(right_frame, padding=(2, 2, 2, 10))
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.placeholder = "Ask about CPU, RAM, gaming, upgrades, performance…"
        self.query_input = ttk.Entry(input_frame, width=30)
        self.query_input.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.query_input.bind("<Return>", lambda e: self._send_query())
        self.query_input.bind("<FocusIn>", self._on_focus_in)
        self.query_input.bind("<FocusOut>", self._on_focus_out)
        
        self.send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self._send_query,
            width=8
        )
        self.send_btn.grid(row=0, column=1, sticky="e")
        
        # Update send button state when input changes
        self.query_input.bind("<KeyRelease>", self._update_send_button_state)
        self._set_placeholder()
    
    def _configure_text_tags(self, text_widget):
        """Configure text tags for diagnostics results formatting."""
        text_widget.tag_config("header", font=("Segoe UI", 12, "bold"), foreground="#0f172a")
        text_widget.tag_config("section", font=("Segoe UI", 10, "bold"), foreground="#1f2937")
        text_widget.tag_config("metric", font=("Consolas", 10), foreground="#111827")
        text_widget.tag_config("issue_high", font=("Segoe UI", 10, "bold"), foreground="#b91c1c")
        text_widget.tag_config("issue_medium", font=("Segoe UI", 10, "bold"), foreground="#d97706")
        text_widget.tag_config("issue_good", font=("Segoe UI", 10, "bold"), foreground="#059669")
        text_widget.tag_config("solution", font=("Segoe UI", 10), foreground="#0f172a")
        text_widget.tag_config("bullet", font=("Consolas", 10), foreground="#0f172a")

    def _set_placeholder(self):
        """Apply subtle placeholder styling for the chat entry."""
        self.query_input.delete(0, tk.END)
        self.query_input.insert(0, self.placeholder)
        self.query_input.config(foreground="#9ca3af")
        self.send_btn.config(state="disabled")

    def _on_focus_in(self, _event=None):
        if self.query_input.get() == self.placeholder:
            self.query_input.delete(0, tk.END)
            self.query_input.config(foreground="#111827")

    def _on_focus_out(self, _event=None):
        if not self.query_input.get().strip():
            self._set_placeholder()
    
    def _update_send_button_state(self, event=None):
        """Disable send button if input is empty."""
        text = self.query_input.get()
        if text.strip() and text != self.placeholder:
            self.send_btn.config(state="normal")
        else:
            self.send_btn.config(state="disabled")
    
    def _handle_run_diagnostics(self):
        """Run diagnostics and display results."""
        self.run_btn.state(["disabled"])
        try:
            result = self.diag_engine.run_diagnostics()

            # Format and display results
            self._display_diagnostics_results(result)

            # Clear chat for fresh interaction
            self._clear_chat()
            self._add_chat_message(
                "ai",
                "Diagnostics complete! Ask me any questions about your system. "
                "E.g., 'Why is my CPU high?' or 'Can I play games?'"
            )
        finally:
            self.run_btn.state(["!disabled"])
    
    def _display_diagnostics_results(self, result):
        """
        Display formatted diagnostics results with improved styling.
        
        Args:
            result: Dictionary with 'metrics' and 'diagnostics' keys
        """
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        
        metrics = result['metrics']
        diagnostics = result['diagnostics']
        timestamp = result['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        
        # Header
        self.results_text.insert(tk.END, "SYSTEM DIAGNOSTICS REPORT\n", "header")
        self.results_text.insert(tk.END, f"Generated: {timestamp}\n\n", "metric")

        # Metrics summary with visual emphasis
        self.results_text.insert(tk.END, "SYSTEM METRICS\n", "section")
        self.results_text.insert(tk.END, "────────────────────────────\n", "metric")

        cpu_tag = "issue_high" if metrics['cpu_percent'] > 80 else ("issue_medium" if metrics['cpu_percent'] > 60 else "metric")
        ram_tag = "issue_high" if metrics['ram_percent'] > 75 else ("issue_medium" if metrics['ram_percent'] > 60 else "metric")
        disk_tag = "issue_high" if metrics['disk_percent'] > 90 else ("issue_medium" if metrics['disk_percent'] > 80 else "metric")

        self.results_text.insert(tk.END, f" CPU:   {metrics['cpu_percent']:.1f}%\n", cpu_tag)
        self.results_text.insert(tk.END, f" RAM:   {metrics['ram_percent']:.1f}%  ({metrics['ram_available_gb']:.1f}/{metrics['ram_total_gb']:.1f} GB free/total)\n", ram_tag)
        if metrics['gpu_available']:
            gpu_tag = "issue_medium" if metrics['gpu_percent'] > 85 else "metric"
            self.results_text.insert(tk.END, f" GPU:   {metrics['gpu_percent']:.1f}% (dedicated)\n", gpu_tag)
        else:
            self.results_text.insert(tk.END, " GPU:   Integrated / not detected\n", "metric")
        self.results_text.insert(tk.END, f" DISK:  {metrics['disk_percent']:.1f}%  ({metrics['disk_free_gb']:.1f}/{metrics['disk_total_gb']:.1f} GB free/total)\n\n", disk_tag)

        # Diagnostics details
        self.results_text.insert(tk.END, "DETECTED ISSUES\n", "section")
        self.results_text.insert(tk.END, "────────────────────────────\n", "metric")

        all_solutions = []
        for diag in diagnostics:
            severity_icon = "●"
            issue_tag = {"HIGH": "issue_high", "MEDIUM": "issue_medium", "GOOD": "issue_good"}.get(diag['severity'], "metric")

            self.results_text.insert(tk.END, f" {severity_icon} {diag['issue']}\n", issue_tag)
            self.results_text.insert(tk.END, f"   WHAT: {diag['what']}\n", "metric")
            self.results_text.insert(tk.END, f"   WHY : {diag['why']}\n", "metric")

            if diag['caused_by']:
                for cause in diag['caused_by']:
                    self.results_text.insert(tk.END, f"     • {cause}\n", "bullet")

            if diag['solutions']:
                for solution in diag['solutions']:
                    self.results_text.insert(tk.END, f"     ✔ {solution}\n", "solution")
                    all_solutions.append(solution)

            self.results_text.insert(tk.END, "\n")

        # Recommendations summary
        if all_solutions:
            self.results_text.insert(tk.END, "RECOMMENDATIONS\n", "section")
            self.results_text.insert(tk.END, "────────────────────────────\n", "metric")
            for sol in all_solutions[:6]:
                self.results_text.insert(tk.END, f" ✔ {sol}\n", "solution")
            self.results_text.insert(tk.END, "\n")
        
        self.results_text.config(state="disabled")
    
    def _send_query(self):
        """Send user query to AI assistant and display response."""
        query = self.query_input.get().strip()
        if not query or query == self.placeholder:
            return
        
        if not self.diag_engine.current_metrics:
            self._add_chat_message("ai", "Please run diagnostics first!")
            return
        
        # Add user message
        self._add_chat_message("user", query)
        self.query_input.delete(0, tk.END)
        
        # Get AI response
        response = self.ai_assistant.respond(query)
        
        # Add AI response
        self._add_chat_message("ai", response)
    
    def _add_chat_message(self, sender, message):
        """Add a message to the chat display with semantic styling."""
        self.chat_display.config(state="normal")
        
        if sender == "user":
            # User message with blue styling
            self.chat_display.insert(tk.END, "You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user_msg")
        else:
            # AI message with green styling
            self.chat_display.insert(tk.END, "AI: ", "ai")
            self.chat_display.insert(tk.END, f"{message}\n\n", "ai_msg")
        
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)  # Auto-scroll to end
    
    def _clear_chat(self):
        """Clear chat display."""
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")
