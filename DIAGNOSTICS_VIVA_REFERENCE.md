# Diagnostics Module - Viva Quick Reference

## 30-Second Pitch

"The Diagnostics module is an explainable AI system analyzer that runs completely offline. It collects live system metrics - CPU, RAM, GPU, disk - using psutil, applies threshold-based rules to detect issues like high CPU load or low memory, and generates human-readable reports explaining what the issue is, why it happens, what likely caused it, and how to fix it. We also built a rule-based chat assistant that answers questions about system health based on the actual metrics. No APIs, no machine learning, no internet required - just pure rule-based logic that's easy to understand and explain."

---

## Key Features to Highlight

### 1. Rule-Based Diagnostics ✅
- **Threshold Rules:**
  - CPU > 80% → High CPU Load
  - RAM > 75% → Memory Pressure
  - GPU > 85% → GPU Overload
  - Disk > 90% → Storage Crisis

- **For Each Issue, We Report:**
  1. What the problem is (plain English)
  2. Why it matters
  3. Root causes (list of likely reasons)
  4. Solutions (actionable recommendations)

### 2. Explainable AI Assistant ✅
- No machine learning, no APIs, no training data
- Pure keyword matching + metric-based responses
- Understands ~10 categories of questions:
  - CPU/Processor usage
  - RAM/Memory issues
  - Gaming capability
  - Performance optimization
  - Disk space
  - GPU availability
  - Temperature
  - Upgrade recommendations

### 3. Offline-Only Operation ✅
- All processing on device
- No cloud calls
- No internet dependency
- ~500ms to run diagnostics
- Real-time metrics

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│         DiagnosticsView (Tkinter UI)                 │
│  ┌────────────────────┬───────────────────────────┐  │
│  │ Diagnostics Panel  │  AI Chat Panel             │  │
│  │ • Metrics Summary  │  • Chat Display           │  │
│  │ • Issues List      │  • Input Box              │  │
│  │ • What/Why/Causes  │  • Send Button            │  │
│  │ • Solutions        │  • Chat History           │  │
│  └────────────────────┴───────────────────────────┘  │
└──────────────────────────────────────────────────────┘
              ↑              ↑
              │              │
    ┌─────────┴──────────────┴─────────┐
    │                                  │
┌───────────────────────────┐    ┌────────────────┐
│ DiagnosticsEngine         │    │ AIAssistant    │
│ • run_diagnostics()       │    │ • respond()    │
│ • _collect_metrics()      │    │ • _match_()    │
│ • _analyze_metrics()      │    │ • pattern lib  │
└───────────────────────────┘    └────────────────┘
    ↓                                  ↓
psutil (CPU, RAM, Disk)       Keyword Matching + Rules
GPUtil (GPU)                   Current System State
```

---

## Code Walkthrough - Key Methods

### 1. Running Diagnostics
```python
# When user clicks "Run Diagnostics":
result = self.diag_engine.run_diagnostics()

# Engine does:
1. Collect metrics via psutil & GPUtil
2. Apply threshold-based rules
3. Generate structured reports
4. Return metrics + diagnostics
```

### 2. Detecting Issues
```python
# Rule example - High CPU
if m['cpu_percent'] > 80:
    issues.append({
        'severity': 'HIGH' if m['cpu_percent'] > 90 else 'MEDIUM',
        'what': f"Your CPU is at {m['cpu_percent']:.1f}%",
        'why': "Heavy workload on processor",
        'caused_by': ["Multiple apps", "Gaming", "..."],
        'solutions': ["Close apps", "Reduce quality", "..."]
    })
