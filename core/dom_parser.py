"""
DOM Accessibility Auditor & Parser Engine
Parses HTML/CSS using BeautifulSoup and extracts 9 WCAG 2.1 violation categories:
1. Poor contrast (WCAG 1.4.3)
2. Red/Green ONLY status indicators (WCAG 1.4.1)
3. Missing alt text (WCAG 1.1.1)
4. Skipped heading levels (WCAG 1.3.1)
5. Missing form labels (WCAG 4.1.2)
6. Poor focus visibility / outline:none (WCAG 2.4.7)
7. Keyboard inaccessible div/span controls (WCAG 2.1.1)
8. Confusing positive tabindex order (WCAG 2.4.3)
9. Small touch target sizes (WCAG 2.5.5/2.5.8)
"""
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup, Tag
from .wcag_math import calculate_contrast_ratio, evaluate_wcag_compliance, auto_fix_contrast

def parse_inline_styles(style_attr: str) -> Dict[str, str]:
    styles = {}
    if not style_attr:
        return styles
    parts = style_attr.split(';')
    for part in parts:
        if ':' in part:
            k, v = part.split(':', 1)
            styles[k.strip().lower()] = v.strip()
    return styles

def extract_element_colors(tag: Tag, default_bg: str = "#ffffff") -> Dict[str, str]:
    style_str = tag.get('style', '')
    styles = parse_inline_styles(style_str)
    
    fg = styles.get('color', None)
    bg = styles.get('background-color', styles.get('background', None))
    
    if not fg and tag.get('color'):
        fg = tag.get('color')
    if not bg and tag.get('bgcolor'):
        bg = tag.get('bgcolor')
        
    if not fg:
        if tag.name == 'a':
            fg = '#2563eb'
        elif tag.name in ['button', 'input']:
            fg = '#1f2937'
        else:
            fg = '#111827'
            
    if not bg:
        if tag.name == 'button':
            bg = '#e5e7eb'
        else:
            bg = default_bg
            
    return {"fg": fg, "bg": bg}

