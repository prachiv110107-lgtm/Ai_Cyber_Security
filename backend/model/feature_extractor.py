import re
import math
from urllib.parse import urlparse
import tldextract

# Suspicious Top-Level Domains frequently abused in phishing campaigns
SUSPICIOUS_TLDS = {
    'top', 'xyz', 'club', 'work', 'click', 'ru', 'cn', 'gq', 'tk', 'ga', 'cf',
    'ml', 'cc', 'pw', 'su', 'bid', 'date', 'buzz', 'live', 'info', 'biz'
}

# Known URL shortener domains
SHORTENER_DOMAINS = {
    'bit.ly', 'tinyurl.com', 't.co', 'is.gd', 'cutt.ly', 'rb.gy', 'goo.gl',
    'ow.ly', 'buff.ly', 'rebrand.ly', 'shorturl.at', 'bl.ink'
}

# High-profile targeted brands
TARGETED_BRANDS = [
    'paypal', 'chase', 'bankofamerica', 'wellsfargo', 'apple', 'amazon',
    'netflix', 'microsoft', 'google', 'facebook', 'instagram', 'binance',
    'coinbase', 'metamask', 'citibank', 'barclays', 'hsbc', 'usps', 'fedex', 'dhl', 'irs'
]

# Sensitive phishing intent keywords
SENSITIVE_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'update', 'account', 'security',
    'secure', 'banking', 'wallet', 'suspend', 'blocked', 'confirm', 'password',
    'auth', 'refund', 'unlock', 'claim', 'kyc', 'recovery', 'seed-phrase', 'token'
]

# Urgent action keywords in text
URGENCY_KEYWORDS = [
    'urgent', 'immediately', 'suspended', 'blocked', 'unauthorized', 'expire',
    'critical', 'final notice', 'within 24 hours', 'action required', 'restricted',
    'compromised', 'frozen', 'terminate', 'won', 'winner', 'free', 'airdrop'
]

def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy to detect algorithmically generated or obfuscated strings."""
    if not text:
        return 0.0
    entropy = 0.0
    for char in set(text):
        p_x = float(text.count(char)) / len(text)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return round(entropy, 3)

def extract_url_features(url: str) -> dict:
    """Extract lexical, structural, and brand-spoofing features from a URL."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url_with_scheme = 'http://' + url
    else:
        url_with_scheme = url

    parsed = urlparse(url_with_scheme)
    ext = tldextract.extract(url_with_scheme)

    domain = (ext.domain + '.' + ext.suffix).lower() if ext.suffix else ext.domain.lower()
    subdomain = ext.subdomain.lower()
    suffix = ext.suffix.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()
    full_str = url.lower()

    # Features
    length = len(url)
    dot_count = url.count('.')
    hyphen_count = url.count('-')
    at_symbol = 1 if '@' in url else 0
    double_slash_redirect = 1 if '//' in parsed.path else 0
    is_https = 1 if parsed.scheme == 'https' else 0

    # IP address host detection
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
    has_ip_host = 1 if re.match(ip_pattern, netloc) else 0

    # Suspicious TLD
    has_suspicious_tld = 1 if suffix in SUSPICIOUS_TLDS else 0

    # Shortener
    is_shortener = 1 if domain in SHORTENER_DOMAINS or netloc in SHORTENER_DOMAINS else 0

    # Subdomain depth
    subdomain_parts = subdomain.split('.') if subdomain else []
    subdomain_depth = len([p for p in subdomain_parts if p])

    # Target brand spoofing check
    brand_in_subdomain_or_path = 0
    detected_brands = []
    for brand in TARGETED_BRANDS:
        if brand in full_str:
            detected_brands.append(brand)
            # If brand is in subdomain/path but NOT in root domain -> High risk spoofing!
            if brand not in ext.domain.lower():
                brand_in_subdomain_or_path = 1

    # Sensitive keyword count
    keyword_matches = [kw for kw in SENSITIVE_KEYWORDS if kw in full_str]
    keyword_count = len(keyword_matches)

    entropy = calculate_entropy(netloc)

    indicators = []
    if has_ip_host:
        indicators.append("IP address host used instead of legitimate domain name")
    if brand_in_subdomain_or_path:
        indicators.append(f"Target brand name spoofed in URL: {', '.join(detected_brands)}")
    if has_suspicious_tld:
        indicators.append(f"High-risk top level domain: .{suffix}")
    if is_shortener:
        indicators.append("URL shortening service disguises actual destination")
    if keyword_count >= 2:
        indicators.append(f"Multiple security/credential keywords in URL: {', '.join(keyword_matches[:3])}")
    if not is_https:
        indicators.append("Unencrypted connection (HTTP instead of HTTPS)")
    if hyphen_count >= 3:
        indicators.append("Excessive hyphens in domain name (common phishing pattern)")
    if subdomain_depth >= 2:
        indicators.append("Deeply nested subdomains attempting to mimic official portals")
    if at_symbol:
        indicators.append("@ symbol present (used in URL credential spoofing)")

    feature_dict = {
        'length': length,
        'dot_count': dot_count,
        'hyphen_count': hyphen_count,
        'at_symbol': at_symbol,
        'double_slash_redirect': double_slash_redirect,
        'is_https': is_https,
        'has_ip_host': has_ip_host,
        'has_suspicious_tld': has_suspicious_tld,
        'is_shortener': is_shortener,
        'subdomain_depth': subdomain_depth,
        'brand_spoof': brand_in_subdomain_or_path,
        'keyword_count': keyword_count,
        'entropy': entropy,
        'indicators': indicators,
        'domain': domain,
        'is_legitimate_authority': 1 if domain in ['wikipedia.org', 'google.com', 'github.com', 'microsoft.com', 'apple.com', 'amazon.com'] else 0
    }
    return feature_dict

