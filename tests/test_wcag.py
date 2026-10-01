"""
Unit Tests for AccessLens Core Algorithms & Modules
Tests WCAG luminance math, contrast ratios, auto-fixer, DOM parser, keyboard tracer, and URL fetcher.
"""
import unittest
from core.wcag_math import (
    hex_to_rgb,
    rgb_to_hex,
    calculate_relative_luminance,
    calculate_contrast_ratio,
    evaluate_wcag_compliance,
    auto_fix_contrast
)
from core.vision_filters import get_svg_filters_html, get_css_for_mode
from core.dom_parser import audit_html_accessibility
from core.keyboard_traps import analyze_keyboard_navigation
from core.url_fetcher import fetch_and_sanitize_url

class TestAccessLensCore(unittest.TestCase):
    
    def test_hex_rgb_conversions(self):
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("fff"), (255, 255, 255))
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")
        self.assertEqual(rgb_to_hex((0, 0, 0)), "#000000")

    def test_wcag_contrast_ratios(self):
        ratio_max = calculate_contrast_ratio("#000000", "#ffffff")
        self.assertEqual(ratio_max, 21.0)
        
        ratio_min = calculate_contrast_ratio("#ffffff", "#ffffff")
        self.assertEqual(ratio_min, 1.0)
        
        ratio_aa = calculate_contrast_ratio("#767676", "#ffffff")
        self.assertGreaterEqual(ratio_aa, 4.5)

    def test_wcag_compliance_evaluator(self):
        comp_pass = evaluate_wcag_compliance(21.0)
        self.assertTrue(comp_pass["passes_aa"])
        self.assertTrue(comp_pass["passes_aaa"])
        self.assertEqual(comp_pass["status"], "Pass AAA")
        
        comp_fail = evaluate_wcag_compliance(2.5)
        self.assertFalse(comp_fail["passes_aa"])
        self.assertFalse(comp_fail["passes_aaa"])
        self.assertEqual(comp_fail["status"], "Fail AA")

    def test_auto_fix_contrast(self):
        res = auto_fix_contrast("#94a3b8", "#ffffff", target_ratio=4.5, fix_target="fg")
        self.assertTrue(res["changed"])
        self.assertGreaterEqual(res["fixed_ratio"], 4.5)
        self.assertNotEqual(res["fixed_fg"], "#94a3b8")

    def test_svg_filters_generation(self):
        svg_html = get_svg_filters_html()
        self.assertIn("filter-protanopia", svg_html)
        self.assertIn("filter-deuteranopia", svg_html)
        self.assertIn("filter-tritanopia", svg_html)
        self.assertIn("filter-cataract", svg_html)

    def test_dom_parser_all_anti_patterns(self):
        sample_html = """
        <div>
          <h1>Main Heading</h1>
          <h4>Skipped Subheading (H1 to H4)</h4>
          <span style="border-radius: 50%; background-color: #ef4444; width: 12px; height: 12px; display: inline-block;"></span>
          <img src="logo.png" />
          <input type="text" placeholder="Enter name" />
          <p style="color: #cbd5e1; background-color: #ffffff;">Hard to read text</p>
          <div onclick="alert('clicked')" class="fake-btn">Div Button</div>
          <button style="outline: none; width: 12px; height: 12px;">x</button>
        </div>
        """
        audit = audit_html_accessibility(sample_html)
        issues = audit["issues"]
        issue_ids = [i["id"] for i in issues]
        
        self.assertIn("color_only_indicator", issue_ids)
        self.assertIn("missing_alt", issue_ids)
        self.assertIn("heading_hierarchy_skip", issue_ids)
        self.assertIn("unlabeled_input", issue_ids)
        self.assertIn("inaccessible_click_element", issue_ids)
        self.assertIn("small_target_size", issue_ids)
        self.assertIn("low_contrast", issue_ids)
        self.assertIn("focus_outline_none", issue_ids)

    def test_keyboard_tracer(self):
        sample_html = """
        <div>
          <a href="/home">Home</a>
          <button tabindex="2">First Focus</button>
          <input type="text" style="outline: none;" />
        </div>
        """
        res = analyze_keyboard_navigation(sample_html)
        self.assertEqual(res["total_focusable_elements"], 3)
        self.assertGreater(len(res["warnings"]), 0)

    def test_url_fetcher(self):
        res = fetch_and_sanitize_url("https://example.com")
        self.assertTrue(res["success"])
        self.assertIn("example.com", res["html"])

if __name__ == "__main__":
    unittest.main()
