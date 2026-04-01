# SysOptima - Visual Assets & Icon Guide

## 🎨 Emoji Icons Used Throughout UI

The SysOptima UI uses consistent emoji icons for intuitive visual communication:

### Navigation Icons
```
📊  Dashboard           - Main overview and quick stats
🔍  Hardware Info       - System specifications
📈  Performance         - Advanced analytics
🤖  AI Diagnostics     - AI-powered insights
📡  Real-time Monitor   - Live metrics streaming
🎮  Benchmarks         - Performance testing
⚙️   Settings           - Application configuration
ℹ️   About              - Application information
```

### Component Icons
```
🔧  CPU                 - Processor/computation
💾  Memory              - RAM and storage
💿  Disk                - Hard drive/storage
🎮  GPU                 - Graphics processor
⚡  Power               - Energy/performance
🌡️   Temperature         - Heat monitoring
📊  Analytics           - Data analysis
📉  Trends              - Historical data
🎯  Target              - Performance goal
✓   Success             - Healthy status
⚠   Warning             - Alert status
✗   Error               - Critical status
●   Status Indicator    - Live status dot
```

### Status Indicators
```
● Green (#10B981)       - Healthy, good status
● Amber (#F59E0B)       - Warning, caution
● Red (#EF4444)         - Critical, error
● Blue (#3B82F6)        - Informational
● Cyan (#06B6D4)        - Data highlight
```

### Trend Indicators
```
↑   Trending Up         - Increasing value
↓   Trending Down       - Decreasing value
→   Stable/Trending     - Unchanged/sideways
↗   Sharp Increase      - Rapid rise
↘   Sharp Decrease      - Rapid fall
```

---

## 🎯 Color-Coding System

### Metric Status Colors

#### CPU Usage
- Color: **#3B82F6** (Chart Blue)
- Icon: 🔧
- Positive Indicator: Lower is better

#### Memory Usage
- Color: **#06B6D4** (Cyan)
- Icon: 💾
- Positive Indicator: Lower is better

#### Disk Usage
- Color: **#4F46E5** (Indigo)
- Icon: 💿
- Positive Indicator: Lower is better

#### GPU Usage
- Color: **#EC4899** (Pink)
- Icon: 🎮
- Positive Indicator: Lower is better

#### System Health
- Color: Adaptive (Green/Amber/Red)
- Icon: 📊
- Positive Indicator: Higher is better (scale 0-100)

---

## 📐 Visual Component Specifications

### Stat Card
```
Dimensions:       Variable (responsive grid)
Background:       #1A1F35 (card_bg)
Corner Radius:    12px (lg)
Padding:          16px (lg)
Border:           None (flat design)
Shadow:           Subtle elevation

Layout:
┌─────────────────────────┐
│ Icon(20px) Title        │
│                         │
│ Value(24px bold)        │
│ Trend(11px)             │
└─────────────────────────┘
```

### Health Bar
```
Height:           8px
Background:       #1E293B (border_medium)
Progress Color:   Dynamic (status-based)
Corner Radius:    4px (sm)
Label Size:       14px (base)
Percentage Size:  14px bold
Spacing:          8px (sm) between rows
```

### Detail Panel
```
Background:       #1A1F35 (card_bg)
Corner Radius:    12px (lg)
Title Size:       14px bold (#06B6D4 cyan)
Row Label:        12px secondary
Row Value:        12px bold primary
Padding:          16px (lg)
Row Spacing:      8px (sm)
```

### Chart Container
```
Background:       #1A1F35 (card_bg)
Corner Radius:    12px (lg)
Title Size:       14px bold
Padding:          16px (lg)
Height:           300-400px (typical)
DPI:              100
Font:             Segoe UI
```

### Navigation Item (Sidebar)
```
Width:            280px (fixed)
Height:           Auto
Spacing:          8px (sm) vertical
Background:       #1A1F35 (card_bg) default
Background Hover: #2D3748 (hover_bg)
Background Active:#1E40AF (primary_accent)
Corner Radius:    8px (md)
Icon Size:        18px
Icon Color:       #06B6D4 (cyan)
Text Size:        14px (base)
Padding:          8px (sm) horizontal
```

---

## 🎪 Component Layouts

### Stat Card Grid
```
Layout:           4 columns on desktop
Responsive:       2-3 columns on tablet
Mobile:           1 column
Gap:              16px (lg)
Total Width:      Expandable

Desktop:
┌─────────┬─────────┬─────────┬─────────┐
│  CPU    │ Memory  │  Disk   │  GPU    │
└─────────┴─────────┴─────────┴─────────┘

Tablet:
┌─────────┬─────────┬─────────┐
│  CPU    │ Memory  │  Disk   │
├─────────┼─────────┼─────────┤
│  GPU    │         │         │
└─────────┴─────────┴─────────┘

Mobile:
┌─────────┐
│  CPU    │
├─────────┤
│ Memory  │
├─────────┤
│  Disk   │
├─────────┤
│  GPU    │
└─────────┘
```

