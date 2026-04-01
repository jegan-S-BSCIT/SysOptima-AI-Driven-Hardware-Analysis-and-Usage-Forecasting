"""
Advanced Visualization Components for SysOptima
Professional charts, graphs, and data visualizations
"""

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from typing import List, Tuple
from ui.theme import theme


class LineChart(CTkFrame):
    """Professional line chart component"""
    
    def __init__(self, parent, title: str, data_series: dict, x_labels: List[str] = None, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create matplotlib figure
        fig = Figure(figsize=(10, 4), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Styling
        ax.set_facecolor(theme.colors.primary_dark)
        ax.grid(True, alpha=0.1, color=theme.colors.border_light)
        ax.spines['bottom'].set_color(theme.colors.border_light)
        ax.spines['left'].set_color(theme.colors.border_light)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Plot data
        colors = [
            theme.colors.chart_blue,
            theme.colors.chart_cyan,
            theme.colors.chart_indigo,
            theme.colors.chart_purple,
        ]
        
        for idx, (label, values) in enumerate(data_series.items()):
            ax.plot(values, label=label, color=colors[idx % len(colors)], 
                   linewidth=2.5, marker='o', markersize=5, alpha=0.9)
        
        # Labels styling
        ax.set_xlabel("Time →", color=theme.colors.text_tertiary, fontsize=10)
        ax.set_ylabel("Value →", color=theme.colors.text_tertiary, fontsize=10)
        ax.tick_params(colors=theme.colors.text_tertiary, labelsize=9)
        ax.legend(loc='upper left', facecolor=theme.colors.primary_dark, 
                 edgecolor=theme.colors.border_light, labelcolor=theme.colors.text_primary)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)


class AreaChart(CTkFrame):
    """Professional area chart component"""
    
    def __init__(self, parent, title: str, data_series: dict, stacked: bool = False, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create figure
        fig = Figure(figsize=(10, 4), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Styling
        ax.set_facecolor(theme.colors.primary_dark)
        ax.grid(True, alpha=0.1, color=theme.colors.border_light)
        ax.spines['bottom'].set_color(theme.colors.border_light)
        ax.spines['left'].set_color(theme.colors.border_light)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Plot area data
        colors = [
            theme.colors.chart_blue,
            theme.colors.chart_cyan,
            theme.colors.chart_indigo,
            theme.colors.chart_purple,
        ]
        
        for idx, (label, values) in enumerate(data_series.items()):
            ax.fill_between(range(len(values)), values, alpha=0.6, 
                            color=colors[idx % len(colors)], label=label)
        
        # Labels
        ax.set_xlabel("Time →", color=theme.colors.text_tertiary, fontsize=10)
        ax.set_ylabel("Value →", color=theme.colors.text_tertiary, fontsize=10)
        ax.tick_params(colors=theme.colors.text_tertiary, labelsize=9)
        ax.legend(loc='upper left', facecolor=theme.colors.primary_dark,
                 edgecolor=theme.colors.border_light, labelcolor=theme.colors.text_primary)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)


class BarChart(CTkFrame):
    """Professional bar chart component"""
    
    def __init__(self, parent, title: str, categories: List[str], values: List[float], 
                 color: str = None, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create figure
        fig = Figure(figsize=(10, 4), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Styling
        ax.set_facecolor(theme.colors.primary_dark)
        ax.grid(True, alpha=0.1, color=theme.colors.border_light, axis='y')
        ax.spines['bottom'].set_color(theme.colors.border_light)
        ax.spines['left'].set_color(theme.colors.border_light)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Plot bars
        bar_color = color or theme.colors.chart_blue
        bars = ax.bar(categories, values, color=bar_color, alpha=0.8, edgecolor=theme.colors.border_light)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', color=theme.colors.text_primary, fontsize=9)
        
        # Labels
        ax.set_ylabel("Value →", color=theme.colors.text_tertiary, fontsize=10)
        ax.tick_params(colors=theme.colors.text_tertiary, labelsize=9)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)


class PieChart(CTkFrame):
    """Professional pie chart component"""
    
    def __init__(self, parent, title: str, labels: List[str], sizes: List[float], **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create figure
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Colors
        colors = [
            theme.colors.chart_blue,
            theme.colors.chart_cyan,
            theme.colors.chart_indigo,
            theme.colors.chart_purple,
            theme.colors.chart_pink,
        ]
        
        # Plot pie
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)],
                                           autopct='%1.1f%%', startangle=90)
        
        # Style
        for text in texts:
            text.set_color(theme.colors.text_primary)
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color(theme.colors.text_primary)
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax.set_facecolor(theme.colors.primary_dark)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)