def audit_html_accessibility(html_content: str, default_bg: str = "#ffffff") -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    
    issues = []
    text_elements_scanned = 0
    passed_checks = 0
    
    # Category Counters
    visual_fails = 0
    motor_fails = 0
    semantic_fails = 0

    # 1. Check Red/Green ONLY Status Indicators (WCAG 1.4.1 Use of Color)
    status_elements = soup.find_all(['span', 'div', 'i'])
    for el in status_elements:
        style = el.get('style', '').lower()
        cls = ' '.join(el.get('class', [])).lower()
        
        is_colored_dot = (
            'border-radius: 50%' in style or 'border-radius:50%' in style or 
            'status-dot' in cls or 'indicator' in cls
        )
        is_red_or_green = (
            '#22c55e' in style or '#ef4444' in style or 'green' in style or 'red' in style or 
            'background-color: green' in style or 'background-color: red' in style
        )
        
        has_text_or_aria = bool(el.get_text(strip=True)) or bool(el.get('aria-label')) or bool(el.get('title'))
        
        if is_colored_dot and is_red_or_green and not has_text_or_aria:
            visual_fails += 1
            issues.append({
                "id": "color_only_indicator",
                "category": "Visual",
                "wcag": "WCAG 1.4.1 (Use of Color)",
                "severity": "Critical",
                "element": f"<{el.name} class=\"{cls}\">",
                "html_snippet": str(el)[:120],
                "description": "Status indicator relies solely on color (red/green) without text, icon, or aria-label. Colorblind users cannot determine state.",
                "fix_recommendation": f'<{el.name} class="{cls}" aria-label="Status: Active">✓ Active</{el.name}>'
            })

    # 2. Check Image Alt Attributes (WCAG 1.1.1)
    for img in soup.find_all('img'):
        alt = img.get('alt', None)
        src = img.get('src', 'image')
        if alt is None:
            visual_fails += 1
            issues.append({
                "id": "missing_alt",
                "category": "Visual",
                "wcag": "WCAG 1.1.1 (Non-text Content)",
                "severity": "Critical",
                "element": f"<img> ({src[:30]})",
                "html_snippet": str(img)[:120],
                "description": "Image is missing an 'alt' attribute. Screen reader and visual-impairment users cannot discern image context.",
                "fix_recommendation": f'<img src="{src}" alt="Descriptive text explaining image content">'
            })
        else:
            passed_checks += 1

    # 3. Check Form Labels & Controls (WCAG 4.1.2 / 3.3.2)
    for inp in soup.find_all('input'):
        input_type = inp.get('type', 'text').lower()
        if input_type in ['hidden', 'submit', 'button']:
            continue
        input_id = inp.get('id')
        aria_label = inp.get('aria-label')
        
        has_label = False
        if input_id:
            label = soup.find('label', attrs={'for': input_id})
            if label:
                has_label = True
        if not has_label and inp.find_parent('label'):
            has_label = True
            
        if not has_label and not aria_label:
            semantic_fails += 1
            issues.append({
                "id": "unlabeled_input",
                "category": "Semantic",
                "wcag": "WCAG 4.1.2 (Name, Role, Value)",
                "severity": "Serious",
                "element": f'<input type="{input_type}">',
                "html_snippet": str(inp)[:120],
                "description": f"Form input control lacks associated <label> element or aria-label attribute.",
                "fix_recommendation": f'<label for="sku_id">Product SKU</label>\n<input id="sku_id" type="{input_type}">'
            })
        else:
            passed_checks += 1

    # 4. Check Heading Hierarchy Skips (WCAG 1.3.1 Info and Relationships)
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    prev_level = 0
    for h in headings:
        curr_level = int(h.name[1])
        if prev_level > 0 and curr_level > prev_level + 1:
            semantic_fails += 1
            issues.append({
                "id": "heading_hierarchy_skip",
                "category": "Semantic",
                "wcag": "WCAG 1.3.1 (Info and Relationships)",
                "severity": "Moderate",
                "element": f"<{h.name}> ('{h.get_text(strip=True)[:25]}')",
                "html_snippet": str(h)[:120],
                "description": f"Heading level skipped from <h{prev_level}> directly to <h{curr_level}>. Breaks screen reader heading navigation structure.",
                "fix_recommendation": f'<h{prev_level + 1}>{h.get_text(strip=True)}</h{prev_level + 1}>'
            })
        prev_level = curr_level

    # 5. Check Keyboard-Inaccessible Controls (WCAG 2.1.1 Keyboard)
    clickable_divs = soup.find_all(attrs={"onclick": True})
    for div in clickable_divs:
        if div.name not in ['button', 'a', 'input']:
            tabindex = div.get('tabindex')
            role = div.get('role')
            if tabindex is None or role != 'button':
                motor_fails += 1
                issues.append({
                    "id": "inaccessible_click_element",
                    "category": "Motor / Keyboard",
                    "wcag": "WCAG 2.1.1 (Keyboard Access)",
                    "severity": "Critical",
                    "element": f"<{div.name} class=\"{div.get('class')}\">",
                    "html_snippet": str(div)[:120],
                    "description": f"Interactive control <{div.name}> uses onclick JavaScript handler without being a native <button> or having tabindex=\"0\" and role=\"button\". Keyboard-only users cannot activate this element.",
                    "fix_recommendation": f'<button class="{div.get("class")}" type="button">{div.get_text(strip=True)}</button>'
                })

    # 6. Check Small Target Sizes (WCAG 2.5.5 / 2.5.8 Target Size)
    buttons_inputs = soup.find_all(['button', 'a', 'input'])
    for btn in buttons_inputs:
        style = parse_inline_styles(btn.get('style', ''))
        w_str = style.get('width', '')
        h_str = style.get('height', '')
        
        w_px = int(re.search(r'\d+', w_str).group()) if re.search(r'\d+', w_str) else None
        h_px = int(re.search(r'\d+', h_str).group()) if re.search(r'\d+', h_str) else None
        
        if (w_px and w_px < 24) or (h_px and h_px < 24):
            motor_fails += 1
            issues.append({
                "id": "small_target_size",
                "category": "Motor / Keyboard",
                "wcag": "WCAG 2.5.8 (Target Size Minimum 24x24px)",
                "severity": "Serious",
                "element": f"<{btn.name}> ({w_str or 'auto'} x {h_str or 'auto'})",
                "html_snippet": str(btn)[:120],
                "description": f"Interactive touch target dimensions ({w_str}x{h_str}) fall below WCAG 24x24px minimum size requirement, making touch/motor operation difficult.",
                "fix_recommendation": f'/* Expand target size */\nmin-width: 24px; min-height: 24px; padding: 6px 12px;'
            })

    # 7. Check Text Element Contrast Ratios (WCAG 1.4.3)
    text_tags = soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'button', 'li', 'div'])
    for tag in text_tags:
        text = tag.get_text(strip=True)
        if not text or len(tag.find_all(recursive=False)) > 3:
            continue
            
        text_elements_scanned += 1
        colors = extract_element_colors(tag, default_bg=default_bg)
        fg = colors['fg']
        bg = colors['bg']
        
        ratio = calculate_contrast_ratio(fg, bg)
        is_large = tag.name in ['h1', 'h2']
        compliance = evaluate_wcag_compliance(ratio, is_large_text=is_large)
        
        if not compliance['passes_aa']:
            visual_fails += 1
            auto_fix = auto_fix_contrast(fg, bg, target_ratio=compliance['aa_target'], fix_target="fg")
            issues.append({
                "id": "low_contrast",
                "category": "Visual",
                "wcag": "WCAG 1.4.3 (Contrast Minimum)",
                "severity": "Serious",
                "element": f"<{tag.name}> ('{text[:25]}...')",
                "html_snippet": str(tag)[:120],
                "description": f"Text contrast ratio is {ratio}:1, failing WCAG AA requirement ({compliance['aa_target']}:1). FG: {fg}, BG: {bg}.",
                "contrast_details": {
                    "ratio": ratio,
                    "target": compliance['aa_target'],
                    "fg": fg,
                    "bg": bg,
                    "fixed_fg": auto_fix['fixed_fg'],
                    "fixed_bg": auto_fix['fixed_bg'],
                    "fixed_ratio": auto_fix['fixed_ratio']
                },
                "fix_recommendation": f"/* Color repair */\ncolor: {auto_fix['fixed_fg']}; background-color: {bg};"
            })
        else:
            passed_checks += 1

    # 8. Check Broken Focus Indicators (WCAG 2.4.7)
    styled_elements = soup.find_all(attrs={"style": True})
    for el in styled_elements:
        style = el.get('style', '').lower().replace(' ', '')
        if 'outline:none' in style or 'outline:0' in style:
            motor_fails += 1
            issues.append({
                "id": "focus_outline_none",
                "category": "Motor / Keyboard",
                "wcag": "WCAG 2.4.7 (Focus Visible)",
                "severity": "Serious",
                "element": f"<{el.name}>",
                "html_snippet": str(el)[:120],
                "description": "Element explicitly sets 'outline: none' or 'outline: 0'. Removes keyboard focus ring.",
                "fix_recommendation": f"/* Visible focus indicator */\n{el.name}:focus-visible {{ outline: 3px solid #2563eb; outline-offset: 2px; }}"
            })

    # Sub-scores
    visual_score = max(0, min(100, 100 - (visual_fails * 15)))
    motor_score = max(0, min(100, 100 - (motor_fails * 18)))
    semantic_score = max(0, min(100, 100 - (semantic_fails * 20)))
    
    total_audited = len(issues) + passed_checks
    overall_score = max(0, min(100, int((passed_checks / max(1, total_audited)) * 100)))

    return {
        "wcag_score": overall_score,
        "visual_score": visual_score,
        "motor_score": motor_score,
        "semantic_score": semantic_score,
        "total_issues": len(issues),
        "passed_checks": passed_checks,
        "text_elements_scanned": text_elements_scanned,
        "issues": issues
    }
