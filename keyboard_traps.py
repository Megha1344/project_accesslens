"""
Keyboard Navigation Journey Engine & Focus Trap Auditor
Analyzes HTML tab sequences, identifies tabindex anti-patterns, missing focus rings,
and potential keyboard navigation traps.
"""
from typing import List, Dict, Any
from bs4 import BeautifulSoup

def analyze_keyboard_navigation(html_content: str) -> Dict[str, Any]:
    """
    Extracts ordered keyboard focus sequence and evaluates keyboard accessibility rules:
    - WCAG 2.1.1 (Keyboard access)
    - WCAG 2.1.2 (No Keyboard Trap)
    - WCAG 2.4.3 (Focus Order)
    - WCAG 2.4.7 (Focus Visible)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tab_sequence = []
    keyboard_warnings = []
    
    # Standard natively focusable HTML elements
    focusable_selector = 'a[href], button, input, select, textarea, [tabindex], [contenteditable="true"]'
    candidates = soup.find_all(['a', 'button', 'input', 'select', 'textarea', 'div', 'span', 'section'])
    
    sequence_id = 0
    positive_tabindex_count = 0
    
    for tag in candidates:
        # Check if focusable
        is_natively_focusable = tag.name in ['a', 'button', 'input', 'select', 'textarea'] and (tag.name != 'a' or tag.has_attr('href'))
        tabindex = tag.get('tabindex', None)
        
        if tabindex is not None:
            try:
                tabindex_val = int(tabindex)
            except ValueError:
                tabindex_val = 0
        else:
            tabindex_val = 0 if is_natively_focusable else None
            
        if tabindex_val is None:
            continue
            
        # Ignored from tab flow if tabindex="-1"
        if tabindex_val == -1:
            if is_natively_focusable:
                keyboard_warnings.append({
                    "id": "disabled_tabindex",
                    "wcag": "WCAG 2.1.1 (Keyboard)",
                    "severity": "Serious",
                    "element": f"<{tag.name}> ({tag.get_text(strip=True)[:20] or tag.get('name') or 'control'})",
                    "description": f"Focusable <{tag.name}> has tabindex=\"-1\". It cannot be reached via standard Tab key navigation."
                })
            continue
            
        if tabindex_val > 0:
            positive_tabindex_count += 1
            keyboard_warnings.append({
                "id": "positive_tabindex",
                "wcag": "WCAG 2.4.3 (Focus Order)",
                "severity": "Moderate",
                "element": f"<{tag.name}> (tabindex={tabindex_val})",
                "description": f"<{tag.name}> uses positive tabindex=\"{tabindex_val}\". This disrupts natural DOM tab order and creates confusing focus jumps."
            })
            
        sequence_id += 1
        
        # Determine focus indicator status
        style_str = tag.get('style', '').lower().replace(' ', '')
        has_outline_none = 'outline:none' in style_str or 'outline:0' in style_str
        
        element_label = tag.get_text(strip=True) or tag.get('aria-label') or tag.get('placeholder') or tag.get('name') or f"<{tag.name}>"
        
        tab_sequence.append({
            "step": sequence_id,
            "tag": tag.name,
            "label": element_label[:30],
            "tabindex": tabindex_val,
            "has_outline_none": has_outline_none,
            "html_snippet": str(tag)[:100],
            "focus_indicator_status": "Missing / Removed" if has_outline_none else "Standard / Visible"
        })

    # Keyboard Trap heuristic check (modal divs missing esc handlers or bad z-index overlays)
    modals = soup.find_all(attrs={"class": lambda c: c and ('modal' in c.lower() or 'popup' in c.lower() or 'dialog' in c.lower())})
    for modal in modals:
        if not modal.get('role') == 'dialog' or not modal.get('aria-modal'):
            keyboard_warnings.append({
                "id": "potential_trap",
                "wcag": "WCAG 2.1.2 (No Keyboard Trap)",
                "severity": "Critical",
                "element": f"<{modal.name} class=\"{modal.get('class')}\">",
                "description": "Modal dialog element detected without proper role=\"dialog\" or aria-modal=\"true\". Keyboard focus may become trapped inside or escape underneath the overlay."
            })

    return {
        "total_focusable_elements": len(tab_sequence),
        "positive_tabindex_count": positive_tabindex_count,
        "tab_sequence": tab_sequence,
        "warnings": keyboard_warnings
    }