class HeatmapChart(CTkFrame):
    """Professional heatmap component"""
    
    def __init__(self, parent, title: str, data: np.ndarray, x_labels: List[str], 
                 y_labels: List[str], **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create figure
        fig = Figure(figsize=(10, 6), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Plot heatmap
        im = ax.imshow(data, cmap='cool', aspect='auto')
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_yticks(np.arange(len(y_labels)))
        ax.set_xticklabels(x_labels, color=theme.colors.text_tertiary)
        ax.set_yticklabels(y_labels, color=theme.colors.text_tertiary)
        
        # Styling
        ax.set_facecolor(theme.colors.primary_dark)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.tick_params(colors=theme.colors.text_tertiary, labelsize=9)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)


class MetricGauge(CTkFrame):
    """Circular gauge for metric display"""
    
    def __init__(self, parent, label: str, value: float, max_value: float = 100, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Create figure
        fig = Figure(figsize=(4, 4), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Draw gauge
        theta = np.linspace(np.pi, 0, 100)
        r = 1
        
        # Background arc
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=theme.colors.border_light, linewidth=3)
        
        # Value arc
        value_ratio = min(value / max_value, 1.0)
        value_theta = np.linspace(np.pi, np.pi - np.pi * value_ratio, 50)
        ax.plot(r * np.cos(value_theta), r * np.sin(value_theta), 
               color=theme.get_status_color(value_ratio * 100), linewidth=4)
        
        # Center text
        ax.text(0, -0.2, f'{value:.1f}%', ha='center', va='center',
               fontsize=24, fontweight='bold', color=theme.colors.text_primary)
        ax.text(0, -0.5, label, ha='center', va='center',
               fontsize=12, color=theme.colors.text_secondary)
        
        # Clean up axes
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        ax.set_facecolor(theme.colors.card_bg)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)


class ComparisonChart(CTkFrame):
    """Comparison chart with multiple metrics"""
    
    def __init__(self, parent, title: str, metrics: dict, **kwargs):
        super().__init__(parent, fg_color=theme.colors.card_bg, corner_radius=theme.border_radius.lg, **kwargs)
        
        # Title
        title_label = CTkLabel(
            self,
            text=title,
            font=(theme.typography.font_primary, theme.typography.size_base, "bold"),
            text_color=theme.colors.text_primary
        )
        title_label.pack(padx=theme.spacing.lg, pady=(theme.spacing.lg, 0))
        
        # Create figure
        fig = Figure(figsize=(10, 5), dpi=100, facecolor=theme.colors.card_bg)
        ax = fig.add_subplot(111)
        
        # Styling
        ax.set_facecolor(theme.colors.primary_dark)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(theme.colors.border_light)
        ax.spines['left'].set_color(theme.colors.border_light)
        
        # Plot grouped bars
        labels = list(metrics.keys())
        x = np.arange(len(labels))
        width = 0.25
        
        colors_list = [theme.colors.chart_blue, theme.colors.chart_cyan, theme.colors.chart_indigo]
        
        # Sample data for comparison
        data1 = [metrics[l].get('current', 0) for l in labels]
        data2 = [metrics[l].get('average', 0) for l in labels]
        data3 = [metrics[l].get('peak', 0) for l in labels]
        
        ax.bar(x - width, data1, width, label='Current', color=colors_list[0], alpha=0.8)
        ax.bar(x, data2, width, label='Average', color=colors_list[1], alpha=0.8)
        ax.bar(x + width, data3, width, label='Peak', color=colors_list[2], alpha=0.8)
        
        ax.set_ylabel('Value', color=theme.colors.text_tertiary)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, color=theme.colors.text_tertiary)
        ax.tick_params(colors=theme.colors.text_tertiary)
        ax.legend(facecolor=theme.colors.primary_dark, edgecolor=theme.colors.border_light,
                 labelcolor=theme.colors.text_primary)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=theme.spacing.md, pady=theme.spacing.md)
