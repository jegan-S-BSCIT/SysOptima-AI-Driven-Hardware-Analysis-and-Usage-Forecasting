# SysOptima Desktop Application
## Intelligent Computer Performance Analysis and Guidance System

### 📋 Project Context

**B.Sc. IT Final Year Project**
- Pure desktop application using Tkinter
- NO web components, Flask, or browser dependencies
- Rule-based AI with optional Gemini API fallback
- Academic-appropriate and viva-ready

---

## 🎯 Features Overview

### 1. **System Monitor Tab**
- **Real-time Metrics**: CPU, RAM, GPU, Disk usage updated every 1 second
- **Live Charts**: 60-second history visualization using matplotlib
- **Performance Indicators**: Color-coded status indicators
- **Hardware Detection**: Automatic GPU detection (NVIDIA/AMD support)

### 2. **Diagnostics Tab**
- **Rule-Based Analysis**: 5 diagnostic categories (CPU, RAM, GPU, Disk, Performance)
- **Intelligent Detection**:
  - High CPU/RAM/GPU usage identification
  - Disk space warnings
  - Low hardware specifications alerts
- **Detailed Explanations**:
  - What is the problem?
  - Why does it happen?
  - What caused it?
  - How to fix it? (with step-by-step recommendations)

### 3. **AI Assistant Tab**
- **Chat Interface**: Conversational system inside Tkinter
- **Rule-Based Responses**: Primary intelligence (offline, no API needed)
- **Gemini Fallback**: Optional OpenAI/Gemini API for educational responses
- **Special Commands**: API testing, help, status, history clearing

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8+ required
python --version

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - tkinter (included with Python)
# - psutil (system monitoring)
# - GPUtil (GPU detection)
# - matplotlib (charts)
# - python-dotenv (environment variables)
# - google-generativeai (optional, for Gemini)
```

### Running the Application

#### Method 1: Using Batch File (Windows)
```bash
run_desktop_app.bat
```

#### Method 2: Using Shell Script (Linux/macOS)
```bash
bash run_desktop_app.sh
```

#### Method 3: Direct Python
```bash
python main.py
```

---

## 🏗️ Project Structure

```
SysOptima/
├── main.py                          # Application entry point
├── desktop_ui/                      # UI Components (pure Tkinter)
│   ├── __init__.py
│   ├── main_window.py              # Main window & tab management
│   ├── monitor_tab.py              # Real-time monitoring with charts
│   ├── diagnostics_tab.py          # Rule-based diagnostics
│   └── ai_chat_tab.py              # AI chat interface
├── core/                            # Core functionality
│   ├── gemini_ai_assistant.py      # AI logic (hybrid rule + API)
│   ├── hardware_detector.py         # Hardware detection
│   └── [other modules]
├── analysis/                        # Diagnostics algorithms
├── build.spec                       # PyInstaller configuration
├── run_desktop_app.bat             # Windows launcher
├── run_desktop_app.sh              # Linux/macOS launcher
├── requirements.txt                 # Python dependencies
└── .env                            # Environment variables (API key)
```

### Key Architecture

```
User Interface (Tkinter)
    ├─ System Monitor
    │   ├─ Real-time metrics collection
    │   ├─ psutil/GPUtil integration
    │   └─ matplotlib visualization
    ├─ Diagnostics Engine
    │   ├─ Rule-based pattern matching
    │   ├─ Performance thresholds
    │   └─ Recommendation generation
    └─ AI Chat Interface
        ├─ Input processing
        ├─ HybridAILogic (rules first → API fallback)
        └─ Formatted response display
