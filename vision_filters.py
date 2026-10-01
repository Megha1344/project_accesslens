"""
Vision Impairment & Color Blindness Simulation Filters
Generates SVG filter definitions and CSS filter classes for Protanopia, Deuteranopia,
Tritanopia, Low Vision Acuity, Cataracts, Glaucoma, and Macular Degeneration.
"""
from typing import Dict, Any

# Standard Viénot / Brettel / Machado color transformation matrices
COLORBLIND_MATRICES = {
    "protanopia": [
        0.56667, 0.43333, 0.00000, 0, 0,
        0.55833, 0.44167, 0.00000, 0, 0,
        0.00000, 0.24167, 0.75833, 0, 0,
        0,       0,       0,       1, 0
    ],
    "deuteranopia": [
        0.62500, 0.37500, 0.00000, 0, 0,
        0.70000, 0.30000, 0.00000, 0, 0,
        0.00000, 0.30000, 0.70000, 0, 0,
        0,       0,       0,       1, 0
    ],
    "tritanopia": [
        0.95000, 0.05000, 0.00000, 0, 0,
        0.00000, 0.43333, 0.56667, 0, 0,
        0.00000, 0.47500, 0.52500, 0, 0,
        0,       0,       0,       1, 0
    ],
    "achromatopsia": [
        0.29900, 0.58700, 0.11400, 0, 0,
        0.29900, 0.58700, 0.11400, 0, 0,
        0.29900, 0.58700, 0.11400, 0, 0,
        0,       0,       0,       1, 0
    ]
}

def get_svg_filters_html() -> str:
    """Returns an inline SVG block containing colorblindness filter definitions."""
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">', '<defs>']
    
    for name, matrix in COLORBLIND_MATRICES.items():
        matrix_str = " ".join(str(m) for m in matrix)
        svg.append(f'  <filter id="filter-{name}">')
        svg.append(f'    <feColorMatrix type="matrix" values="{matrix_str}"/>')
        svg.append('  </filter>')
        
    # Cataract filter (Blur + brightness/contrast shift to simulate cloudy lens glare)
    svg.append('  <filter id="filter-cataract">')
    svg.append('    <feGaussianBlur stdDeviation="2.5" />')
    svg.append('    <feComponentTransfer>')
    svg.append('      <feFuncR type="linear" slope="0.85" intercept="0.15" />')
    svg.append('      <feFuncG type="linear" slope="0.85" intercept="0.15" />')
    svg.append('      <feFuncB type="linear" slope="0.80" intercept="0.15" />')
    svg.append('    </feComponentTransfer>')
    svg.append('  </filter>')
    
    svg.append('</defs>')
    svg.append('</svg>')
    return '\n'.join(svg)

def get_css_for_mode(mode: str) -> str:
    """Returns CSS rule string to apply chosen vision impairment simulation to container."""
    mode = mode.lower().strip()
    
    if mode in COLORBLIND_MATRICES:
        return f"filter: url(#filter-{mode}); -webkit-filter: url(#filter-{mode});"
    elif mode == "cataract":
        return "filter: url(#filter-cataract) contrast(85%) brightness(115%); -webkit-filter: url(#filter-cataract) contrast(85%) brightness(115%);"
    elif mode == "low_acuity":
        return "filter: blur(3.5px) contrast(90%); -webkit-filter: blur(3.5px) contrast(90%);"
    elif mode == "glaucoma":
        return "filter: contrast(95%); mask-image: radial-gradient(circle at center, transparent 20%, black 80%); -webkit-mask-image: radial-gradient(circle at center, transparent 20%, black 80%);"
    elif mode == "macular_degeneration":
        return "filter: contrast(95%); mask-image: radial-gradient(circle at center, black 0%, black 15%, transparent 35%, transparent 100%); -webkit-mask-image: radial-gradient(circle at center, black 0%, black 15%, transparent 35%, transparent 100%);"
    else:
        return "filter: none; -webkit-filter: none;"

def get_impairment_descriptions() -> Dict[str, Dict[str, str]]:
    """Returns metadata and human explanations for each vision mode."""
    return {
        "normal": {
            "name": "Normal Vision",
            "tagline": "Full color spectrum & 20/20 visual acuity",
            "details": "Standard baseline visual experience without color deficiency or clarity loss."
        },
        "protanopia": {
            "name": "Protanopia",
            "tagline": "Red-blindness (~1% of males)",
            "details": "Complete absence of red retinal photoreceptors. Red appears dark gray or dark brown, and red-green distinctions are lost."
        },
        "deuteranopia": {
            "name": "Deuteranopia",
            "tagline": "Green-blindness (~5% of males)",
            "details": "Complete absence of green retinal photoreceptors. Green tones appear beige/yellowish, and red-green distinctions are lost."
        },
        "tritanopia": {
            "name": "Tritanopia",
            "tagline": "Blue-blindness (~0.01% population)",
            "details": "Absence of blue photoreceptors. Blue appears greenish or dark grey, yellow appears pink or light grey."
        },
        "achromatopsia": {
            "name": "Achromatopsia",
            "tagline": "Complete Monochromacy / Color Blindness",
            "details": "Total lack of color vision. The world is perceived strictly in shades of gray, white, and black."
        },
        "low_acuity": {
            "name": "Low Visual Acuity",
            "tagline": "Uncorrected refractive blur (~20/100 to 20/200)",
            "details": "Simulates significant uncorrected vision blur, making fine text fonts, thin icons, and tight line-spacing unreadable."
        },
        "cataract": {
            "name": "Cataracts",
            "tagline": "Clouding of natural crystalline lens",
            "details": "Causes milky/cloudy vision, loss of contrast, washed-out color saturation, and severe glare sensitivity."
        },
        "glaucoma": {
            "name": "Glaucoma",
            "tagline": "Optic nerve damage & Peripheral Vision Loss",
            "details": "Creates progressive 'tunnel vision' where peripheral sight is lost while central vision remains partially intact."
        }
    }
