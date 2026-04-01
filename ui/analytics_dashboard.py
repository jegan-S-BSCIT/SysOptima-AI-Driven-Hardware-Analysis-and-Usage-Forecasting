"""
Advanced Analytics Dashboard for SysOptima
Comprehensive performance analysis and insights view
"""

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame
import numpy as np
from ui.theme import theme
from ui.visualizations import (
    LineChart, AreaChart, BarChart, PieChart, 
    HeatmapChart, MetricGauge, ComparisonChart
)


class AnalyticsDashboard(CTkFrame):
    """Comprehensive analytics dashboard"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_bg, **kwargs)
        
        # Main scroll frame
        scroll_frame = CTkScrollableFrame(
            self,
            fg_color=theme.colors.primary_bg,
            label_text="📊 Performance Analytics",
            label_font=(theme.typography.font_primary, theme.typography.size_lg, "bold"),
            label_text_color=theme.colors.text_primary
        )
        scroll_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Section 1: Real-time System Metrics
        section1 = self._create_section("Real-time System Metrics", scroll_frame)
        
        # CPU and Memory gauge grid
        metrics_grid = CTkFrame(section1, fg_color="transparent")
        metrics_grid.pack(fill="x", pady=theme.spacing.lg)
        
        MetricGauge(metrics_grid, "CPU Usage", 42, 100).pack(side="left", expand=True, padx=theme.spacing.md)
        MetricGauge(metrics_grid, "Memory Usage", 68, 100).pack(side="left", expand=True, padx=theme.spacing.md)
        MetricGauge(metrics_grid, "Disk Usage", 56, 100).pack(side="left", expand=True, padx=theme.spacing.md)
        MetricGauge(metrics_grid, "GPU Usage", 28, 100).pack(side="left", expand=True, padx=theme.spacing.md)
        
        # Section 2: Historical Trends
        section2 = self._create_section("Historical Trends - Last 24 Hours", scroll_frame)
        
        # CPU and Memory trend
        trend_data = {
            'CPU Usage': np.sin(np.linspace(0, 2*np.pi, 24)) * 20 + 40,
            'Memory Usage': np.sin(np.linspace(0, 2*np.pi, 24) + 1) * 15 + 65,
        }
        LineChart(section2, "System Resources Over Time", trend_data, height=300).pack(fill="both", expand=True)
        
        # Section 3: Performance Comparison
        section3 = self._create_section("Performance Comparison", scroll_frame)
        
        comparison_metrics = {
            'CPU': {'current': 42, 'average': 38, 'peak': 78},
            'Memory': {'current': 68, 'average': 62, 'peak': 82},
            'Disk': {'current': 56, 'average': 45, 'peak': 71},
        }
        ComparisonChart(section3, "Current vs Average vs Peak", comparison_metrics, height=300).pack(fill="both", expand=True)
        
        # Section 4: Storage Distribution
        section4 = self._create_section("Storage Distribution", scroll_frame)
        
        pie_data = ['System Files', 'Applications', 'User Data', 'Media', 'Other']
        pie_sizes = [150, 250, 300, 200, 100]
        PieChart(section4, "Disk Space Breakdown", pie_data, pie_sizes, height=300).pack(fill="both", expand=True)
        
        # Section 5: Disk I/O Activity
        section5 = self._create_section("Disk I/O Activity - Last 12 Hours", scroll_frame)
        
        io_data = {
            'Read Speed': np.random.randint(100, 500, 12),
            'Write Speed': np.random.randint(50, 300, 12),
        }
        AreaChart(section5, "Disk I/O Performance", io_data, height=300).pack(fill="both", expand=True)
        
        # Section 6: Process CPU Usage
        section6 = self._create_section("Top CPU-Intensive Processes", scroll_frame)
        
        processes = ['Chrome', 'VS Code', 'Windows Explorer', 'Discord', 'Steam']
        cpu_usage = [18, 12, 8, 5, 3]
        BarChart(section6, "CPU Usage by Process", processes, cpu_usage, 
                color=theme.colors.chart_blue, height=300).pack(fill="both", expand=True)
        
        # Section 7: System Temperature Heatmap
        section7 = self._create_section("Component Temperature Heatmap", scroll_frame)
        
        temp_data = np.array([
            [65, 62, 68, 61],
            [70, 72, 75, 71],
            [55, 58, 60, 57],
            [52, 54, 56, 53],
        ])
        HeatmapChart(section7, "Temperature by Component and Time", temp_data,
                    ['Time 1', 'Time 2', 'Time 3', 'Time 4'],
                    ['CPU', 'GPU', 'SSD', 'Chipset'], height=350).pack(fill="both", expand=True)
        
        # Section 8: Network Activity
        section8 = self._create_section("Network Activity", scroll_frame)
        
        net_data = {
            'Download': np.random.randint(1, 50, 20),
            'Upload': np.random.randint(0.5, 20, 20),
        }
        LineChart(section8, "Network Speed (Mbps)", net_data, height=300).pack(fill="both", expand=True)
    
    def _create_section(self, title: str, parent: CTkFrame) -> CTkFrame:
        """Create a collapsible section"""
        section_frame = CTkFrame(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg)
        section_frame.pack(fill="both", expand=False, pady=theme.spacing.lg)
        
        # Section header
        header = CTkFrame(section_frame, fg_color="transparent")
        header.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        header_label = CTkLabel(
            header,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        header_label.pack(anchor="w")
        
        return section_frame


class DiagnosticsView(CTkFrame):
    """AI-powered diagnostics view"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.colors.primary_bg, **kwargs)
        
        scroll_frame = CTkScrollableFrame(
            self,
            fg_color=theme.colors.primary_bg,
            label_text="🤖 AI-Powered System Diagnostics",
            label_font=(theme.typography.font_primary, theme.typography.size_lg, "bold"),
            label_text_color=theme.colors.text_primary
        )
        scroll_frame.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Overall Health Score
        health_section = self._create_section("System Health Analysis", scroll_frame)
        
        # Health gauge
        health_gauge = MetricGauge(health_section, "Overall Health", 85, 100)
        health_gauge.pack(fill="both", expand=True, padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        # Health insights
        insights_frame = CTkFrame(health_section, fg_color="transparent")
        insights_frame.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        self._add_insight(insights_frame, "✓", "CPU Performance", 
                         "Excellent - Operating at optimal frequency", theme.colors.success)
        self._add_insight(insights_frame, "⚠", "Disk Health", 
                         "Moderate - Consider defragmentation", theme.colors.warning)
        self._add_insight(insights_frame, "✓", "Memory Health", 
                         "Good - No memory leaks detected", theme.colors.success)
        
        # Issues and Recommendations
        issues_section = self._create_section("Issues & Recommendations", scroll_frame)
        
        # Critical issues
        critical_frame = self._create_subsection(issues_section, "🔴 Critical Issues", theme.colors.danger)
        self._add_issue_item(critical_frame, "High disk usage", 
                            "Clear temporary files and cache")
        
        # Warnings
        warning_frame = self._create_subsection(issues_section, "🟡 Warnings", theme.colors.warning)
        self._add_issue_item(warning_frame, "GPU drivers outdated", 
                            "Update to latest version for security")
        self._add_issue_item(warning_frame, "Background processes", 
                            "Consider disabling unused startup programs")
        
        # Info
        info_frame = self._create_subsection(issues_section, "ℹ️ Informational", theme.colors.info)
        self._add_issue_item(info_frame, "System uptime: 45 days", 
                            "Performance may improve with restart")
        self._add_issue_item(info_frame, "Battery health: 85%", 
                            "Battery degradation is normal")
        
        # Recommendations
        rec_section = self._create_section("Smart Recommendations", scroll_frame)
        
        recommendations = [
            ("Priority 1", "Clear cache files", "Estimated recovery: 2.3 GB"),
            ("Priority 2", "Update GPU drivers", "Improves performance by ~5-8%"),
            ("Priority 3", "Optimize startup", "Reduces boot time by ~20 seconds"),
        ]
        
        for priority, action, benefit in recommendations:
            self._add_recommendation(rec_section, priority, action, benefit)
    
    def _create_section(self, title: str, parent: CTkFrame) -> CTkFrame:
        """Create a section frame"""
        section_frame = CTkFrame(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg)
        section_frame.pack(fill="both", expand=False, pady=theme.spacing.lg)
        
        # Section header
        header = CTkFrame(section_frame, fg_color="transparent")
        header.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.lg)
        
        header_label = CTkLabel(
            header,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        header_label.pack(anchor="w")
        
        return section_frame
    
    def _create_subsection(self, parent: CTkFrame, title: str, color: str) -> CTkFrame:
        """Create a subsection"""
        sub_frame = CTkFrame(parent, fg_color=theme.colors.primary_dark, corner_radius=theme.border_radius.md)
        sub_frame.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.md)
        
        # Title with colored indicator
        title_frame = CTkFrame(sub_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=theme.spacing.md, pady=theme.spacing.md)
        
        title_label = CTkLabel(
            title_frame,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=color
        )
        title_label.pack(anchor="w")
        
        # Content frame
        content = CTkFrame(sub_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=theme.spacing.md, pady=(0, theme.spacing.md))
        
        return content
    
    def _add_insight(self, parent: CTkFrame, icon: str, title: str, description: str, color: str):
        """Add an insight item"""
        item_frame = CTkFrame(parent, fg_color=theme.colors.primary_dark, corner_radius=theme.border_radius.md)
        item_frame.pack(fill="x", pady=theme.spacing.sm)
        
        content = CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=theme.spacing.md, pady=theme.spacing.md)
        
        # Icon
        icon_label = CTkLabel(
            content,
            text=icon,
            font=(theme.typography.font_primary, 14),
            text_color=color,
            width=30
        )
        icon_label.pack(side="left", padx=(0, theme.spacing.md))
        
        # Text
        text_frame = CTkFrame(content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        title_label = CTkLabel(
            text_frame,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(anchor="w")
        
        desc_label = CTkLabel(
            text_frame,
            text=description,
            font=(theme.typography.font_primary, theme.typography.size_xs),
            text_color=theme.colors.text_tertiary
        )
        desc_label.pack(anchor="w", pady=(theme.spacing.xs, 0))
    
    def _add_issue_item(self, parent: CTkFrame, issue: str, action: str):
        """Add an issue item"""
        item_frame = CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=theme.spacing.sm)
        
        # Issue
        issue_label = CTkLabel(
            item_frame,
            text=f"• {issue}",
            font=(theme.typography.font_primary, theme.typography.size_sm),
            text_color=theme.colors.text_primary
        )
        issue_label.pack(anchor="w")
        
        # Action
        action_label = CTkLabel(
            item_frame,
            text=f"  → {action}",
            font=(theme.typography.font_primary, theme.typography.size_xs),
            text_color=theme.colors.text_tertiary
        )
        action_label.pack(anchor="w")
    
    def _add_recommendation(self, parent: CTkFrame, priority: str, action: str, benefit: str):
        """Add a recommendation item"""
        rec_frame = CTkFrame(parent, fg_color=theme.colors.primary_dark, corner_radius=theme.border_radius.md)
        rec_frame.pack(fill="x", padx=theme.spacing.lg, pady=theme.spacing.md)
        
        # Header
        header = CTkFrame(rec_frame, fg_color="transparent")
        header.pack(fill="x", padx=theme.spacing.md, pady=(theme.spacing.md, 0))
        
        priority_label = CTkLabel(
            header,
            text=priority,
            font=(theme.typography.font_primary, theme.typography.size_sm, "bold"),
            text_color=theme.colors.accent_cyan
        )
        priority_label.pack(anchor="w")
        
        # Action
        action_label = CTkLabel(
            rec_frame,
            text=action,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        action_label.pack(anchor="w", padx=theme.spacing.md, pady=theme.spacing.sm)
        
        # Benefit
        benefit_label = CTkLabel(
            rec_frame,
            text=benefit,
            font=(theme.typography.font_primary, theme.typography.size_xs),
            text_color=theme.colors.text_tertiary
        )
        benefit_label.pack(anchor="w", padx=theme.spacing.md, pady=(0, theme.spacing.md))
        
        # Action button
        button = CTkButton(
            rec_frame,
            text="Apply Now →",
            font=(theme.typography.font_primary, theme.typography.size_sm),
            fg_color=theme.colors.primary_accent,
            hover_color=theme.colors.accent_indigo,
            text_color=theme.colors.text_primary,
            height=32,
            corner_radius=theme.border_radius.md
        )
        button.pack(fill="x", padx=theme.spacing.md, pady=theme.spacing.md)
