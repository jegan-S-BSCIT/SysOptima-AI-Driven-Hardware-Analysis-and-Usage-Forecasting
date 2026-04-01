"""
SysOptima UI Implementation Guide
How to use and extend the professional UI system
"""

# ============================================================================
# QUICK START GUIDE
# ============================================================================

"""
To run the application with the new professional UI:

    python main_application.py

This launches the SysOptima main window with the complete interface.
"""

# ============================================================================
# FILE STRUCTURE & ORGANIZATION
# ============================================================================

"""
SysOptima/
│
├─ main_application.py          ← Application entry point
│
├─ ui/                          ← All UI components
│  ├─ __init__.py
│  ├─ theme.py                  ← Design system & color palette
│  ├─ modern_ui.py              ← Main UI components
│  ├─ visualizations.py         ← Chart & graph components
│  └─ analytics_dashboard.py    ← Advanced analytics views
│
├─ core/                        ← Business logic
│  ├─ hardware_detector.py      ← System info detection
│  ├─ benchmark_engine.py       ← Performance benchmarking
│  └─ diagnostics_engine.py     ← AI-powered diagnostics
│
├─ docs/                        ← Documentation
│  ├─ DESIGN_SYSTEM.md          ← Design principles
│  ├─ UI_SHOWCASE.md            ← UI showcase
│  ├─ VISUAL_STYLE_GUIDE.md     ← Visual guidelines
│  └─ IMPLEMENTATION_GUIDE.md   ← This file
│
└─ requirements.txt             ← Dependencies
"""

# ============================================================================
# USING THE THEME SYSTEM
# ============================================================================

"""
Example 1: Basic Component Creation
─────────────────────────────────────────────────────────────

from ui.theme import theme
import customtkinter as ctk

class MyComponent(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=theme.colors.card_bg,
            corner_radius=theme.border_radius.lg,
            **kwargs
        )
        
        # Add label
        label = ctk.CTkLabel(
            self,
            text="Hello World",
            font=(theme.typography.font_primary, theme.typography.size_base),
            text_color=theme.colors.text_primary
        )
        label.pack(padx=theme.spacing.lg, pady=theme.spacing.lg)


Example 2: Using Status Colors
─────────────────────────────────────────────────────────────

# Get color based on health percentage
color = theme.get_status_color(85)  # Returns #10B981 (success)
color = theme.get_status_color(45)  # Returns #F59E0B (warning)
color = theme.get_status_color(20)  # Returns #EF4444 (danger)

# Use in components
progress_bar = ctk.CTkProgressBar(
    parent,
    progress_color=theme.get_status_color(cpu_usage_percent)
)


Example 3: Accessing Theme Values
─────────────────────────────────────────────────────────────

# Colors
bg_color = theme.colors.primary_dark
text_color = theme.colors.text_primary
accent = theme.colors.accent_cyan

# Typography
font_size = theme.typography.size_lg
font_family = theme.typography.font_primary

# Spacing
padding = theme.spacing.lg
margin = theme.spacing.xl

# Border radius
radius = theme.border_radius.md

# Status colors
success = theme.colors.success
warning = theme.colors.warning
danger = theme.colors.danger
"""

# ============================================================================
# CREATING NEW VIEWS
# ============================================================================

"""
Template: Creating a New Dashboard View
─────────────────────────────────────────────────────────────

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame
from ui.theme import theme


class MyNewView(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_bg, **kwargs)
        
        # Create scrollable container
        scroll_frame = CTkScrollableFrame(
            self,
            fg_color=theme.colors.primary_bg,
            label_text="My View Title",
            label_font=(
                theme.typography.font_primary,
                theme.typography.size_lg,
                "bold"
            ),
            label_text_color=theme.colors.text_primary
        )
        scroll_frame.pack(fill="both", expand=True, 
                         padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Add sections
        self._create_section1(scroll_frame)
        self._create_section2(scroll_frame)
    
    def _create_section1(self, parent):
        \"\"\"Create first section\"\"\"
        section = self._create_section("Section 1", parent)
        
        # Add content
        label = CTkLabel(
            section,
            text="Content here...",
            text_color=theme.colors.text_primary
        )
        label.pack(padx=theme.spacing.lg, pady=theme.spacing.lg)
    
    def _create_section2(self, parent):
        \"\"\"Create second section\"\"\"
        section = self._create_section("Section 2", parent)
        
        # Add more content
        pass
    
    def _create_section(self, title, parent):
        \"\"\"Helper: Create a section frame\"\"\"
        section = CTkFrame(
            parent,
            fg_color=theme.colors.card_bg,
            corner_radius=theme.border_radius.lg
        )
        section.pack(fill="both", expand=False, pady=theme.spacing.lg)
        
        # Add title
        title_label = CTkLabel(
            section,
            text=title,
            font=(theme.typography.font_primary, 
                  theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        return section


# To integrate into main window, update modern_ui.py:

def _show_my_new_view(self):
    MyNewView(self.content_area).pack(fill="both", expand=True)

# Add to sidebar navigation and tab handling
"""

