# SysOptima Architecture & Design Documentation
## Visual Architecture for B.Sc. IT Project Presentation

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌───────────────────────────────────────────────────────┐     │
│  │                    FRONTEND LAYER                      │     │
│  │                                                         │     │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │     │
│  │  │   HTML5     │  │ Tailwind CSS │  │  JavaScript  │ │     │
│  │  │  Structure  │  │   Styling    │  │    Logic     │ │     │
│  │  └─────────────┘  └──────────────┘  └──────────────┘ │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐  │     │
│  │  │              Chart.js                           │  │     │
│  │  │  (CPU/RAM/GPU/Disk Visualization)               │  │     │
│  │  └─────────────────────────────────────────────────┘  │     │
│  └───────────────────────────────────────────────────────┘     │
│                            │                                     │
│                            │ HTTP Fetch API                     │
│                            │ (Controlled Polling)                │
│                            ▼                                     │
└─────────────────────────────────────────────────────────────────┘

                             ║
                    ═════════╬═════════
                             ║
                             ▼

┌─────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (Python)                       │
│  ┌───────────────────────────────────────────────────────┐     │
│  │                    REST API LAYER                      │     │
│  │                                                         │     │
│  │  /api/monitor/start  │  /api/benchmark/run            │     │
│  │  /api/monitor/stop   │  /api/comparison               │     │
│  │  /api/monitor/live   │  /api/health                   │     │
│  └───────────────────────────────────────────────────────┘     │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────┐     │
│  │              BUSINESS LOGIC LAYER                      │     │
│  │                                                         │     │
│  │  ┌──────────────────┐    ┌─────────────────────┐     │     │
│  │  │ Data Collection  │    │  Benchmark Engine   │     │     │
│  │  │  - psutil        │    │  - CPU test         │     │     │
│  │  │  - GPUtil        │    │  - RAM test         │     │     │
│  │  │  - disk_io       │    │  - Storage test     │     │     │
│  │  └──────────────────┘    │  - GPU classify     │     │     │
│  │                           └─────────────────────┘     │     │
│  │                                                         │     │
│  │  ┌──────────────────┐    ┌─────────────────────┐     │     │
│  │  │ Comparison Logic │    │  Health Calculator  │     │     │
│  │  │  - Score diff    │    │  - Overall score    │     │     │
│  │  │  - Status calc   │    │  - Bottleneck ID    │     │     │
│  │  └──────────────────┘    │  - Recommendations  │     │     │
│  │                           └─────────────────────┘     │     │
│  └───────────────────────────────────────────────────────┘     │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────┐     │
│  │                   DATA LAYER                           │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────┐     │     │
│  │  │  Reference Database (JSON)                   │     │     │
│  │  │  - Reference CPU score: 65                   │     │     │
│  │  │  - Reference RAM score: 70                   │     │     │
│  │  │  - Reference Storage: 60                     │     │     │
│  │  │  - Reference GPU: 65                         │     │     │
│  │  └──────────────────────────────────────────────┘     │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────┐     │     │
│  │  │  In-Memory Cache                             │     │     │
│  │  │  - Benchmark results                         │     │     │
│  │  │  - Monitoring history (60 points)            │     │     │
│  │  └──────────────────────────────────────────────┘     │     │
│  └───────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘

                             ║
                    ═════════╬═════════
                             ║
                             ▼

┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM LAYER (OS)                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   CPU    │  │   RAM    │  │   GPU    │  │   Disk   │       │
│  │ Hardware │  │ Hardware │  │ Hardware │  │ Hardware │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAMS

### 1. Live Monitoring Flow

