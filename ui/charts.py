"""
Charts Module
Handles Matplotlib integration for Tkinter
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections

class RealTimeChart(ttk.Frame):
    """A real-time line chart component"""
    
    def __init__(self, parent, title, color="cyan", y_limit=100, buffer_size=60):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.y_limit = y_limit
        self.buffer_size = buffer_size
        
        # Data buffer (deque is efficient for sliding windows)
        self.data = collections.deque([0] * buffer_size, maxlen=buffer_size)
        
        self.setup_chart()
        
    def setup_chart(self):
        """Initialize the Matplotlib figure and canvas"""
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('#f0f0f0') # Match default GUI bg
        
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#ffffff')
        self.ax.set_title(self.title, fontsize=10)
        self.ax.set_ylim(0, self.y_limit)
        
        # Remove clutter
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.get_xaxis().set_visible(False) # Hide time axis for simplicity
        
        # Initial Plot
        self.line, = self.ax.plot(self.data, color=self.color, linewidth=1.5)
        
        # Embed in Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_chart(self, new_value):
        """Update the chart with a new value"""
        self.data.append(new_value)
        self.line.set_ydata(self.data)
        self.canvas.draw()