def analyze_text_content(text: str, sender: str = "") -> dict:
    """Analyze SMS or Email content for social engineering and phishing indicators."""
    text_lower = (sender + " " + text).lower()
    
    urgency_matches = [w for w in URGENCY_KEYWORDS if w in text_lower]
    sensitive_matches = [w for w in SENSITIVE_KEYWORDS if w in text_lower]
    brand_matches = [b for b in TARGETED_BRANDS if b in text_lower]

    # Look for URLs in text
    url_pattern = r'(https?://\S+|www\.\S+|bit\.ly/\S+|tinyurl\.com/\S+|[a-zA-Z0-9-]+\.(?:top|xyz|club|work|click|pw|live|cc)/\S*)'
    found_urls = re.findall(url_pattern, text)

    indicators = []
    if urgency_matches:
        indicators.append(f"Urgent pressure language: {', '.join(urgency_matches[:3])}")
    if sensitive_matches:
        indicators.append(f"Credential/account request keywords: {', '.join(sensitive_matches[:3])}")
    if brand_matches:
        indicators.append(f"Impersonating trusted organization: {', '.join(brand_matches[:2]).upper()}")
    if found_urls:
        indicators.append(f"Contains {len(found_urls)} link(s) prompting external click")
        for u in found_urls[:2]:
            u_feat = extract_url_features(u)
            if u_feat['has_suspicious_tld'] or u_feat['brand_spoof'] or u_feat['has_ip_host']:
                indicators.append(f"Embedded malicious link detected: {u}")

    if any(k in text_lower for k in ['otp', 'one time password', 'pin', 'social security', 'ssn', 'seed phrase']):
        indicators.append("Solicits confidential credentials (OTP / PIN / Secret Key)")

    if any(k in text_lower for k in ['wire transfer', 'gift card', 'bitcoin', 'crypto', 'direct deposit']):
        indicators.append("Financial transfer or untraceable payment request")

    return {
        'urgency_count': len(urgency_matches),
        'sensitive_count': len(sensitive_matches),
        'brand_count': len(brand_matches),
        'has_url': 1 if found_urls else 0,
        'url_count': len(found_urls),
        'found_urls': found_urls,
        'indicators': indicators
    }