```
┌──────────┐                                      ┌──────────┐
│  USER    │                                      │  FLASK   │
│ BROWSER  │                                      │  BACKEND │
└─────┬────┘                                      └────┬─────┘
      │                                                │
      │ 1. Click "Start" Button                       │
      ├──────────────────────────────────────────────►│
      │    POST /api/monitor/start                    │
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { "status": "started" }                    │
      │                                                │
      │ 2. setInterval Timer Starts                   │
      │    (Every 1s/2s/5s based on user)             │
      │                                                │
      │ 3. Fetch Live Data                            │
      ├──────────────────────────────────────────────►│
      │    GET /api/monitor/live                      │
      │                                                │
      │                                          4. Collect Data
      │                                           ┌─────────────┐
      │                                           │ psutil.cpu  │
      │                                           │ psutil.ram  │
      │                                           │ GPUtil.gpu  │
      │                                           │ disk_io     │
      │                                           └─────────────┘
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { cpu: {...}, ram: {...}, ... }           │
      │                                                │
      │ 5. Update UI                                  │
      │    - Update text values                       │
      │    - Update charts                            │
      │    - Update change indicators                 │
      │                                                │
      │ 6. Repeat every interval                      │
      │    (Until user clicks "Stop")                 │
      │                                                │
      │ 7. Click "Stop" Button                        │
      ├──────────────────────────────────────────────►│
      │    POST /api/monitor/stop                     │
      │                                                │
      │ 8. clearInterval()                            │
      │    Timer stopped immediately                  │
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { "status": "stopped" }                    │
      │                                                │
```

### 2. Benchmark Flow

```
┌──────────┐                                      ┌──────────┐
│  USER    │                                      │  FLASK   │
│ BROWSER  │                                      │  BACKEND │
└─────┬────┘                                      └────┬─────┘
      │                                                │
      │ 1. Click "Run Benchmark"                      │
      ├──────────────────────────────────────────────►│
      │    POST /api/benchmark/run                    │
      │                                                │
      │ 2. Show Loading Spinner                  3. Run Tests
      │    "Running benchmarks..."              ┌──────────────┐
      │                                         │ CPU Test (~1s)│
      │                                         │ RAM Test (~2s)│
      │                                         │ Disk Test(~2s)│
      │                                         │ GPU Test(<0.1s│
      │                                         └──────────────┘
      │                                                │
      │                                          4. Calculate
      │                                         ┌──────────────┐
      │                                         │ Normalize    │
      │                                         │ Overall Score│
      │                                         │ Find Bottlnck│
      │                                         └──────────────┘
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { benchmarks: {...}, overall: 76.1 }       │
      │                                                │
      │ 5. Display Results                            │
      │    - Individual scores                        │
      │    - Ratings                                  │
      │    - Chart                                    │
      │                                                │
      │ 6. Auto-fetch Comparison                      │
      ├──────────────────────────────────────────────►│
      │    GET /api/comparison                        │
      │                                                │
      │                                          7. Compare
      │                                         ┌──────────────┐
      │                                         │ Local vs Ref │
      │                                         │ Calculate %  │
      │                                         │ Determine    │
      │                                         │ Status       │
      │                                         └──────────────┘
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { local: {...}, reference: {...} }         │
      │                                                │
      │ 8. Auto-fetch Health                          │
      ├──────────────────────────────────────────────►│
      │    GET /api/health                            │
      │                                                │
      │                                          9. Generate
      │                                         ┌──────────────┐
      │                                         │ Health Score │
      │                                         │ Status       │
      │                                         │ Recommend.   │
      │                                         └──────────────┘
      │                                                │
      │◄───────────────────────────────────────────────┤
      │    { health: "Good", recommendations: [...] } │
      │                                                │
      │ 10. All tabs populated                        │
      │     User can view all data                    │
      │                                                │
```

---

## 🎨 UI COMPONENT HIERARCHY