### Health Bar Group
```
Layout:           Vertical stack
Spacing:          8px (sm) between each
Width:            Full available
Padding:          16px (lg)

Visual:
┌────────────────────────────┐
│ CPU Temperature    65%     │
│ ████████░░░░░░░░░░░░      │
│                            │
│ Memory Health      82%     │
│ ██████████░░░░░░░░░░      │
│                            │
│ Disk Health        55%     │
│ ███████░░░░░░░░░░░░░░     │
│                            │
│ System Overall     72%     │
│ ███████████░░░░░░░░░░     │
└────────────────────────────┘
```

### Chart Layout
```
Title:            14px bold at top
Chart Area:       Main content (60% height)
Legend:           Bottom or side (15% height)
Axes:             Auto-scaled, labeled
Grid:             Light lines (0.1 alpha)
Margins:          16px (lg) padding

Example:
┌──────────────────────────┐
│ Chart Title              │
├──────────────────────────┤
│                          │
│    Chart Content Area    │
│    (Graph/Bars/etc)      │
│                          │
├──────────────────────────┤
│ ■ Legend Label           │
│ ■ Legend Label           │
└──────────────────────────┘
```

---

## 🎨 Typography Specifications

### Font: Segoe UI

#### Size 32px (XXL)
```
Weight:    Bold (700)
Color:     #F1F5F9 (primary text)
Usage:     Main page titles
Line Height: 1.2
Example:   "System Overview"
```

#### Size 28px (XL)
```
Weight:    Bold (700)
Color:     #F1F5F9
Usage:     Section headers
Line Height: 1.3
Example:   "Hardware Information"
```

#### Size 24px (LG)
```
Weight:    Medium (500) / Bold (700)
Color:     #F1F5F9
Usage:     Large headers, emphasis
Line Height: 1.4
Example:   Metric value display
```

#### Size 16px (MD)
```
Weight:    Medium (500)
Color:     #F1F5F9 / #CBD5E1
Usage:     Subheadings
Line Height: 1.5
Example:   Component titles
```

#### Size 14px (Base)
```
Weight:    Normal (400) / Medium (500)
Color:     #F1F5F9 / #CBD5E1
Usage:     Body text, default
Line Height: 1.5
Example:   Regular labels
```

#### Size 12px (SM)
```
Weight:    Normal (400) / Medium (500)
Color:     #CBD5E1 / #94A3B8
Usage:     Secondary text, labels
Line Height: 1.5
Example:   Helper text
```

#### Size 11px (XS)
```
Weight:    Normal (400)
Color:     #94A3B8 / #475569
Usage:     Tertiary text, small labels
Line Height: 1.4
Example:   Timestamps, units
```

---

## 🎯 Spacing Applications

### Component Padding
```
Card:              16px (lg) on all sides
Button:            12px vertical (md), 16px horizontal (lg)
Input:             12px vertical (md), 12px horizontal (md)
Section:           16px (lg) top and bottom
Header:            16px (lg) padding
```

### Element Spacing
```
Between labels:    8px (sm)
Between sections:  24px (xl)
Between rows:      8px (sm)
Between cards:     16px (lg)
Between icons/text: 8px (sm)
```

### Page Margins
```
Left/Right:        32px (xxl)
Top/Bottom:        24px (xl)
Content Area:      48px (xxxl) total horizontal
```

---

## 🖼️ Visual Hierarchy

### Primary Level
- Size: 32px or 28px (XXL/XL)
- Weight: Bold (700)
- Color: #F1F5F9 (primary)
- Spacing: Large (xl, xxl)
- Usage: Main titles, critical metrics

### Secondary Level
- Size: 16px or 24px (MD/LG)
- Weight: Medium/Bold (500/700)
- Color: #F1F5F9 (primary)
- Spacing: Medium (lg)
- Usage: Section headers, important data

### Tertiary Level
- Size: 14px (Base)
- Weight: Normal/Medium (400/500)
- Color: #CBD5E1 (secondary)
- Spacing: Standard (md)
- Usage: Supporting text, descriptions

### Quaternary Level
- Size: 12px or 11px (SM/XS)
- Weight: Normal (400)
- Color: #94A3B8 (tertiary)
- Spacing: Tight (sm)
- Usage: Labels, metadata, helpers

---

## 🎬 Animation Timings