```

---

## 🔧 Module Descriptions

### `main.py` - Application Entry Point
- Initializes Tkinter root window
- Creates MainWindow container
- Handles application lifecycle

### `desktop_ui/main_window.py` - Main Application Window
- Manages tabbed interface (Notebook)
- Initializes all tabs
- Background update thread (1-second updates)
- Application cleanup on close

### `desktop_ui/monitor_tab.py` - System Monitor
- **Features**:
  - Real-time CPU, RAM, GPU, Disk monitoring
  - 60-second history buffer
  - 4-chart matplotlib visualization
  - Updated every 1 second via `after()` pattern
- **Metrics Displayed**:
  - CPU: Percentage usage
  - RAM: Percentage usage + GB allocation
  - GPU: Percentage usage (if detected)
  - Disk: Percentage usage + GB allocation

### `desktop_ui/diagnostics_tab.py` - Diagnostics Engine
- **Rule Categories**:
  1. **CPU Diagnostics**:
     - Rule 1: CPU > 90% → Critical alert
     - Rule 2: CPU > 70% → Warning
     - Rule 3: < 4 cores → Information
  
  2. **RAM Diagnostics**:
     - Rule 1: RAM > 90% → Critical alert
     - Rule 2: RAM > 75% → Warning
     - Rule 3: Total < 8GB → Information
  
  3. **Disk Diagnostics**:
     - Rule 1: Disk > 95% → Critical alert
     - Rule 2: Disk > 80% → Warning
  
  4. **GPU Diagnostics** (if detected):
     - Rule 1: GPU > 80% → Information

- **Output Format**:
  - Severity indicator (Critical/Warning/Info/Good)
  - Color-coded background
  - 4-point explanation format
  - Actionable recommendations

### `desktop_ui/ai_chat_tab.py` - AI Assistant
- **User Interaction**:
  - Type question → Press Ctrl+Enter or Send button
  - Real-time response generation
- **Query Types**:
  - Diagnostic queries ("What about my CPU?")
  - Educational queries ("Explain CPU")
  - API test queries ("hello gemini")
  - Special commands ("help", "clear", "status")

### `core/gemini_ai_assistant.py` - Hybrid AI Logic
- **GeminiAIAssistant Class**: Manages Google Gemini API
- **HybridAILogic Class**: Orchestrates decision-making
  - Try rule-based responses first (fast, offline)
  - Fall back to Gemini API (if available, for educational content)
  - Graceful error handling for API failures
- **Features**:
  - Safe API key loading from environment
  - Connection testing
  - Rate limit handling
  - Response formatting

---

## 🎨 User Interface

### Window Layout
```
┌─────────────────────────────────────────┐
│ Title                          Status   │
├─────────────────────────────────────────┤
│                                         │
│   [System Monitor] [Diagnostics] [AI]   │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │                                 │   │
│   │   Tab Content                   │   │
│   │   (varies by selected tab)      │   │
│   │                                 │   │
│   └─────────────────────────────────┘   │
│                                         │
├─────────────────────────────────────────┤
│ B.Sc. IT Final Year Project | v1.0     │
└─────────────────────────────────────────┘
```

### System Monitor Tab
```
┌────────────────────────────────────────┐
│ System Metrics (Real-time)             │
│                                        │
│ CPU: 45%    RAM: 62%    GPU: 12%      │
│ Disk: 78%   Processes: 156            │
├────────────────────────────────────────┤
│ Performance Charts (Last 60 seconds)   │
│                                        │
│ [CPU Chart] [RAM] [GPU] [Disk]       │
│                                        │
│ (Live updating every 1 second)         │
└────────────────────────────────────────┘
```

### Diagnostics Tab
```
┌────────────────────────────────────────┐
│ ✓ System Running Normally              │
│ All metrics within normal ranges       │
│                                        │
│ ⚠ High RAM Usage (75%)                 │
│ RAM: 12GB of 16GB used                 │
│ Recommendation: Close unused apps      │
│                                        │
│ [scrollable area for all issues]       │
└────────────────────────────────────────┘
```

### AI Chat Tab
```
┌────────────────────────────────────────┐
│ AI Assistant - Ask about performance  │
│                      ✓ Online         │
├────────────────────────────────────────┤
│ [Chat History Display Area]            │
│                                        │
│ [12:34:56] You: What about CPU?        │
│ [12:34:57] AI: Your CPU is running...  │
│                                        │
├────────────────────────────────────────┤
│ [Send Message Input Box]      [Send]   │
│                                        │
│ Tips: Ask about CPU, RAM, GPU, Disk   │
└────────────────────────────────────────┘
```

---

## 🔌 Configuration

### Environment Variables (.env)

```bash
# Optional: Google Gemini API (for conversational AI)
GEMINI_API_KEY=your-actual-api-key-here