# ============================================================================
# CREATING CHARTS & VISUALIZATIONS
# ============================================================================

"""
Chart Creation Examples
─────────────────────────────────────────────────────────────

from ui.visualizations import LineChart, BarChart, PieChart
import numpy as np

# Example 1: Line Chart
────────────────────────
data = {
    'CPU Usage': np.array([40, 42, 45, 43, 40, 38, 42, 45, 48, 50]),
    'Memory Usage': np.array([60, 62, 65, 63, 60, 58, 62, 65, 68, 70]),
}

chart = LineChart(
    parent,
    title="System Metrics Over Time",
    data_series=data,
    height=300
)
chart.pack(fill="both", expand=True, padx=16, pady=16)


# Example 2: Bar Chart
──────────────────────
processes = ['Chrome', 'VS Code', 'Explorer', 'Discord', 'Steam']
usage = [18, 12, 8, 5, 3]

chart = BarChart(
    parent,
    title="Top CPU Processes",
    categories=processes,
    values=usage,
    color=theme.colors.chart_blue,
    height=300
)
chart.pack(fill="both", expand=True)


# Example 3: Pie Chart
──────────────────────
labels = ['System', 'Applications', 'User Data', 'Media', 'Other']
sizes = [150, 250, 300, 200, 100]

chart = PieChart(
    parent,
    title="Disk Space Distribution",
    labels=labels,
    sizes=sizes,
    height=300
)
chart.pack(fill="both", expand=True)


# Example 4: Metric Gauge
─────────────────────────
gauge = MetricGauge(
    parent,
    label="CPU Usage",
    value=42,
    max_value=100
)
gauge.pack(fill="both", expand=True, padx=16, pady=16)
"""

# ============================================================================
# COMPONENT LIBRARY REFERENCE
# ============================================================================

"""
HeaderBar
────────────────────────────────────────────────────────────
Professional header with logo and status indicators.

from ui.modern_ui import HeaderBar

header = HeaderBar(parent)
header.pack(fill="x", side="top")


StatCard
────────────────────────────────────────────────────────────
Metric card with icon, title, value, and trend.

from ui.modern_ui import StatCard

card = StatCard(
    parent,
    icon="🔧",
    title="CPU Usage",
    value="42",
    unit="%",
    color=theme.colors.chart_blue,
    trend="↓ 5% from avg"
)
card.pack(fill="x", padx=16, pady=16)


HealthBar
────────────────────────────────────────────────────────────
Progress bar with health indicator.

from ui.modern_ui import HealthBar

bar = HealthBar(parent, label="CPU Temperature", percentage=65)
bar.pack(fill="x", padx=16, pady=8)


DetailPanel
────────────────────────────────────────────────────────────
Information display panel.

from ui.modern_ui import DetailPanel

panel = DetailPanel(parent, title="CPU Information")
panel.add_info_row("Processor", "Intel Core i7")
panel.add_info_row("Cores", "16")
panel.pack(fill="x", pady=16)


Sidebar
────────────────────────────────────────────────────────────
Navigation sidebar with tabs.

from ui.modern_ui import Sidebar

def on_tab_change(tab_key):
    print(f"Tab changed to: {tab_key}")

sidebar = Sidebar(parent, on_tab_change=on_tab_change)
sidebar.pack(fill="both", side="left")


DashboardPanel
────────────────────────────────────────────────────────────
Main dashboard view.

from ui.modern_ui import DashboardPanel

dashboard = DashboardPanel(parent)
dashboard.pack(fill="both", expand=True)


AnalyticsDashboard
────────────────────────────────────────────────────────────
Advanced analytics view.

from ui.analytics_dashboard import AnalyticsDashboard

analytics = AnalyticsDashboard(parent)
analytics.pack(fill="both", expand=True)


DiagnosticsView
────────────────────────────────────────────────────────────
AI diagnostics view.

from ui.analytics_dashboard import DiagnosticsView

diagnostics = DiagnosticsView(parent)
diagnostics.pack(fill="both", expand=True)
"""

# ============================================================================
# EXTENDING THE THEME SYSTEM
# ============================================================================

"""
Adding New Colors
─────────────────────────────────────────────────────────────

In ui/theme.py, add to ColorPalette class:

@dataclass
class ColorPalette:
    # ... existing colors ...
    
    # NEW COLOR
    my_custom_color: str = "#YOUR_HEX_CODE"


Then use it:

    label_color = theme.colors.my_custom_color


Adding New Spacing Values
─────────────────────────────────────────────────────────────

In ui/theme.py, add to Spacing class:

@dataclass
class Spacing:
    # ... existing spacing ...
    
    # NEW SPACING
    custom: int = 20  # 20 pixels


Then use it:

    widget.pack(padx=theme.spacing.custom)


Adding Helper Methods
─────────────────────────────────────────────────────────────

In ui/theme.py, add to SysOptimaTheme class:

def get_custom_color(self, metric_type: str) -> str:
    \"\"\"Get color based on metric type\"\"\"
    color_map = {
        'cpu': self.colors.chart_blue,
        'memory': self.colors.chart_cyan,
        'disk': self.colors.chart_indigo,
        'gpu': self.colors.chart_pink,
    }
    return color_map.get(metric_type, self.colors.text_primary)


Then use it:

    color = theme.get_custom_color('cpu')  # Returns blue
"""

# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
1. ALWAYS USE THE THEME SYSTEM
   ❌ Bad:  fg_color="#1A1F35"
   ✅ Good: fg_color=theme.colors.card_bg

2. MAINTAIN CONSISTENT SPACING
   ❌ Bad:  padx=15, pady=10
   ✅ Good: padx=theme.spacing.lg, pady=theme.spacing.md

3. USE SEMANTIC COLORS FOR STATUS
   ❌ Bad:  "Good" → blue, "Bad" → red (unclear)
   ✅ Good: theme.colors.success, theme.colors.danger

4. TEST ON DIFFERENT RESOLUTIONS
   Test at: 1600x900, 1200x800, 1024x768

5. ENSURE ACCESSIBILITY
   - Minimum 12px font size
   - 4.5:1 contrast ratio
   - 48px+ touch targets
   - Keyboard navigation support

6. KEEP COMPONENTS FOCUSED
   One component = one responsibility
   Avoid mixing different functionalities

7. USE CONSISTENT TRANSITIONS
   Duration: 200ms
   Easing: ease-in-out
   Properties: color, opacity, transform

8. FOLLOW THE SPACING GRID
   All spacing must be multiples of 4px
   Use theme.spacing values for consistency

9. DOCUMENT YOUR COMPONENTS
   Include docstrings explaining usage
   Provide parameter descriptions
   Show usage examples

10. TEST PERFORMANCE
    Monitor FPS during interactions
    Profile memory usage
    Optimize chart rendering if needed
"""

# ============================================================================
# INTEGRATION WITH BACKEND
# ============================================================================

"""
Connecting Real Data
─────────────────────────────────────────────────────────────

from core.hardware_detector import HardwareDetector

class MyView(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.detector = HardwareDetector()
        
        # Fetch hardware info
        hw_info = self.detector.detect()
        cpu_usage = hw_info['cpu']['usage']
        
        # Update UI
        self._update_metrics(cpu_usage)
    
    def _update_metrics(self, cpu_usage):
        # Update display components
        pass


Real-time Updates
─────────────────────────────────────────────────────────────

class MonitorView(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.detector = HardwareDetector()
        self._start_monitoring()
    
    def _start_monitoring(self):
        # Update every second
        self.after(1000, self._update_and_refresh)
    
    def _update_and_refresh(self):
        metrics = self.detector.detect()
        # Update UI with new metrics
        self._start_monitoring()  # Schedule next update
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Issue: Colors look different than expected
Solution: 
  1. Verify appearance mode: ctk.set_appearance_mode("dark")
  2. Check theme colors in ui/theme.py
  3. Ensure using theme.colors values, not hardcoded hex
  4. Test on different monitors

Issue: Text is hard to read
Solution:
  1. Check contrast ratio (should be 4.5:1+)
  2. Increase font size if needed
  3. Use brighter text color
  4. Add background contrast
  5. Verify using theme.colors.text_* values

Issue: Layout looks misaligned
Solution:
  1. Verify spacing uses theme.spacing values
  2. Check pack(fill=...) parameters
  3. Ensure parent containers have proper sizing
  4. Use consistent padding throughout

Issue: Charts are rendering slowly
Solution:
  1. Reduce chart update frequency
  2. Limit data points displayed
  3. Use appropriate DPI settings (100)
  4. Consider canvas caching

Issue: UI is not responsive
Solution:
  1. Ensure proper pack/grid configuration
  2. Check for blocking operations
  3. Use threading for long operations
  4. Verify update rates
"""

# ============================================================================
# NEXT STEPS
# ============================================================================

"""
Future Enhancements:

1. Light Theme Support
   - Create alternative color palette
   - Add theme switcher
   - Save user preference

2. Custom Theming
   - Allow users to customize colors
   - Preset theme options
   - Export/import themes

3. Advanced Animations
   - Tab transitions
   - Data value animations
   - Smooth chart updates

4. Real-time Data Streaming
   - WebSocket integration
   - Live data updates
   - Historical data recording

5. Export Functionality
   - Save screenshots
   - Export data as CSV/JSON
   - Generate reports

6. Keyboard Shortcuts
   - Tab navigation
   - Common actions
   - Accessibility shortcuts

7. Multi-language Support
   - Internationalization (i18n)
   - Language selection
   - Translation files

8. Mobile Responsiveness
   - Responsive layouts
   - Touch-friendly controls
   - Mobile-optimized views
"""

# ============================================================================

class ImplementationGuide:
    """Reference guide for SysOptima UI implementation"""
    pass
