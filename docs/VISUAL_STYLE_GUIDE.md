# SysOptima UI Visual Style Guide

## Application Layout Overview

```
╔════════════════════════════════════════════════════════════════════════════╗
║ ⚙️ SysOptima - System Intelligence Platform                   ● Healthy   ║  HEADER BAR
╠══════════════════╦═══════════════════════════════════════════════════════╣
║ Navigation       ║  Dashboard - System Overview                         ║
║                  ║                                                       ║
║ 📊 Dashboard     ║  ┌─────────────────────────────────────────────────┐ ║
║ 🔍 Hardware      ║  │ Quick Metrics Overview                           │ ║
║ 📈 Performance   ║  ├─────────────────────────────────────────────────┤ ║
║ 🤖 Diagnostics   ║  │                                                 │ ║
║ 📡 Monitor       ║  │ 🔧 CPU Usage    💾 Memory Usage                 │ ║
║ 🎮 Benchmarks    ║  │ ┌──────────────┐  ┌──────────────┐             │ ║
║                  ║  │ │  42%         │  │  68%         │             │ ║
║ ⚙️ Settings      ║  │ │ ↓ 5% from avg│  │ ↑ 2% from avg│             │ ║
║ ℹ️ About         ║  │ └──────────────┘  └──────────────┘             │ ║
║                  ║  │                                                 │ ║
║                  ║  │ 💿 Disk Usage   🎮 GPU Usage                   │ ║
║                  ║  │ ┌──────────────┐  ┌──────────────┐             │ ║
║                  ║  │ │  56%         │  │  28%         │             │ ║
║                  ║  │ │ → Stable     │  │ ↓ 8% from avg│             │ ║
║                  ║  │ └──────────────┘  └──────────────┘             │ ║
║                  ║  │                                                 │ ║
║                  ║  ├─────────────────────────────────────────────────┤ ║
║                  ║  │ System Health                                   │ ║
║                  ║  │                                                 │ ║
║                  ║  │ CPU Temperature    ████████░░░  65%             │ ║
║                  ║  │ Memory Health      ██████████░░  82%             │ ║
║                  ║  │ Disk Health        █████████░░░  55%             │ ║
║                  ║  │ System Overall     ███████░░░░░  72%             │ ║
║                  ║  │                                                 │ ║
║                  ║  └─────────────────────────────────────────────────┘ ║
║                  ║                                                       ║
╚══════════════════╩═══════════════════════════════════════════════════════╝
```

## Color Scheme Visualization

```
PRIMARY PALETTE:
┌─────────────────────────────────────────────────────────────┐
│ Primary Dark        ▓▓▓▓▓▓▓▓  #0F172A  (Main Background)   │
│ Primary BG          ░░░░░░░░  #1A1F35  (Secondary BG)      │
│ Primary Accent      ░░░░░░░░  #1E40AF  (CTAs, Highlights)  │
│                                                               │
│ Accent Cyan         ▒▒▒▒▒▒▒▒  #06B6D4  (Data Highlights)   │
│ Accent Teal         ▒▒▒▒▒▒▒▒  #0891B2  (Secondary)         │
│ Accent Indigo       ▒▒▒▒▒▒▒▒  #4F46E5  (Tertiary)          │
└─────────────────────────────────────────────────────────────┘

SEMANTIC COLORS:
┌─────────────────────────────────────────────────────────────┐
│ Success (Green)     ▓▓▓▓▓▓▓▓  #10B981  (Healthy Systems)   │
│ Warning (Amber)     ▓▓▓▓▓▓▓▓  #F59E0B  (Warning State)     │
│ Danger (Red)        ▓▓▓▓▓▓▓▓  #EF4444  (Critical/Error)    │
│ Info (Blue)         ▓▓▓▓▓▓▓▓  #3B82F6  (Informational)     │
└─────────────────────────────────────────────────────────────┘

TEXT COLORS:
┌─────────────────────────────────────────────────────────────┐
│ Primary Text        ░░░░░░░░  #F1F5F9  (Main Text)         │
│ Secondary Text      ░░░░░░░░  #CBD5E1  (Secondary)         │
│ Tertiary Text       ░░░░░░░░  #94A3B8  (Meta Info)         │
│ Disabled Text       ░░░░░░░░  #475569  (Disabled State)    │
└─────────────────────────────────────────────────────────────┘

CHART COLORS:
┌─────────────────────────────────────────────────────────────┐
│ Chart Blue          ▒▒▒▒▒▒▒▒  #3B82F6  (Primary Data)      │
│ Chart Cyan          ▒▒▒▒▒▒▒▒  #06B6D4  (Secondary Data)    │
│ Chart Indigo        ▒▒▒▒▒▒▒▒  #4F46E5  (Tertiary Data)     │
│ Chart Purple        ▒▒▒▒▒▒▒▒  #A855F7  (Quaternary Data)   │
│ Chart Pink          ▒▒▒▒▒▒▒▒  #EC4899  (Quinary Data)      │
└─────────────────────────────────────────────────────────────┘
```