# Optional: OpenAI API (future support)
# OPENAI_API_KEY=your-api-key-here
```

**Getting Gemini API Key:**
1. Visit: https://ai.google.dev/
2. Click "Get API Key"
3. Create/select a project
4. Copy the API key
5. Paste into `.env` file

### Requirements (requirements.txt)

```
psutil>=5.9.0                    # System monitoring
GPUtil>=1.4.0                    # GPU detection
matplotlib>=3.5.0                # Charts
python-dotenv>=0.19.0            # Environment variables
google-generativeai>=0.3.0       # Gemini AI (optional)
```

---

## 📊 Real-time Monitoring Details

### Update Mechanism
- **Frequency**: Every 1 second
- **Method**: Tkinter `after()` in background thread
- **Data Collection**: psutil library
- **Visualization**: matplotlib embedded in Tkinter

### Performance Metrics

| Metric | Source | Update | Accuracy |
|--------|--------|--------|----------|
| CPU % | psutil.cpu_percent() | 1s | Per-process tracking |
| RAM % | psutil.virtual_memory() | 1s | System-wide |
| Disk % | psutil.disk_usage() | 1s | Per-partition |
| GPU % | GPUtil.getGPUs() | 1s | If NVIDIA/AMD GPU present |

### Historical Data
- **Buffer Size**: 60 entries (60 seconds)
- **Storage**: Deque (automatic old data removal)
- **Visualization**: 4 separate matplotlib subplots

---

## 🧠 Diagnostic Rules

### CPU Rules

```python
if cpu_usage > 90%:
    severity = "CRITICAL"
    recommendation = [
        "Close unnecessary applications",
        "Check for malware with antivirus",
        "Update drivers and BIOS",
        "Check Task Manager for runaway processes"
    ]
elif cpu_usage > 70%:
    severity = "WARNING"
    recommendation = [
        "Monitor CPU-intensive applications",
        "Disable unnecessary startup items"
    ]
elif cpu_cores < 4:
    severity = "INFO"
    recommendation = [
        "Consider upgrading to multi-core CPU"
    ]
```

### RAM Rules

```python
if ram_usage > 90%:
    severity = "CRITICAL"
    recommendation = [
        "Close memory-intensive applications",
        "Restart browser to clear cache",
        "Upgrade RAM to 16GB+"
    ]
elif ram_usage > 75%:
    severity = "WARNING"
    recommendation = [
        "Close unused applications",
        "Reduce browser tabs",
        "Consider RAM upgrade"
    ]
elif total_ram < 8GB:
    severity = "WARNING"
    recommendation = [
        "Upgrade RAM to 16GB minimum"
    ]
```

### Disk Rules

```python
if disk_usage > 95%:
    severity = "CRITICAL"
    recommendation = [
        "Delete unnecessary files",
        "Clear temporary files",
        "Uninstall unused applications",
        "Upgrade storage device"
    ]
elif disk_usage > 80%:
    severity = "WARNING"
    recommendation = [
        "Clean up temporary files",
        "Archive old files",
        "Consider larger storage"
    ]
```

---

## 🤖 AI Assistant Logic

### Query Processing Flow

```
User Query
    ↓
[API Test Detection] → "hello gemini"
    ├─ YES → Show API status
    └─ NO → Continue
    ↓
[Rule Matching] → CPU/RAM/GPU/Disk patterns
    ├─ MATCH → Return diagnostic response
    └─ NO MATCH → Continue
    ↓
[Gemini API Available?]
    ├─ YES → Get Gemini response
    └─ NO → Return helpful error message
    ↓
Display Response with Timestamp
```

### Rule-Based Categories

1. **CPU Category**:
   - Patterns: "cpu", "processor", "performance", "slow"
   - Response: CPU diagnostic info

2. **RAM Category**:
   - Patterns: "ram", "memory", "slow", "lag"
   - Response: RAM diagnostic info

3. **GPU Category**:
   - Patterns: "gpu", "graphics", "video", "game"
   - Response: GPU diagnostic info

4. **Disk Category**:
   - Patterns: "disk", "storage", "space", "full"
   - Response: Disk diagnostic info

5. **Performance Category**:
   - Patterns: "slow", "lag", "freeze", "hang"
   - Response: Performance summary

### Gemini API Integration

- **Purpose**: Educational responses for questions not matching rules
- **Optional**: Works perfectly without API key
- **Safe**: Graceful fallback if API unavailable
- **Academic**: Explainable decisions (not black-box AI)

---

## 🐛 Debugging

### Enable Debug Logging

Edit `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Common Issues