```
┌─────────────────────────────────────────────────────────┐
│                      HEADER                             │
│  [SysOptima Logo] [Title] [Monitoring Status] [Time]   │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   NAVIGATION TABS                       │
│  [Live Monitor] [Benchmark] [Comparison] [Health]      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   TAB CONTENT AREA                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           LIVE MONITOR TAB                     │    │
│  │                                                  │    │
│  │  ┌────────────────────────────────────────┐    │    │
│  │  │    Control Panel                       │    │    │
│  │  │  [Refresh: 1s▼] [Start] [Stop]        │    │    │
│  │  └────────────────────────────────────────┘    │    │
│  │                                                  │    │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  │    │
│  │  │  CPU  │  │  RAM  │  │  GPU  │  │ DISK  │  │    │
│  │  │  Card │  │  Card │  │  Card │  │  Card │  │    │
│  │  │       │  │       │  │       │  │       │  │    │
│  │  │ [Icon]│  │ [Icon]│  │ [Icon]│  │ [Icon]│  │    │
│  │  │  45%  │  │ 8.3GB │  │  32%  │  │ 45MB/s│  │    │
│  │  │ +2%   │  │ +0.1GB│  │  +5%  │  │ Active│  │    │
│  │  │       │  │       │  │       │  │       │  │    │
│  │  │[Chart]│  │[Chart]│  │[Chart]│  │[Chart]│  │    │
│  │  └───────┘  └───────┘  └───────┘  └───────┘  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           BENCHMARK TAB                        │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │  [Description]    [Run Benchmark Button] │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                                                  │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │    │
│  │  │  CPU   │ │  RAM   │ │Storage │ │  GPU   │ │    │
│  │  │ Score  │ │ Score  │ │ Score  │ │ Score  │ │    │
│  │  │  79.8  │ │  39.5  │ │  100   │ │  85    │ │    │
│  │  │ ABOVE  │ │ BELOW  │ │ ABOVE  │ │ ABOVE  │ │    │
│  │  │  AVG   │ │  AVG   │ │  AVG   │ │  AVG   │ │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │        Overall Score: 76.1               │  │    │
│  │  │        Bottleneck: RAM                   │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │      [Component Scores Bar Chart]        │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           COMPARISON TAB                       │    │
│  │                                                  │    │
│  │  ┌──────────────────┐  ┌─────────────────┐    │    │
│  │  │  Radar Chart     │  │  Status Table   │    │    │
│  │  │  Local vs Ref    │  │  CPU: Above Avg │    │    │
│  │  │                  │  │  RAM: Below Avg │    │    │
│  │  │                  │  │  Storage: Above │    │    │
│  │  │                  │  │  GPU: Above Avg │    │    │
│  │  └──────────────────┘  └─────────────────┘    │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │  Detailed Comparison Table               │  │    │
│  │  │  Component | Your Score | Ref | Diff %   │  │    │
│  │  │  CPU       |    79.8    | 65  | +22.8%  │  │    │
│  │  │  ...                                      │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           SYSTEM HEALTH TAB                    │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │      Overall System Health               │  │    │
│  │  │            76.1%                         │  │    │
│  │  │            Good                          │  │    │
│  │  │      Bottleneck: RAM                     │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │      Recommendations                     │  │    │
│  │  │  🔴 HIGH: Close memory apps             │  │    │
│  │  │  🟡 MED: Upgrade RAM                    │  │    │
│  │  │  🔵 LOW: Update drivers                 │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      FOOTER                             │
│     SysOptima - B.Sc. IT Final Year Project            │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 LAG PREVENTION MECHANISMS

### 1. Single Timer Pattern

```javascript
// ❌ WRONG - Multiple timers (LAG)
function startMonitoring() {
    setInterval(fetchData, 1000);  // Timer 1
}
// If called twice, you get 2 timers!

// ✅ CORRECT - Single timer (NO LAG)
let monitoringTimer = null;

function startMonitoring() {
    if (monitoringTimer) return;  // Prevent duplicate
    monitoringTimer = setInterval(fetchData, 1000);
}

function stopMonitoring() {
    if (monitoringTimer) {
        clearInterval(monitoringTimer);
        monitoringTimer = null;
    }
}
```

### 2. Efficient DOM Updates

```javascript
// ❌ WRONG - Full re-render (LAG)
function updateCard(data) {
    document.getElementById('card').innerHTML = `
        <div class="card">
            <h3>CPU</h3>
            <p>${data.value}%</p>
            <canvas id="chart"></canvas>
        </div>
    `;
    // Recreates everything!
}

// ✅ CORRECT - Update only changed values (NO LAG)
function updateCard(data) {
    document.getElementById('cpu-value').textContent = data.value + '%';
    // Only updates one text node
}
```

### 3. Chart Update Optimization

```javascript
// ❌ WRONG - Recreate chart (LAG)
function updateChart(data) {
    if (chart) chart.destroy();
    chart = new Chart(ctx, { data: data });
}

// ✅ CORRECT - Update data only (NO LAG)
function updateChart(data) {
    chart.data.datasets[0].data = data;
    chart.update('none');  // 'none' = no animation
}
```

### 4. History Limiting

```javascript
// ❌ WRONG - Unlimited growth (LAG)
function addDataPoint(value) {
    history.push(value);
    // Grows forever, slows down over time
}