## Component Styles

### Stat Card
```
┌──────────────────────────────────────┐
│ 🔧 CPU Usage        CPU: 42%         │
│                                      │
│ Current CPU Usage                    │
│                                      │
│ 42%                                  │
│ ↓ 5% from avg                        │
│                                      │
└──────────────────────────────────────┘

Elements:
- Icon (20px, colored)
- Title (12px, secondary text)
- Value (24px bold, primary text)
- Trend (11px, tertiary text)
- Background: #1A1F35 with 12px radius
```

### Health Bar
```
┌────────────────────────────────────────┐
│ CPU Temperature                    65% │
│ ████████████░░░░░░░░░░░░░░░░░░░░░   │
│                                        │
│ Memory Health                      82% │
│ ██████████████░░░░░░░░░░░░░░░░░░░   │
│                                        │
│ Disk Health                        55% │
│ ███████████░░░░░░░░░░░░░░░░░░░░░░   │
│                                        │
│ System Overall                     72% │
│ ███████████████░░░░░░░░░░░░░░░░░░   │
└────────────────────────────────────────┘

Progress Bar:
- Height: 8px
- Filled Color: Status color (green/amber/red)
- Background: #1E293B
- Label: 14px primary text + percentage in status color
```

### Detail Panel
```
┌────────────────────────────────────────┐
│ 🔧 CPU Information                     │
├────────────────────────────────────────┤
│ Processor        Intel Core i7-13700K  │
│ Cores            16 (8P + 8E)          │
│ Base Frequency   3.4 GHz                │
│ Max Frequency    5.4 GHz                │
│ Cache            30 MB                  │
└────────────────────────────────────────┘

Structure:
- Title: 14px bold in accent color
- Rows: Label (secondary) | Value (primary/bold)
- Spacing: 8px between rows
- Background: #1A1F35 with 12px radius
- Padding: 16px
```

### Metric Gauge
```
                    ┌─ Current value (large, bold)
                    │
                ╱───┴───╲
              ╱  ▓▓▓▓▓▓  ╲        ┌─ Arc color (status color)
            ╱   ▓▓▓▓▓▓   ╲  ← ← ← ┤   Green: 80+%
          ╱     ▓▓▓▓▓▓      ╲     │   Amber: 40-79%
         │      ▓ 85 ▓      │  ← ← ┤   Red: < 40%
         │      ▓▓▓▓▓▓      │       │
          ╲    Memory       ╱       └─ Label
            ╲              ╱
              ╲__________╱

Appearance:
- Circular gauge with background arc
- Colored value arc from left to right
- Value centered and prominent
- Label below in secondary text
```

### Chart Layout
```
Chart Title
┌────────────────────────────────────────┐
│ y-axis                                 │
│     │   ▲    ▲      ▲                  │
│     │  ╱ ╲  ╱ ╲    ╱ ╲  ← Line 1 (Blue)│
│     │ ╱   ╲╱   ╲  ╱   ╲                │
│     │            ╲╱     ─ ← Line 2      │
│ ────┼──────────────────────────────────│
│     │ Grid lines (light, low opacity)  │
│     └───x-axis ────────────────────────│
│              Legend                    │
│              ■ Line 1: Blue            │
│              ■ Line 2: Cyan            │
└────────────────────────────────────────┘

Features:
- Dark background (#0F172A)
- Light grid lines (0.1 alpha)
- Clear axis labels (secondary text)
- Legend with color indicators
- Consistent font sizing
```

## Typography Scale

```
Size Reference:
─────────────────────────────────────
32px  ▌ XXL - Main Page Titles
28px  ▌ XL  - Section Headers
24px  ▌ LG  - Large Headers
16px  ▌ MD  - Subheadings
14px  ▌ Base - Body Text (Default)
12px  ▌ SM  - Secondary Text
11px  ▌ XS  - Tertiary Text
─────────────────────────────────────

Weight Examples:
┌────────────────────────────────┐
│ Light (300)         Subtle     │
│ Normal (400)   Regular Text    │
│ Medium (500)    Emphasized     │
│ Semibold (600)  Section Titles  │
│ Bold (700)    Important Headers │
└────────────────────────────────┘

Font: Segoe UI (Professional, Clean, Native)
```

## Spacing System