#### 1. "No module named 'tkinter'"
```bash
# Solution: Install tkinter
# Windows: Already included with Python
# Linux: sudo apt-get install python3-tk
# macOS: Usually included; if not: brew install python-tk
```

#### 2. "GPU not detected"
- Check: `GPUtil.getGPUs()` returns empty list
- Ensure: NVIDIA/AMD drivers are installed
- Note: Desktop app falls back gracefully if no GPU

#### 3. "Gemini API key not found"
- Check: `.env` file in project root
- Verify: `GEMINI_API_KEY=...` (no spaces)
- Test: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"`

#### 4. "matplotlib not rendering charts"
```bash
# Solution: Reinstall matplotlib
pip uninstall matplotlib
pip install matplotlib
```

---

## 📦 Building Executable (PyInstaller)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build Application
```bash
pyinstaller build.spec
```

### Step 3: Find Executable
```
dist/SysOptima/SysOptima.exe  (on Windows)
dist/SysOptima/SysOptima      (on Linux/macOS)
```

### Step 4: Distribute
- Copy entire `dist/SysOptima/` folder
- Users can run `SysOptima.exe` directly
- No Python installation required!

### Build Options
- `console=False`: No console window
- `windowed=True`: Desktop application
- Single executable: Change `COLLECT` to `EXE` only

---

## 🎓 Academic Considerations

### Project Strengths for Viva

1. **Explainable AI**
   - ✓ Rule-based logic (not black-box)
   - ✓ All decisions traceable
   - ✓ Optional Gemini (not required)

2. **Academic Appropriateness**
   - ✓ Pure desktop application (no web)
   - ✓ No complex deep learning
   - ✓ Standard libraries (psutil, tkinter)

3. **Code Quality**
   - ✓ Modular architecture
   - ✓ Clear separation of concerns
   - ✓ Inline documentation

4. **Functionality**
   - ✓ Real-time monitoring (every 1s)
   - ✓ Rule-based diagnostics
   - ✓ AI chat interface
   - ✓ Visual charts and indicators

### Viva Talking Points

1. **Why Rule-Based First?**
   - Deterministic behavior
   - Fast performance (no network latency)
   - Explainable decision-making
   - Works offline

2. **Why Hybrid Approach?**
   - Best of both worlds
   - Fallback system for robustness
   - Educational AI responses
   - No single point of failure

3. **Why Desktop Application?**
   - Lightweight and responsive
   - Direct system access (psutil, GPUtil)
   - No web browser overhead
   - Professional system utility appearance

4. **Scalability**
   - Can extend to network monitoring
   - Can add more rule categories
   - Can integrate additional APIs
   - PyInstaller creates standalone EXE

---

## 📝 License & Attribution

**B.Sc. IT Final Year Project**
- Pure desktop application
- Educational and academic use
- Original development for course completion

---

## 📞 Support & Troubleshooting

### Quick Tests

```bash
# Test system monitoring
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%')"

# Test GPU detection
python -c "import GPUtil; print(GPUtil.getGPUs())"

# Test UI modules
python -c "from desktop_ui.main_window import MainWindow; print('✓ UI loaded')"

# Test AI module
python -c "from core.gemini_ai_assistant import HybridAILogic; print('✓ AI loaded')"
```

### Performance Optimization

- **Reduce chart update frequency**: Modify `monitor_tab.py` `after()` timing
- **Increase history buffer**: Modify `MonitorTab.history_size`
- **Disable GPU detection**: Comment out `GPUtil` import if not needed
- **Reduce diagnostic frequency**: Modify `main_window.py` update thread

---

## ✅ Checklist for Viva

- [ ] Application runs without errors
- [ ] System Monitor shows real-time data
- [ ] Charts update every second
- [ ] Diagnostics generate appropriate alerts
- [ ] AI chat responds to queries
- [ ] Rule-based responses work offline
- [ ] Code is clean and modular
- [ ] PyInstaller executable builds successfully
- [ ] Documentation is comprehensive
- [ ] All features work as designed

---

**Happy coding! Good luck with your final year project! 🚀**