### Hover Transitions
```
Duration:          200ms
Easing:            ease-in-out
Color Change:      Background #1A1F35 → #2D3748
Opacity:           1.0 → 0.95
Trigger:           Mouse enter
```

### Focus States
```
Duration:          Immediate
Style:             Blue border or highlight
Color:             #1E40AF (primary_accent)
Width:             2-3px border
Trigger:           Click or Tab key
```

### Value Changes
```
Duration:          500ms
Easing:            ease-out
Animation:         Smooth number transition
Color Flash:       Optional highlight
Trigger:           Metric update
```

---

## ✨ Visual Effects

### Shadows
```
None:              0 0 0 0 rgba(0,0,0,0)
Small:             0 1px 2px 0 rgba(0,0,0,0.05)
Medium:            0 4px 6px -1px rgba(0,0,0,0.1)
Large:             0 10px 15px -3px rgba(0,0,0,0.1)
Elevated:          0 25px 50px -12px rgba(0,0,0,0.25)

Usage:
- Small: Subtle depth for cards
- Medium: Regular component elevation
- Large: Important component emphasis
- Elevated: Modal or overlay shadow
```

### Gradients
```
Default Gradient:  #0F172A → #1E40AF (dark to accent blue)
Reverse Gradient:  #1E40AF → #0F172A (accent to dark)
Usage:             Backgrounds, chart styling
Opacity:           40-60% for subtle effects
```

### Border Effects
```
Light Border:      #334155 (border_light)
Medium Border:     #1E293B (border_medium)
Radius Levels:
- Square:          0px
- Subtle:          4px (sm)
- Standard:        8px (md)
- Rounded:         12px (lg)
- Heavy:           16px (xl)
```

---

## 📊 Chart Styling Guide

### Line Chart
```
Line Width:        2.5px
Marker Size:       5px
Colors:            Palette rotation (blue → cyan → indigo → purple)
Alpha:             0.9
Background:        #0F172A (primary_dark)
Grid:              Light with 0.1 opacity
Legend:            Upper left, dark background
```

### Bar Chart
```
Bar Width:         Auto-distributed
Bar Color:         Single or palette rotation
Alpha:             0.8
Value Labels:      On top of each bar
Background:        #0F172A
Grid:              Horizontal only, light
Edge Color:        #334155 (border_light)
```

### Pie Chart
```
Slice Colors:      Palette rotation
Percentage Label:  White, bold
Label Position:    On pie slice
Explode:           None (flat)
Start Angle:       90 degrees
Legend:            Positioned outside
```

### Gauge Chart
```
Background Arc:    #334155 (border_light)
Value Arc:         Status color (green/amber/red)
Arc Width:         3-4px
Center Value:      24px, bold, white
Label:             12px, secondary text
Angle Range:       180 degrees (left to right)
```

---

## 🎓 Design Token Summary

### Color Tokens (16 colors)
```
Primary:      dark, bg, accent
Accents:      cyan, teal, indigo
Status:       success, warning, danger, info
Text:         primary, secondary, tertiary, disabled
Borders:      light, medium
Component:    card_bg, input_bg, hover_bg, input_bg
Chart:        blue, cyan, teal, indigo, purple, pink
```

### Type Tokens (7 sizes + 5 weights)
```
Sizes:    xxl(32), xl(28), lg(24), md(16), base(14), sm(12), xs(11)
Weights:  light(300), normal(400), medium(500), semi(600), bold(700)
Family:   Segoe UI
Line:     1.4-1.5 for optimal readability
```

### Space Tokens (7 values)
```
xs(4), sm(8), md(12), lg(16), xl(24), xxl(32), xxxl(48)
Grid-based: All divisible by 4
```

### Radius Tokens (6 values)
```
none(0), sm(4), md(8), lg(12), xl(16), full(9999)
```

---

## 🔍 Design Quality Checklist

### Visual Consistency
- [ ] All colors from palette
- [ ] Typography follows scale
- [ ] Spacing uses grid values
- [ ] Border radius consistent
- [ ] Icons are appropriate

### Accessibility
- [ ] Text contrast ≥ 4.5:1
- [ ] Icons have labels
- [ ] Focus states visible
- [ ] Hover states clear
- [ ] Touch targets ≥ 48px

### Performance
- [ ] No unnecessary shadows
- [ ] Efficient animations
- [ ] Optimized images
- [ ] DPI appropriate
- [ ] Rendering smooth

### Professional Quality
- [ ] Polished appearance
- [ ] Consistent styling
- [ ] No visual clutter
- [ ] Clear hierarchy
- [ ] Enterprise-grade

---

**SysOptima Visual Assets v1.0**
*Professional, Consistent, Accessible* ✨
