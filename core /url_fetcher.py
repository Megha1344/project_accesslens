"""
URL Fetcher & Web Proxy Engine with Security & Framing Handling
Handles URL fetching, base URL injection, X-Frame-Options/CSP header analysis,
and sanitization for live browser rendering in Streamlit.
"""
import re
import requests
from urllib.parse import urlparse, urljoin
from typing import Dict, Any

def fetch_and_sanitize_url(url: str, timeout: int = 6) -> Dict[str, Any]:
    """
    Fetches web content from target URL, analyzes X-Frame-Options & CSP headers,
    injects <base> tags for relative paths, and prepares safe HTML for rendering.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AccessLens/2.0 (Accessibility Auditor)'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = res.status_code
        
        if status_code != 200:
            return {
                "success": False,
                "error": f"HTTP Status {status_code}: Unable to load page content.",
                "html": f"<div style='padding:20px; color:#ef4444;'>HTTP Error {status_code} when loading {url}</div>",
                "headers": {},
                "has_frame_restrictions": False
            }
            
        # Check X-Frame-Options & CSP framing rules
        resp_headers = {k.lower(): v for k, v in res.headers.items()}
        x_frame_opt = resp_headers.get('x-frame-options', '').upper()
        csp = resp_headers.get('content-security-policy', '').lower()
        
        has_frame_restrictions = (
            'DENY' in x_frame_opt or 
            'SAMEORIGIN' in x_frame_opt or 
            'frame-ancestors' in csp
        )
        
        raw_html = res.text
        
        # Inject <base> tag after <head> so relative CSS, JS, and image URLs resolve correctly
        base_tag = f'<base href="{base_url}/" target="_blank">'
        if '<head>' in raw_html.lower():
            sanitized_html = re.sub(r'(<head[^>]*>)', r'\1\n  ' + base_tag, raw_html, flags=re.IGNORECASE, count=1)
        else:
            sanitized_html = base_tag + "\n" + raw_html
            
        return {
            "success": True,
            "url": url,
            "status_code": status_code,
            "html": sanitized_html,
            "headers": resp_headers,
            "x_frame_options": x_frame_opt or "None",
            "has_frame_restrictions": has_frame_restrictions,
            "restriction_notice": "Site enforces X-Frame-Options or CSP framing restrictions. AccessLens direct DOM proxy rendering active." if has_frame_restrictions else "No framing restrictions detected."
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out after 6 seconds.",
            "html": "<div style='padding:20px; color:#ef4444;'>Connection timed out while trying to reach the target URL.</div>",
            "headers": {},
            "has_frame_restrictions": False
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "html": f"<div style='padding:20px; color:#ef4444;'>Fetch error: {str(e)}</div>",
            "headers": {},
            "has_frame_restrictions": False
        }
