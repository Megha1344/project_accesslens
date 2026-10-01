"""
WCAG 2.1 Color Contrast Engine & Auto-Fixer Algorithms
Implements W3C WCAG 2.1 specifications for Relative Luminance and Contrast Ratio.
"""
import math
import re
from typing import Tuple, Dict, Any, Optional

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Converts hex color string (#RGB, #RRGGBB) to (r, g, b) tuple 0-255."""
    hex_str = hex_str.strip().lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c * 2 for c in hex_str])
    if len(hex_str) != 6:
        # Default fallback if invalid hex
        return (0, 0, 0)
    try:
        return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
    except ValueError:
        return (0, 0, 0)

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Converts (r, g, b) tuple 0-255 to #RRGGBB hex string."""
    r = max(0, min(255, int(rgb[0])))
    g = max(0, min(255, int(rgb[1])))
    b = max(0, min(255, int(rgb[2])))
    return f"#{r:02x}{g:02x}{b:02x}"

def parse_color_to_rgb(color_str: str) -> Tuple[int, int, int]:
    """Parses hex, rgb(), rgba(), or color names to (r, g, b)."""
    if not color_str:
        return (0, 0, 0)
    color_str = color_str.strip().lower()
    
    # Hex format
    if color_str.startswith('#'):
        return hex_to_rgb(color_str)
    
    # rgb/rgba format
    rgb_match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
    if rgb_match:
        return (int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3)))
        
    # Common named colors fallback dictionary
    named_colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        'lightgray': (211, 211, 211),
        'darkgray': (169, 169, 169),
        'transparent': (255, 255, 255),  # Assume white bg for transparent
    }
    return named_colors.get(color_str, (0, 0, 0))

def srgb_channel_to_linear(c_255: float) -> float:
    """Converts 8-bit sRGB channel [0..255] to linear luminance component per WCAG 2.1."""
    c = c_255 / 255.0
    if c <= 0.04045:
        return c / 12.92
    else:
        return math.pow((c + 0.055) / 1.055, 2.4)

def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calculates WCAG 2.1 Relative Luminance (L).
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B (linear sRGB)
    """
    r_lin = srgb_channel_to_linear(rgb[0])
    g_lin = srgb_channel_to_linear(rgb[1])
    b_lin = srgb_channel_to_linear(rgb[2])
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def calculate_contrast_ratio(fg_color: str, bg_color: str) -> float:
    """
    Calculates the WCAG 2.1 contrast ratio between foreground and background.
    Ratio = (L1 + 0.05) / (L2 + 0.05) where L1 > L2.
    Returns float rounded to 2 decimal places (1.00 to 21.00).
    """
    fg_rgb = parse_color_to_rgb(fg_color)
    bg_rgb = parse_color_to_rgb(bg_color)
    
    l1 = calculate_relative_luminance(fg_rgb)
    l2 = calculate_relative_luminance(bg_rgb)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    ratio = (lighter + 0.05) / (darker + 0.05)
    return round(ratio, 2)

def evaluate_wcag_compliance(ratio: float, is_large_text: bool = False) -> Dict[str, Any]:
    """
    Evaluates contrast ratio against WCAG 2.1 Level AA and Level AAA thresholds.
    Standard text: AA >= 4.5:1, AAA >= 7.0:1
    Large text (>= 18pt or 14pt bold): AA >= 3.0:1, AAA >= 4.5:1
    UI Components / Graphics: AA >= 3.0:1
    """
    aa_target = 3.0 if is_large_text else 4.5
    aaa_target = 4.5 if is_large_text else 7.0
    
    passes_aa = ratio >= aa_target
    passes_aaa = ratio >= aaa_target
    
    if passes_aaa:
        status = "Pass AAA"
        badge_color = "#10B981"  # Emerald green
    elif passes_aa:
        status = "Pass AA"
        badge_color = "#3B82F6"  # Blue
    else:
        status = "Fail AA"
        badge_color = "#EF4444"  # Red
        
    return {
        "contrast_ratio": ratio,
        "is_large_text": is_large_text,
        "aa_target": aa_target,
        "aaa_target": aaa_target,
        "passes_aa": passes_aa,
        "passes_aaa": passes_aaa,
        "status": status,
        "badge_color": badge_color,
    }

def auto_fix_contrast(
    fg_color: str,
    bg_color: str,
    target_ratio: float = 4.5,
    fix_target: str = "fg"
) -> Dict[str, Any]:
    """
    Auto-suggests an adjusted color for foreground (or background) to meet target WCAG contrast ratio
    while preserving original hue & saturation as closely as possible.
    
    fix_target: 'fg' (adjust foreground) or 'bg' (adjust background).
    """
    original_ratio = calculate_contrast_ratio(fg_color, bg_color)
    if original_ratio >= target_ratio:
        return {
            "original_fg": fg_color,
            "original_bg": bg_color,
            "original_ratio": original_ratio,
            "fixed_fg": fg_color,
            "fixed_bg": bg_color,
            "fixed_ratio": original_ratio,
            "target_ratio": target_ratio,
            "changed": False,
            "suggestion_css": f"color: {fg_color}; background-color: {bg_color};"
        }

    fg_rgb = parse_color_to_rgb(fg_color)
    bg_rgb = parse_color_to_rgb(bg_color)
    
    l_bg = calculate_relative_luminance(bg_rgb)
    
    # Determine whether we should darken or lighten the target color
    bg_is_light = l_bg > 0.5
    
    fixed_fg_rgb = list(fg_rgb)
    fixed_bg_rgb = list(bg_rgb)
    
    best_rgb = fixed_fg_rgb if fix_target == "fg" else fixed_bg_rgb
    
    step = -2 if (fix_target == "fg" and bg_is_light) or (fix_target == "bg" and not bg_is_light) else 2
    
    current_ratio = original_ratio
    attempts = 0
    
    while current_ratio < target_ratio and attempts < 150:
        attempts += 1
        for i in range(3):
            best_rgb[i] = max(0, min(255, best_rgb[i] + step))
            
        test_fg = rgb_to_hex(tuple(fixed_fg_rgb))
        test_bg = rgb_to_hex(tuple(fixed_bg_rgb))
        current_ratio = calculate_contrast_ratio(test_fg, test_bg)
        
        if best_rgb == [0, 0, 0] or best_rgb == [255, 255, 255]:
            if bg_is_light:
                if fix_target == "fg": fixed_fg_rgb = [0, 0, 0]
                else: fixed_bg_rgb = [255, 255, 255]
            else:
                if fix_target == "fg": fixed_fg_rgb = [255, 255, 255]
                else: fixed_bg_rgb = [0, 0, 0]
            current_ratio = calculate_contrast_ratio(rgb_to_hex(tuple(fixed_fg_rgb)), rgb_to_hex(tuple(fixed_bg_rgb)))
            break

    fixed_fg_hex = rgb_to_hex(tuple(fixed_fg_rgb))
    fixed_bg_hex = rgb_to_hex(tuple(fixed_bg_rgb))
    final_ratio = calculate_contrast_ratio(fixed_fg_hex, fixed_bg_hex)
    
    return {
        "original_fg": fg_color,
        "original_bg": bg_color,
        "original_ratio": original_ratio,
        "fixed_fg": fixed_fg_hex,
        "fixed_bg": fixed_bg_hex,
        "fixed_ratio": final_ratio,
        "target_ratio": target_ratio,
        "changed": True,
        "suggestion_css": f"color: {fixed_fg_hex}; background-color: {fixed_bg_hex};"
    }
