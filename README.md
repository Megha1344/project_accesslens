# AccessLens — Premium Developer Accessibility Suite 👁️⚡

> **"Don't just audit it — experience it!"**

**AccessLens** is an interactive, premium developer tool built entirely in Python using **Streamlit**. It solves the fundamental gap in web accessibility engineering: while developers can run automated audits (Lighthouse, axe), they don't actually understand what those accessibility problems look or feel like for users with visual or motor impairments.

AccessLens enables developers to **visually and interactively experience** their website's accessibility issues, understand WCAG rules deeply, auto-suggest fixes, and immediately verify compliance.

---

## 🌟 Key Features

1. **🏠 Modern Hero & Developer Landing**:
   - Sleek developer tool UI showcasing the AccessLens value proposition ("Static Audit vs. Sensory Experience"), interactive feature cards, and quick CTAs.

2. **👁️ Sensory Vision & Impairment Simulator Engine**:
   - Live browser preview with SVG color transformation matrices and CSS filters:
     - **Color Blindness**: Protanopia (Red-blind), Deuteranopia (Green-blind), Tritanopia (Blue-blind), Achromatopsia (Monochromacy).
     - **Ocular Conditions**: Low Visual Acuity (20/100 blur), Cataracts (Cloudiness + lens glare), Glaucoma (Peripheral tunnel vision), Macular Degeneration.
     - **Side-by-Side View**: Compare Normal Vision vs. Simulated Impairment in real-time.
     - **Motor Tremor Simulator**: Interactive fine-motor tremor overlay simulating mouse click inaccuracy.

3. **⌨️ Keyboard Navigation Journey Center**:
   - Visual step-by-step map of DOM focus sequences.
   - Audits missing focus indicators (`outline: none` without alternative) and positive `tabindex` violations (WCAG 2.4.3 & 2.4.7).
   - Identifies potential modal dialog keyboard traps (WCAG 2.1.2).

4. **🎨 Auto-Suggested Contrast Ratio Fixer**:
   - Built on WCAG 2.1 Relative Luminance formulas ($L = 0.2126R + 0.7152G + 0.0722B$).
   - Evaluates text contrast against Level AA (4.5:1 / 3.0:1) and Level AAA (7.0:1 / 4.5:1).
   - **1-Click Color Repair**: Automatically adjusts text/background luminance to achieve target contrast while preserving original hue & saturation.

5. **🧪 Inspection Sandbox & DOM Parser**:
   - Dual input modes: Fetch any live website URL or paste custom HTML & CSS snippets.
   - Real-time BeautifulSoup DOM parser checking image `alt` attributes (WCAG 1.1.1), unlabeled form inputs & buttons (WCAG 4.1.2), and low contrast elements.
   - **1-Click Exports**: Download complete JSON audit reports and auto-generated `accesslens_fixes.css` files.

---

## 📁 Repository Structure

```
accesslens/
├── app.py                      # Main Streamlit Application Entry Point
├── requirements.txt            # Python Dependencies
├── README.md                   # Complete Guide & GitHub Instructions
├── core/
│   ├── __init__.py
│   ├── wcag_math.py            # WCAG 2.1 Relative Luminance, Contrast Ratios & Auto-Fixer
│   ├── vision_filters.py       # SVG Colorblind Matrices & CSS Impairment Filters
│   ├── dom_parser.py           # BeautifulSoup DOM Accessibility Auditor
│   └── keyboard_traps.py      # Keyboard Tab Sequence & Focus Trap Engine
├── components/
│   ├── __init__.py
│   ├── hero.py                 # Modern Hero Landing Component
│   ├── live_inspector.py       # Live Website & Vision Filter Preview Component
│   ├── sandbox.py              # Raw HTML/CSS Code Editor & Sandbox
│   ├── contrast_fixer.py       # Auto-Suggested Contrast Ratio Engine UI
│   ├── keyboard_tracer.py      # Keyboard Navigation Journey Center UI
│   └── audit_summary.py        # WCAG Issue Inspector, Metrics Bar & Exporter
├── samples/
│   ├── __init__.py
│   └── demo_sites.py           # Pre-built Accessible & Inaccessible HTML Presets
└── tests/
    ├── __init__.py
    └── test_wcag.py            # Unit Test Suite
```

---

## 🚀 Quick Start & Installation

### 1. Clone or Navigate to the Project
```bash
git clone https://github.com/your-username/accesslens.git
cd accesslens
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

AccessLens will automatically open in your default browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests

To run the automated core algorithm test suite:

```bash
python -m unittest discover -s tests
```

---

## 📤 Commit to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AccessLens developer accessibility suite"
git branch -M main
git remote add origin https://github.com/your-username/accesslens.git
git push -u origin main
```