```

### 3. AI Response Logic
```python
# User asks: "Why is my CPU high?"
# AI does:
1. Keyword match → finds "cpu" and "why"
2. Get current CPU from metrics
3. If CPU > 80: suggest closing apps
4. If CPU < 50: say it's normal
5. Return system-specific response
```

---

## Common Viva Questions & Answers

### Q1: "Why not use machine learning?"
**A:** "For this academic project, rule-based logic is more important than accuracy because it's explainable and transparent. With ML, we'd need training data and couldn't easily show why the system made a particular diagnosis. Rule-based lets us point to exact thresholds and say 'We flagged this because CPU exceeds 80%.' It also works offline, uses minimal resources, and is reproducible."

### Q2: "How accurate is the diagnostics?"
**A:** "Accuracy depends on the rule thresholds we chose. The 80% CPU threshold works well for most systems, but gaming might use 90%+ consistently. The diagnostics are less about 'accuracy' and more about 'useful detection.' When we say 'High CPU Load,' we're flagging something the user should probably investigate. The recommendations help them decide if it's a real problem."

### Q3: "What if GPU is not available?"
**A:** "We gracefully handle it. GPUtil is optional - if it's not installed or no GPU is found, we show 0% GPU and flag 'GPU Unavailable' in the diagnostics. The system still runs perfectly; we just skip GPU analysis. When users ask 'Can I play games?', we tell them they're using integrated graphics and recommend adjusting expectations accordingly."

### Q4: "Can the AI talk to multiple users?"
**A:** "The current design handles one user session. The AI maintains chat history for that session. To scale to multiple users, we'd need a database to store chat history per user, but that wasn't required for this project. The current approach is sufficient for an academic demo."

### Q5: "How do you prevent the UI from freezing?"
**A:** "All metric collection happens in the main thread using psutil, which is fast (~500ms). We don't spawn threads for diagnostics. We use Tkinter's after() mechanism for the real-time monitor (which does spawn threads for separate monitoring), but diagnostics is a simple synchronous operation that completes quickly."

### Q6: "What's the biggest limitation?"
**A:** "We can't see inside running processes - we only get system-level metrics from psutil. So if a user's system is slow but CPU and RAM are low, we can't pinpoint which specific application is causing the issue. That would require process-level analysis, which is beyond this scope. We recommend users check Task Manager for that level of detail."

---

## Live Demo Script

### Step 1: Navigate to Diagnostics
- Click on "Diagnostics" in the sidebar
- Show the empty state: "Click 'Run Diagnostics' to scan your system"

### Step 2: Run Diagnostics
- Click "🔍 Run Diagnostics" button
- Point out:
  - Timestamp of the scan
  - Current metrics (CPU %, RAM %, Disk %)
  - Issues detected with severity indicators

### Step 3: Show Diagnostic Report
- Explain each issue shown:
  - "What" section (plain language problem)
  - "Why" section (impact explanation)
  - Causes (list of root causes)
  - Solutions (actionable recommendations)

### Step 4: Ask AI Questions
- Type: "Why is my CPU at 45%?" (or whatever current CPU is)
- Show response explains current metrics
- Type: "Can I play games?"
- Show system-specific response
- Type: "How can I improve performance?"
- Show context-aware suggestions

### Step 5: Highlight Features
- Explain the rule-based logic
- Show how thresholds work
- Demonstrate keyword matching for different questions
- Emphasize: "No APIs, no ML, completely offline"

---

## Expected System Outputs

### Low System Load
```
System Running Smoothly ✓
• CPU: 15%
• RAM: 30%
• Disk: 45%

Output: "Your system is operating within normal parameters."
```

### High Resource Usage
```
🔴 High CPU Usage (92.5%)
What: Your CPU is working at 92.5% capacity
Why: Heavy workload on processor
Caused by:
  • Gaming or video editing
  • Compilation/build process
  • Background services
Solutions:
  • Close unnecessary applications
  • Check Task Manager for resource hogs
  • Lower graphics settings
```

---

## Files Modified

- **ui/diagnostics.py** - Complete rewrite with 530 lines
  - DiagnosticsEngine class (~150 lines)
  - AIAssistant class (~120 lines)
  - DiagnosticsView class (~260 lines)

**No changes to:**
- ui/main_window.py (already wired correctly)
- app.py (no changes needed)
- Other modules (fully compatible)

---

## Time Estimates for Viva

- **Explain Architecture:** 2-3 minutes
- **Show Live Demo:** 2-3 minutes
- **Answer Questions:** 3-5 minutes
- **Total Time:** 7-11 minutes

---

## Key Strengths to Emphasize

1. ✅ **Completely Offline** - No internet, no APIs, works anywhere
2. ✅ **Explainable** - Every diagnosis has reasoning, not a black box
3. ✅ **Rule-Based** - Deterministic, easy to audit and modify
4. ✅ **Clean UI** - Professional layout with diagnostics + chat
5. ✅ **Educational** - Shows how to build practical AI without ML
6. ✅ **Lightweight** - Fast, low resource usage
7. ✅ **Production Ready** - Error handling, graceful degradation

---

**Ready for Viva! ✅**