// ✅ CORRECT - Fixed size (NO LAG)
function addDataPoint(value) {
    history.push(value);
    if (history.length > 60) {
        history.shift();  // Remove oldest
    }
}
```

---

## 📊 SCORING ALGORITHM

### Benchmark Score Calculation

```python
# CPU Score Calculation
def calculate_cpu_score(execution_time):
    """
    Lower time = Better performance
    Reference: 1.0 second = 65 score
    """
    reference_time = 1.0
    score = (reference_time / execution_time) * 65
    
    # Normalize to 0-100
    score = min(100, max(0, score))
    return score

# RAM Score Calculation
def calculate_ram_score(speed_gbps):
    """
    Higher speed = Better performance
    Reference: 10 GB/s = 70 score
    """
    reference_speed = 10.0
    score = (speed_gbps / reference_speed) * 70
    
    # Normalize to 0-100
    score = min(100, max(0, score))
    return score

# Storage Score Calculation
def calculate_storage_score(speed_mbps):
    """
    Higher speed = Better performance
    Reference: 100 MB/s = 60 score
    """
    reference_speed = 100.0
    score = (speed_mbps / reference_speed) * 60
    
    # Normalize to 0-100
    score = min(100, max(0, score))
    return score

# GPU Score Classification
def classify_gpu(gpu_memory_gb):
    """
    Based on GPU memory capacity
    """
    if gpu_memory_gb < 4:
        return "Entry Level", 50
    elif gpu_memory_gb < 8:
        return "Mid Range", 75
    else:
        return "High End", 95
```

### Overall Score

```python
overall_score = (cpu_score + ram_score + storage_score + gpu_score) / 4
```

### Bottleneck Identification

```python
scores = {
    'CPU': cpu_score,
    'RAM': ram_score,
    'Storage': storage_score,
    'GPU': gpu_score
}

bottleneck = min(scores, key=scores.get)
# Returns component with LOWEST score
```

---

## 🎯 KEY DESIGN DECISIONS

### 1. Why REST API instead of WebSockets?

| REST API | WebSockets |
|----------|------------|
| ✅ Simpler implementation | ❌ Complex setup |
| ✅ Better debugging | ❌ Hard to debug |
| ✅ User-controlled | ❌ Always-on overhead |
| ✅ No connection management | ❌ Reconnection logic needed |
| ✅ Works everywhere | ❌ Firewall issues |

**Decision:** REST API with controlled polling

### 2. Why Vanilla JS instead of React/Vue?

| Vanilla JS | React/Vue |
|------------|-----------|
| ✅ No build step | ❌ Requires webpack/vite |
| ✅ Instant load | ❌ Bundle size |
| ✅ Easy to understand | ❌ Learning curve |
| ✅ Full control | ❌ Framework overhead |
| ✅ Viva-friendly | ❌ Hard to explain |

**Decision:** Vanilla JavaScript

### 3. Why In-Memory Cache instead of Database?

| In-Memory | Database |
|-----------|----------|
| ✅ Instant access | ❌ Query overhead |
| ✅ No setup needed | ❌ Installation required |
| ✅ Perfect for temp data | ❌ Overkill for this use |
| ✅ No persistence needed | ❌ Adds complexity |

**Decision:** In-memory cache with 60-point limit

---

## 📱 RESPONSIVE DESIGN

The UI uses Tailwind's responsive classes:

```html
<!-- Mobile: 1 column, Tablet: 2 columns, Desktop: 4 columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- Cards -->
</div>
```

**Breakpoints:**
- `sm:` - 640px and up (Mobile)
- `md:` - 768px and up (Tablet)
- `lg:` - 1024px and up (Desktop)
- `xl:` - 1280px and up (Large Desktop)

---

## 🎓 ACADEMIC JUSTIFICATION

**This project demonstrates:**

1. **Web Technologies:** HTML, CSS, JavaScript, Python, Flask
2. **Architecture:** Client-Server, REST API, MVC pattern
3. **System Programming:** Hardware monitoring, benchmarking
4. **UI/UX Design:** Responsive, intuitive, professional
5. **Algorithm Design:** Scoring, comparison, recommendations
6. **Performance Optimization:** Lag prevention, efficient updates
7. **Documentation:** Comprehensive guides for viva

**Suitable for B.Sc. IT Final Year Project ✅**

---

**For Viva Presentation:**
- Use architecture diagrams to explain system
- Show data flow for clarity
- Demonstrate lag prevention techniques
- Explain scoring algorithms
- Justify design decisions

**Good Luck! 🎓**
