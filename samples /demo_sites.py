"""
Pre-built Sample Web Pages for AccessLens Inspection & Demonstration
Provides rich HTML & CSS templates with common accessibility challenges.
"""

DEMO_SITES = {
    "shoptech_audit_demo": {
        "title": "ShopTech E-Commerce & SaaS Portal (Contains 9 Critical Accessibility Violations)",
        "description": "Comprehensive testbed containing poor contrast, red/green status dots, missing alt text, skipped headings, unlabeled inputs, outline:none focus, div-onClick controls, bad tabindex, and tiny touch targets.",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ShopTech Cloud Portal</title>
  <style>
    body { font-family: 'Segoe UI', system-ui, sans-serif; background-color: #f8fafc; color: #64748b; margin: 0; padding: 24px; }
    .card { background: #ffffff; border-radius: 12px; padding: 28px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 24px; max-width: 850px; }
    
    /* 1. POOR CONTRAST FAIL */
    .title-sub { color: #cbd5e1; font-size: 14px; margin-top: -10px; } 
    .hdr-main { color: #94a3b8; font-size: 26px; font-weight: 700; margin-bottom: 4px; }
    .metric-label { color: #a1a1aa; font-size: 12px; text-transform: uppercase; }
    .metric-val { color: #71717a; font-size: 26px; font-weight: 700; }
    
    /* 2. RED/GREEN ONLY STATUS INDICATOR (Color-only fail) */
    .status-dot-green { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e; margin-right: 6px; }
    .status-dot-red { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444; margin-right: 6px; }
    
    /* 5. POOR FOCUS VISIBILITY (Outline none fail) */
    .input-field { padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 6px; outline: none; color: #94a3b8; margin-bottom: 12px; width: 240px; }
    .btn-submit { background-color: #93c5fd; color: #ffffff; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; outline: none; font-weight: 600; }
    
    /* 7. KEYBOARD-INACCESSIBLE CONTROL (Div onClick fail) */
    .fake-btn-checkout { background-color: #3b82f6; color: #ffffff; padding: 10px 20px; border-radius: 6px; display: inline-block; cursor: pointer; font-weight: 600; margin-top: 12px; }
    
    /* 9. SMALL TOUCH TARGET FAIL */
    .tiny-close-btn { width: 12px; height: 12px; padding: 0; font-size: 10px; border: 1px solid #cbd5e1; background: #f1f5f9; color: #64748b; cursor: pointer; border-radius: 2px; line-height: 10px; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
    .box { background: #f1f5f9; padding: 18px; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="card">
    <!-- 3. INCORRECT HEADING HIERARCHY (H1 skips directly to H4) -->
    <h1 class="hdr-main">ShopTech Merchant Dashboard</h1>
    <div class="title-sub">Manage server nodes, payments, and product inventory.</div>
    
    <div class="grid-2">
      <div class="box">
        <!-- SKIPPED HEADING LEVEL (H1 -> H4) -->
        <h4>System Node Health</h4>
        <p style="font-size: 14px; color: #94a3b8;">
          Server US-East-1: <span class="status-dot-green"></span>
          <br/>
          Database Cluster: <span class="status-dot-red"></span>
        </p>
        <!-- 8. CONFUSING TAB ORDER (tabindex="8" jump) -->
        <button class="btn-submit" tabindex="8">Refresh Metrics</button>
      </div>

      <div class="box">
        <h4>Product Quick Add</h4>
        <!-- 4. MISSING FORM LABELS (Input has placeholder only, no <label> or aria-label) -->
        <input type="text" class="input-field" placeholder="Enter Product SKU..." />
        <br/>
        <!-- 7. KEYBOARD INACCESSIBLE DIV BUTTON -->
        <div class="fake-btn-checkout" onclick="alert('Added to Store')">Save Product</div>
        
        <!-- 9. SMALL TOUCH TARGET (12x12px button) -->
        <span style="float: right;">
          Dismiss <button class="tiny-close-btn" tabindex="2">x</button>
        </span>
      </div>
    </div>

    <div style="margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
      <h4>Promotional Banner</h4>
      <!-- 3. MISSING ALT TEXT ON IMAGE -->
      <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400" style="border-radius: 8px; width: 300px;" />
      <p style="color: #cbd5e1; font-size: 13px;">Special holiday merchant discount valid through Q4.</p>
      
      <!-- 8. CONFUSING TAB ORDER (tabindex="1") -->
      <button class="btn-submit" tabindex="1">Claim Discount</button>
    </div>
  </div>
</body>
</html>"""
    },

    "accessible_storefront": {
        "title": "Aura Hardware Store (Accessible WCAG 2.1 AA Compliant)",
        "description": "Fully compliant e-commerce product showcase with high contrast, focus indicators, aria labels, and valid heading structures.",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Aura Hardware Store</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; }
    .product-card { background: #1e293b; border: 2px solid #334155; border-radius: 12px; padding: 24px; max-width: 480px; }
    h1 { color: #ffffff; font-size: 24px; margin-top: 0; }
    h2 { color: #38bdf8; font-size: 18px; margin-top: 12px; }
    .price { color: #38bdf8; font-size: 26px; font-weight: 700; margin: 12px 0; }
    .description { color: #e2e8f0; font-size: 15px; line-height: 1.5; }
    .btn-buy { background-color: #0284c7; color: #ffffff; border: none; padding: 12px 24px; font-size: 16px; font-weight: 600; border-radius: 6px; cursor: pointer; min-height: 44px; min-width: 44px; }
    .btn-buy:focus-visible { outline: 3px solid #38bdf8; outline-offset: 3px; }
    .status-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #22c55e; padding: 4px 10px; border-radius: 20px; font-size: 13px; font-weight: 600; }
  </style>
</head>
<body>
  <main class="product-card">
    <h1>Aura Wireless Headset</h1>
    <span class="status-badge">✓ In Stock (Ready to Ship)</span>
    <br/><br/>
    <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400" alt="Black Aura Wireless Over-Ear Headphones with soft leather ear cushions" style="width: 100%; border-radius: 8px;" />
    <h2>Product Details</h2>
    <div class="price">$249.00</div>
    <p class="description">Active noise cancellation with 35-hour battery life and spatial audio driver system.</p>
    <button class="btn-buy" aria-label="Add Aura Wireless Headset to Shopping Cart">Add to Cart</button>
  </main>
</body>
</html>"""
    }
}