```
Spacing Grid (8px base):
┌─────────────────────────────────┐
│ xs: 4px   (tight)               │
│ sm: 8px   (adjacent)            │
│ md: 12px  (standard)            │
│ lg: 16px  (component padding)   │
│ xl: 24px  (section break)       │
│ xxl: 32px (page margin)         │
│ xxxl: 48px (large containers)   │
└─────────────────────────────────┘

Application:
┌─────────────────────────────────────────┐
│ ┌─── xxl spacing ───────────────────┐   │
│ │ ┌─── lg padding ──────────────┐  │   │
│ │ │ Component Title             │  │   │
│ │ │ ┌ md spacing ┐              │  │   │
│ │ │ │ Item 1     │ sm spacing   │  │   │
│ │ │ │ Item 2     │              │  │   │
│ │ │ └────────────┘              │  │   │
│ │ └─────────────────────────────┘  │   │
│ └────────────────────────────────────┘   │
│ ────── lg spacing ──────────────────────│
│ Next Component                           │
└─────────────────────────────────────────┘
```

## Interactive States

### Button/Tab States
```
DEFAULT:              HOVER:                ACTIVE:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Dashboard    │     │ Dashboard    │     │ Dashboard    │
│ (Secondary)  │  →  │ (Highlighted)│  →  │ (Accent BG)  │
└──────────────┘     └──────────────┘     └──────────────┘

Transition: 200ms smooth animation
```

### Text Input States
```
DEFAULT:                FOCUS:                 DISABLED:
┌──────────────────┐  ┌──────────────────┐   ┌──────────────────┐
│ Enter value...   │  │ Enter value...   │   │ [Disabled text]  │
│ (#0F172A bg)     │  │ (Accent border)  │   │ (50% opacity)    │
└──────────────────┘  └──────────────────┘   └──────────────────┘
```

## Responsive Breakpoints

```
Desktop (1600x900):
┌─────────────────────────────────────────────┐
│ [Sidebar] [Full Dashboard with 4 columns] │
└─────────────────────────────────────────────┘

Tablet (1200x800):
┌─────────────────────────────────────────────┐
│ [Sidebar] [Dashboard with 2-3 columns]    │
│           [Scrollable Content]              │
└─────────────────────────────────────────────┘

Mobile (800x600):
┌──────────────────────────┐
│ [Sidebar: Icons Only]    │
│ [Dashboard: 1 column]    │
│ [Scrollable Content]     │
└──────────────────────────┘
```

## Design Tokens Summary

```python
# COLOR TOKENS
colors = {
    'primary_dark': '#0F172A',      # Main background
    'primary_bg': '#1A1F35',        # Secondary background
    'primary_accent': '#1E40AF',    # Primary interactions
    'accent_cyan': '#06B6D4',       # Data highlights
    'text_primary': '#F1F5F9',      # Main text
    'text_secondary': '#CBD5E1',    # Secondary text
    'success': '#10B981',           # Healthy
    'warning': '#F59E0B',           # Alert
    'danger': '#EF4444',            # Critical
}

# SPACING TOKENS
spacing = {
    'xs': 4,    'sm': 8,    'md': 12,
    'lg': 16,   'xl': 24,   'xxl': 32,
}

# TYPOGRAPHY TOKENS
typography = {
    'font': 'Segoe UI',
    'sizes': {
        'xxl': 32, 'xl': 28, 'lg': 24, 'md': 16,
        'base': 14, 'sm': 12, 'xs': 11,
    },
    'weights': {
        'light': 300, 'normal': 400, 'medium': 500,
        'semibold': 600, 'bold': 700,
    },
}

# BORDER RADIUS TOKENS
radius = {
    'none': 0,   'sm': 4,    'md': 8,
    'lg': 12,    'xl': 16,   'full': 9999,
}
```

## Usage Guidelines

### ✅ DO

- Use the centralized theme system
- Maintain consistent spacing with the grid
- Use semantic colors for status
- Apply smooth transitions (200ms)
- Keep components focused and simple
- Use high contrast text
- Provide clear hover states
- Test accessibility compliance

### ❌ DON'T

- Hardcode colors (use theme)
- Mix spacing values inconsistently
- Use low contrast combinations
- Add jarring animations
- Overload components with information
- Ignore touch target sizes
- Skip hover/focus states
- Ignore accessibility guidelines

## Animation Principles

```
Hover Transition:
    Duration: 200ms
    Easing: ease-in-out
    Properties: background-color, opacity

Example:
    DEFAULT → HOVER (200ms)
    #1A1F35 → #2D3748 (smoother interaction)
```

---

This style guide ensures a cohesive, professional appearance throughout SysOptima. 
All components should follow these standards for consistency and quality.
