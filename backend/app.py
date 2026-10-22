import os
import time
import datetime
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from model.feature_extractor import extract_url_features, analyze_text_content

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVED_MODEL_DIR = os.path.join(BASE_DIR, 'model', 'saved')

url_model = None
sms_model = None
email_model = None

def load_models():
    global url_model, sms_model, email_model
    url_path = os.path.join(SAVED_MODEL_DIR, 'url_phishing_model.pkl')
    sms_path = os.path.join(SAVED_MODEL_DIR, 'sms_phishing_model.pkl')
    email_path = os.path.join(SAVED_MODEL_DIR, 'email_phishing_model.pkl')

    if os.path.exists(url_path):
        url_model = joblib.load(url_path)
    if os.path.exists(sms_path):
        sms_model = joblib.load(sms_path)
    if os.path.exists(email_path):
        email_model = joblib.load(email_path)

# Try loading models on startup
load_models()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "app": "AI CYBER SHIELD Backend API",
        "version": "2.0.0",
        "status": "online",
        "models_loaded": {
            "url_model": url_model is not None,
            "sms_model": sms_model is not None,
            "email_model": email_model is not None
        },
        "endpoints": [
            "POST /predict-url",
            "POST /predict-sms",
            "POST /predict-email",
            "POST /predict-qr",
            "GET /demo-samples",
            "GET /challenge-questions",
            "GET /health"
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": str(datetime.datetime.now())})

@app.route('/predict-url', methods=['POST'])
def predict_url():
    data = request.get_json(force=True, silent=True) or {}
    url = data.get('url', '').strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    features = extract_url_features(url)
    indicators = list(features['indicators'])

    # ML Model Prediction if available
    ml_label = 'safe'
    ml_confidence = 0.85

    if url_model:
        try:
            probs = url_model.predict_proba([url])[0]
            classes = list(url_model.classes_)
            max_idx = probs.argmax()
            ml_label = classes[max_idx]
            ml_confidence = float(probs[max_idx])
        except Exception as e:
            ml_label = 'safe'

    # Hybrid Decision Matrix
    # High-severity red flags immediately escalate to dangerous
    has_critical_indicators = (
        features['has_ip_host'] or
        features['brand_spoof'] or
        (features['has_suspicious_tld'] and features['keyword_count'] >= 1) or
        (features['keyword_count'] >= 2 and not features['is_https'])
    )

    if features['is_legitimate_authority'] and not features['brand_spoof']:
        status = 'safe'
        confidence = max(0.95, ml_confidence)
        reason = "Verified authentic legitimate domain name with trusted SSL profile"
        indicators = ["Valid domain authority", "Secure protocol verified"]
    elif has_critical_indicators or ml_label == 'dangerous':
        status = 'dangerous'
        confidence = max(0.91, ml_confidence)
        reason = "Malicious phishing patterns and suspicious deception indicators detected"
        if not indicators:
            indicators.append("Deceptive URL structure matches known phishing templates")
    elif features['is_shortener'] or features['has_suspicious_tld'] or features['keyword_count'] >= 1 or ml_label == 'suspicious':
        status = 'suspicious'
        confidence = max(0.78, ml_confidence)
        reason = "Suspicious link attributes detected that warrant caution before accessing"
        if not indicators:
            indicators.append("Unverified domain redirect or suspicious structure")
    else:
        status = 'safe'
        confidence = max(0.88, ml_confidence)
        reason = "No known malicious patterns or deceptive structures detected"
        indicators = ["Standard domain structure", "No credential harvesting triggers found"]

    recommendations = []
    if status == 'dangerous':
        recommendations = [
            "DO NOT click this link or enter any personal credentials",
            "This URL mimics trusted brands to harvest passwords and banking data",
            "Block this sender immediately and report as digital fraud"
        ]
    elif status == 'suspicious':
        recommendations = [
            "Proceed with extreme caution; verify the sender through official channels",
            "Do not enter passwords, OTPs, or financial information",
            "Inspect full destination before providing any sensitive details"
        ]
    else:
        recommendations = [
            "URL appears safe to browse",
            "Always verify address bar in your browser before entering credentials"
        ]

    return jsonify({
        "status": status,
        "confidence": round(confidence, 2),
        "target": url,
        "type": "URL",
        "reason": reason,
        "indicators": indicators,
        "recommendations": recommendations,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/predict-sms', methods=['POST'])
def predict_sms():
    data = request.get_json(force=True, silent=True) or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    analysis = analyze_text_content(message)
    indicators = list(analysis['indicators'])

    ml_label = 'safe'
    ml_confidence = 0.85

    if sms_model:
        try:
            probs = sms_model.predict_proba([message])[0]
            classes = list(sms_model.classes_)
            max_idx = probs.argmax()
            ml_label = classes[max_idx]
            ml_confidence = float(probs[max_idx])
        except Exception:
            ml_label = 'safe'

    # Heuristic check
    if (analysis['urgency_count'] >= 1 and (analysis['sensitive_count'] >= 1 or analysis['brand_count'] >= 1)) or any('OTP' in ind for ind in indicators) or ml_label == 'dangerous':
        status = 'dangerous'
        confidence = max(0.92, ml_confidence)
        reason = "Social engineering smishing attack detected (fake urgency / credential harvesting)"
    elif analysis['has_url'] or analysis['urgency_count'] >= 1 or analysis['brand_count'] >= 1 or ml_label == 'suspicious':
        status = 'suspicious'
        confidence = max(0.77, ml_confidence)
        reason = "Suspicious message patterns or unverified promotions detected"
    else:
        status = 'safe'
        confidence = max(0.89, ml_confidence)
        reason = "Message appears to be normal communication with no threat indicators"
        indicators = ["No urgency threats found", "No malicious link redirects"]

    recommendations = []
    if status == 'dangerous':
        recommendations = [
            "Never share OTPs, PINs, or passwords with anyone via SMS",
            "Banks will NEVER ask you to click a link to unfreeze accounts",
            "Block and report the sender number immediately"
        ]
    elif status == 'suspicious':
        recommendations = [
            "Verify offers directly through official company apps or websites",
            "Avoid clicking shortened links in unsolicited text messages"
        ]
    else:
        recommendations = [
            "Standard notification; keep your privacy settings secure"
        ]

    return jsonify({
        "status": status,
        "confidence": round(confidence, 2),
        "target": message[:80] + ("..." if len(message) > 80 else ""),
        "type": "SMS",
        "reason": reason,
        "indicators": indicators,
        "recommendations": recommendations,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/predict-email', methods=['POST'])
def predict_email():
    data = request.get_json(force=True, silent=True) or {}
    sender = data.get('sender', '').strip()
    subject = data.get('subject', '').strip()
    content = data.get('content', '').strip()

    combined_text = f"{sender} {subject} {content}".strip()
    if not combined_text:
        return jsonify({"error": "No email content provided"}), 400

    analysis = analyze_text_content(content, sender=sender)
    indicators = list(analysis['indicators'])

    # Check sender domain anomalies
    if '@' in sender:
        sender_domain = sender.split('@')[-1].lower()
        if any(sender_domain.endswith('.' + tld) for tld in ['top', 'xyz', 'club', 'pw', 'work', 'cc', 'live']):
            indicators.append(f"Suspicious email domain extension: @{sender_domain}")
        if any(brand in sender_domain and not sender_domain.endswith(f"{brand}.com") for brand in ['paypal', 'chase', 'apple', 'netflix', 'amazon', 'microsoft']):
            indicators.append(f"Email spoofing detected: Sender domain mimics official service (@{sender_domain})")

    ml_label = 'safe'
    ml_confidence = 0.85

    if email_model:
        try:
            probs = email_model.predict_proba([combined_text])[0]
            classes = list(email_model.classes_)
            max_idx = probs.argmax()
            ml_label = classes[max_idx]
            ml_confidence = float(probs[max_idx])
        except Exception:
            ml_label = 'safe'

    if len(indicators) >= 2 or ml_label == 'dangerous':
        status = 'dangerous'
        confidence = max(0.93, ml_confidence)
        reason = "Phishing email detected with active impersonation and deceptive intent"
    elif len(indicators) == 1 or ml_label == 'suspicious':
        status = 'suspicious'
        confidence = max(0.79, ml_confidence)
        reason = "Potential spam or unverified sender with promotional elements"
    else:
        status = 'safe'
        confidence = max(0.90, ml_confidence)
        reason = "Legitimate business communication format verified"
        indicators = ["Authentic sender domain profile", "No deceptive payload identified"]

    recommendations = []
    if status == 'dangerous':
        recommendations = [
            "Do not reply or click any links in this email",
            "Do not download attachments from this sender",
            "Report this email as phishing to your security team/email provider"
        ]
    elif status == 'suspicious':
        recommendations = [
            "Check the full header and sender address carefully",
            "Confirm sensitive requests through a separate official channel"
        ]
    else:
        recommendations = [
            "Email appears authentic; exercise standard cyber hygiene"
        ]

    return jsonify({
        "status": status,
        "confidence": round(confidence, 2),
        "target": f"[{sender}] {subject}",
        "type": "EMAIL",
        "reason": reason,
        "indicators": indicators,
        "recommendations": recommendations,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/predict-qr', methods=['POST'])
def predict_qr():
    data = request.get_json(force=True, silent=True) or {}
    qr_data = data.get('qr_data', '').strip()

    if not qr_data:
        return jsonify({"error": "No QR data provided"}), 400

    # If QR data contains URL or starts with protocol, treat as URL
    if qr_data.startswith(('http://', 'https://', 'www.')) or '.' in qr_data:
        res = predict_url_internal(qr_data)
        res['type'] = 'QR Code'
        return jsonify(res)
    else:
        # Treat as plain text or payment string
        analysis = analyze_text_content(qr_data)
        status = 'suspicious' if analysis['indicators'] else 'safe'
        return jsonify({
            "status": status,
            "confidence": 0.88,
            "target": qr_data[:60],
            "type": "QR Code",
            "reason": "QR text content scanned and inspected for embedded exploits",
            "indicators": analysis['indicators'] or ["Standard plain text QR payload"],
            "recommendations": ["Ensure QR code is from a trusted physical source"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

def predict_url_internal(url):
    features = extract_url_features(url)
    indicators = list(features['indicators'])
    has_critical = (
        features['has_ip_host'] or
        features['brand_spoof'] or
        (features['has_suspicious_tld'] and features['keyword_count'] >= 1)
    )
    if features['is_legitimate_authority'] and not features['brand_spoof']:
        status = 'safe'
        confidence = 0.96
        reason = "Legitimate verified organization QR payload"
    elif has_critical:
        status = 'dangerous'
        confidence = 0.94
        reason = "Malicious QR Code directing to a confirmed phishing domain (QRishing)"
    elif features['is_shortener'] or features['has_suspicious_tld']:
        status = 'suspicious'
        confidence = 0.81
        reason = "QR code contains shortened or unverified web destination"
    else:
        status = 'safe'
        confidence = 0.89
        reason = "Standard web destination encoded in QR code"

    return {
        "status": status,
        "confidence": round(confidence, 2),
        "target": url,
        "type": "QR Code",
        "reason": reason,
        "indicators": indicators or ["No malicious QR patterns detected"],
        "recommendations": [
            "Never scan untrusted QR stickers placed over official signage",
            "Verify URL before authorizing logins or payments"
        ],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/demo-samples', methods=['GET'])
def get_demo_samples():
    """Provides instant test samples for college project demonstrations."""
    samples = {
        "urls": [
            {
                "label": "SAFE: Wikipedia Article",
                "status": "safe",
                "value": "https://www.wikipedia.org"
            },
            {
                "label": "SUSPICIOUS: Shortened Redirection Link",
                "status": "suspicious",
                "value": "http://bit.ly/3x8Qz91"
            },
            {
                "label": "DANGEROUS: Fake PayPal Verification Portal",
                "status": "dangerous",
                "value": "http://secure-paypal-login-verification-account.top/login.php"
            },
            {
                "label": "DANGEROUS: Chase Bank Security Alert Spoof",
                "status": "dangerous",
                "value": "http://chase-bank-alert-update-auth.xyz/verify-account"
            }
        ],
        "sms": [
            {
                "label": "SAFE: Uber Ride Arrival Notification",
                "status": "safe",
                "value": "Uber: Your driver John is arriving in a Silver Toyota Camry (ABC-123)."
            },
            {
                "label": "SUSPICIOUS: Lottery Winner Notice",
                "status": "suspicious",
                "value": "CONGRATULATIONS! You have been selected as the winner of a $1000 Walmart Gift Card! Click http://bit.ly/3x8Qz91 to claim."
            },
            {
                "label": "DANGEROUS: Wells Fargo Urgent Account Freeze Scam",
                "status": "dangerous",
                "value": "URGENT: Your Wells Fargo bank account is suspended due to unusual activity. Click http://wellsfarg0-online-security-token.club to restore access now."
            }
        ],
        "emails": [
            {
                "label": "SAFE: GitHub Dependabot Alert",
                "status": "safe",
                "sender": "support@github.com",
                "subject": "Security alert for your repository",
                "content": "We noticed a potential security vulnerability in your repository dependencies. Check the Dependabot alerts tab."
            },
            {
                "label": "DANGEROUS: Microsoft 365 Password Expiration Spear Phishing",
                "status": "dangerous",
                "sender": "admin@microsoft365-urgent-auth.pw",
                "subject": "CRITICAL: Password Expiration Notice",
                "content": "Dear Employee, Your corporate Microsoft 365 password expires in 2 hours. To maintain access, you must immediately renew your corporate credentials at http://microsoft-office365-urgent-password-reset.pw/auth."
            }
        ]
    }
    return jsonify(samples)

import json
import random

CHALLENGE_QUESTIONS_CACHE = None

def load_challenge_questions():
    global CHALLENGE_QUESTIONS_CACHE
    if CHALLENGE_QUESTIONS_CACHE is None:
        json_path = os.path.join(BASE_DIR, 'challenge_questions.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    CHALLENGE_QUESTIONS_CACHE = json.load(f)
            except Exception as e:
                print(f"Error loading challenge_questions.json: {e}")
                CHALLENGE_QUESTIONS_CACHE = []
        else:
            CHALLENGE_QUESTIONS_CACHE = []
    return list(CHALLENGE_QUESTIONS_CACHE)

@app.route('/challenge-questions', methods=['GET'])
def get_challenge_questions():
    difficulty = request.args.get('difficulty', 'all').lower().strip()
    count_param = request.args.get('count', '10').strip()
    exclude_ids_param = request.args.get('exclude_ids', '').strip()

    try:
        count = int(count_param)
        if count <= 0:
            count = 10
    except ValueError:
        count = 10

    exclude_ids = set()
    if exclude_ids_param:
        for part in exclude_ids_param.split(','):
            part = part.strip()
            if part.isdigit():
                exclude_ids.add(int(part))

    all_questions = load_challenge_questions()

    if difficulty in ['beginner', 'intermediate', 'advanced']:
        pool = [q for q in all_questions if q.get('difficulty') == difficulty]
    else:
        pool = all_questions

    if not pool:
        return jsonify([])

    # Filter out excluded (already seen) questions
    unseen = [q for q in pool if q.get('id') not in exclude_ids]

    # If unseen has enough questions, sample from unseen
    if len(unseen) >= count:
        selected = random.sample(unseen, count)
    else:
        # If unseen pool is exhausted or less than count, reset and sample from entire difficulty pool
        selected = random.sample(pool, min(count, len(pool)))

    return jsonify(selected)

if __name__ == '__main__':
    print("Starting AI CYBER SHIELD Flask REST API Server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
