"""
SysOptima Theme System
Professional, calm, enterprise-grade color scheme and styling
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ColorPalette:
    """Modern, professional color palette inspired by enterprise design"""
    
    # Primary Colors - Deep, professional blues and teals
    primary_dark: str = "#0F172A"           # Almost black-blue - main background
    primary_bg: str = "#1A1F35"             # Dark blue-gray - secondary background
    primary_accent: str = "#1E40AF"         # Professional blue - CTAs and highlights
    
    # Secondary Colors - Calm, trustworthy
    accent_cyan: str = "#06B6D4"            # Cyan accent - data highlights
    accent_teal: str = "#0891B2"            # Teal - secondary highlights
    accent_indigo: str = "#4F46E5"          # Indigo - tertiary accent
    
    # Status Colors - Semantic meaning
    success: str = "#10B981"                # Emerald - healthy systems
    warning: str = "#F59E0B"                # Amber - warning state
    danger: str = "#EF4444"                 # Red - critical/error
    info: str = "#3B82F6"                   # Blue - informational
    
    # Gradient Colors
    gradient_start: str = "#0F172A"         # Dark for gradients
    gradient_end: str = "#1E40AF"           # Blue for gradients
    
    # Text Colors
    text_primary: str = "#F1F5F9"           # Bright white - main text
    text_secondary: str = "#CBD5E1"         # Light gray - secondary text
    text_tertiary: str = "#94A3B8"          # Medium gray - tertiary text
    text_disabled: str = "#475569"          # Darker gray - disabled text
    
    # Border and Divider
    border_light: str = "#334155"           # Light borders
    border_medium: str = "#1E293B"          # Medium borders
    
    # Component Backgrounds
    card_bg: str = "#1A1F35"                # Card backgrounds
    input_bg: str = "#0F172A"               # Input field backgrounds
    hover_bg: str = "#2D3748"               # Hover state
    
    # Chart Colors - Professional data visualization
    chart_blue: str = "#3B82F6"
    chart_cyan: str = "#06B6D4"
    chart_teal: str = "#0891B2"
    chart_indigo: str = "#4F46E5"
    chart_purple: str = "#A855F7"
    chart_pink: str = "#EC4899"
    chart_orange: str = "#F97316"     # Orange - GPU/performance charts
    
    def to_dict(self) -> Dict[str, str]:
        """Convert palette to dictionary"""
        return {
            'primary_dark': self.primary_dark,
            'primary_bg': self.primary_bg,
            'primary_accent': self.primary_accent,
            'accent_cyan': self.accent_cyan,
            'accent_teal': self.accent_teal,
            'accent_indigo': self.accent_indigo,
            'success': self.success,
            'warning': self.warning,
            'danger': self.danger,
            'info': self.info,
            'text_primary': self.text_primary,
            'text_secondary': self.text_secondary,
            'text_tertiary': self.text_tertiary,
            'text_disabled': self.text_disabled,
            'border_light': self.border_light,
            'border_medium': self.border_medium,
            'card_bg': self.card_bg,
            'input_bg': self.input_bg,
            'hover_bg': self.hover_bg,
        }


@dataclass
class Typography:
    """Professional typography settings"""
    
    # Font families
    font_primary: str = "Segoe UI"
    font_mono: str = "Consolas"
    
    # Font sizes (in pixels)
    size_xxl: int = 32
    size_xl: int = 28
    size_lg: int = 24
    size_md: int = 16
    size_base: int = 14
    size_sm: int = 12
    size_xs: int = 11
    
    # Font weights
    weight_light: int = 300
    weight_normal: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700


@dataclass
class Spacing:
    """Consistent spacing system"""
    
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32
    xxxl: int = 48


@dataclass
class BorderRadius:
    """Consistent border radius"""
    
    none: int = 0
    sm: int = 4
    md: int = 8
    lg: int = 12
    xl: int = 16
    full: int = 9999


@dataclass
class Shadows:
    """Shadow system for depth and elevation"""
    
    none: str = "0 0 0 0 rgba(0, 0, 0, 0)"
    sm: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
    xl: str = "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
    elevated: str = "0 25px 50px -12px rgba(0, 0, 0, 0.25)"


class SysOptimaTheme:
    """Complete theme system for SysOptima"""
    
    def __init__(self):
        self.colors = ColorPalette()
        self.typography = Typography()
        self.spacing = Spacing()
        self.border_radius = BorderRadius()
        self.shadows = Shadows()
    
    def get_status_color(self, percentage: float) -> str:
        """Get color based on health percentage (0-100)"""
        if percentage >= 80:
            return self.colors.success
        elif percentage >= 60:
            return self.colors.info
        elif percentage >= 40:
            return self.colors.warning
        else:
            return self.colors.danger
    
    def get_gradient(self, reverse: bool = False) -> Tuple[str, str]:
        """Get gradient colors for charts and backgrounds"""
        if reverse:
            return (self.colors.gradient_end, self.colors.gradient_start)
        return (self.colors.gradient_start, self.colors.gradient_end)


# Global theme instance
theme = SysOptimaTheme()
