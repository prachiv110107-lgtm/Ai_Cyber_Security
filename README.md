<<<<<<< HEAD
# AI CYBER SHIELD – Intelligent Phishing & Digital Scam Protection System

**AI CYBER SHIELD** is a comprehensive, multi-modal cybersecurity defense mobile application and machine learning backend engineered to detect, classify, explain, and block digital threats including:
- 🔗 **Phishing URLs & Malicious Web Links**
- 📱 **QR Code Scams (QRishing)**
- 💬 **SMS Fraud & Smishing Attacks**
- 📧 **Spear Phishing & Spoofed Email Campaigns**
- 🏆 **Cyber Awareness Challenge** (Interactive cybersecurity training and testing engine)

---

## 🏛️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                           AI CYBER SHIELD SYSTEM                                  |
+-----------------------------------------------------------------------------------+
                                      |
         +----------------------------+----------------------------+
         |                                                         |
         v                                                         v
+-----------------------------------+             +----------------------------------+
|      ANDROID CLIENT (Java/XML)    |             |       BACKEND API (Python Flask) |
| - Android Studio Project (Gradle) |  REST/JSON  | - Flask Web Server (Port 5000)   |
| - Clean White + Purple/Blue UI    |<----------->| - Scikit-learn Classifier Models |
| - 4-Tab Bottom Navigation:        |             |   * URL Phishing Model (TF-IDF)  |
|   1. Home (Cards, Banner, Recents)|             |   * SMS Smishing Model (NLP)     |
|   2. History (Filtered Chips)     |             |   * Email Phishing Analyzer      |
|   3. Challenge (3 Levels, Quiz)   |             | - Heuristic Threat Indicators    |
|   4. Profile (Score, Settings)    |             | - Shannon Entropy & TLD Checking |
| - Dedicated Analyzers:            |             | - Actionable Recommendations     |
|   * Link Analyzer                 |             +----------------------------------+
|   * QR Scanner (ZXing / Camera)   |                              ^
|   * SMS Analyzer                  |                              |
|   * Email Analyzer                |                              v
| - Color-Coded Result Screens:     |             +----------------------------------+
|   * SAFE (Emerald, Open Link)     |             |      FIREBASE & LOCAL STORAGE    |
|   * SUSPICIOUS (Amber, Caution)   |             | - Firebase Authentication        |
|   * DANGEROUS (Crimson, Block)    |             | - Cloud Firestore Sync           |
| - Share Sheet Integration         |             | - SQLite / Local Persistence     |
| - Safe In-App Browser Sandbox     |             +----------------------------------+
+-----------------------------------+
```

---

## 🚀 Quick Start Guide

### 1. Run the Python AI/ML Backend

1. Open a terminal / command prompt and navigate to the backend folder:
   ```bash
   cd "c:\final project\backend"
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Re-train the machine learning models:
   ```bash
   python model/train_model.py
   ```

4. Start the Flask REST API server:
   ```bash
   python app.py
   ```
   *The server will start listening at `http://0.0.0.0:5000`.*

5. Verify that the API is running by visiting:
   ```
   http://localhost:5000/
   ```

---

### 2. Open and Run the Android App in Android Studio

1. Launch **Android Studio**.
2. Select **Open** and select the folder:
   ```
   c:\final project\android_app
   ```
3. Allow Gradle to sync dependencies.
4. Run the app on an **Android Emulator** or a **Physical Device**:
   - **For Android Emulator**: The app is pre-configured to communicate with `http://10.0.2.2:5000` automatically.
   - **For Physical Android Phones**: Ensure your phone and computer are on the same Wi-Fi network. In the app, go to **Profile → Backend Server URL** and enter your computer's local IP (e.g. `http://192.168.1.15:5000`). Tap **Test Ping** to verify!

---

## 🧪 Demo Test Cases for College Presentation

### A. Website Link Scenarios
| Type | URL Example | Expected Result | Reason Explained |
| :--- | :--- | :--- | :--- |
| **SAFE** | `https://www.wikipedia.org` | 🟢 **Safe** | Verified authentic domain with legitimate SSL certificate. |
| **SUSPICIOUS** | `http://bit.ly/3x8Qz91` | 🟡 **Suspicious** | Shortened redirection link hiding the real destination. |
| **DANGEROUS** | `http://secure-paypal-login-verification-account.top/login.php` | 🔴 **Dangerous** | Brand spoofing (`paypal`), high-risk `.top` TLD, credential harvesting keywords, unencrypted HTTP. |
| **DANGEROUS** | `http://chase-bank-alert-update-auth.xyz/verify-account` | 🔴 **Dangerous** | Fake Chase bank alert and untrusted `.xyz` domain. |

### B. SMS / Smishing Scenarios
| Type | SMS Text Example | Expected Result |
| :--- | :--- | :--- |
| **SAFE** | `Uber: Your driver John is arriving in a Silver Toyota Camry (ABC-123).` | 🟢 **Safe** |
| **SUSPICIOUS** | `CONGRATULATIONS! You have been selected as the winner of a $1000 Walmart Gift Card! Click http://bit.ly/3x8Qz91 to claim.` | 🟡 **Suspicious** |
| **DANGEROUS** | `URGENT: Your Wells Fargo bank account is suspended due to unusual activity. Click http://wellsfarg0-online-security-token.club to restore access now.` | 🔴 **Dangerous** |

### C. Email Phishing Scenarios
| Type | Sender / Subject | Expected Result |
| :--- | :--- | :--- |
| **SAFE** | `support@github.com` — *Security alert for your repository* | 🟢 **Safe** |
| **DANGEROUS** | `admin@microsoft365-urgent-auth.pw` — *CRITICAL: Password Expiration Notice* | 🔴 **Dangerous** |

---

## 🏆 Cyber Awareness Challenge Feature

The built-in **Cyber Awareness Challenge** allows users to learn and test their cybersecurity knowledge across 3 distinct difficulty tiers:
1. **Beginner**: Safe browsing, basic cyber hygiene, HTTPS awareness.
2. **Intermediate**: Smishing attacks, QR code traps (QRishing), Typosquatting.
3. **Advanced**: Adversary-in-the-Middle (AiTM) phishing, SSL deception, CEO fraud.

**Challenge Flow:**
- Question progress & animated progress bar.
- Immediate visual feedback on answer selection (Green for correct, Red for wrong).
- Detailed "Why this matters" explanation and practical cybersecurity tips.
- Comprehensive Score Summary with Accuracy %, Question Breakdown, and Cyber Awareness Rank.

---

## 🛡️ Security Behavior & Guardrails

- **Dangerous Content Guard**: The application **strictly prevents direct opening of dangerous links**. It presents a prominent warning, details all detected indicators, and provides "Block & Warn" and "Go Back" actions.
- **Safe Content Workflow**: Confirmed safe links can be safely explored through the isolated in-app web preview sandbox or the default browser.
- **Offline Resilience**: If network connectivity to the backend is interrupted, the app's built-in heuristic engine automatically activates so live demonstrations never fail.
- **Android Share Sheet Integration**: Users can share links or messages directly from browsers, SMS, or WhatsApp to AI Cyber Shield for instant threat analysis.

---

## 📁 Repository Structure

```
c:\final project\
├── backend/
│   ├── app.py                      # Flask REST API server
│   ├── requirements.txt            # Python dependencies
│   ├── test_api.py                 # Automated backend test suite
│   ├── dataset/
│   │   ├── urls.csv                # URL phishing dataset
│   │   ├── sms.csv                 # SMS smishing dataset
│   │   └── emails.csv              # Email phishing dataset
│   └── model/
│       ├── feature_extractor.py    # Lexical, structural & NLP heuristics
│       ├── train_model.py          # Scikit-learn training script
│       └── saved/                  # Exported .pkl model files
│
└── android_app/
    ├── build.gradle                # Project-level Gradle build script
    ├── settings.gradle             # Settings configuration
    ├── gradle.properties
    └── app/
        ├── build.gradle            # App-level dependencies (Material 3, ZXing, Retrofit)
        ├── google-services.json    # Firebase configuration template
        └── src/main/
            ├── AndroidManifest.xml # Permissions, activities & share intent filters
            ├── java/com/aicybershield/app/
            │   ├── activities/     # Splash, Login, Main, ScanLink, ScanQr, ScanSms, ScanEmail, Result, Challenge, Score, WebPreview, Settings, About
            │   ├── fragments/      # Home, History, Challenge, Profile
            │   ├── adapters/       # RecentScansAdapter, HistoryAdapter, IndicatorsAdapter
            │   ├── models/         # ScanResult, ScanHistoryItem, ChallengeQuestion, UserProfile, DemoSample
            │   ├── api/            # ApiClient, ApiService, Request DTOs
            │   ├── storage/        # LocalStorageManager (Persistence & Cache)
            │   ├── firebase/       # FirebaseAuthHelper, FirestoreHelper
            │   └── utils/          # Constants, DateUtils, UrlSafetyChecker
            └── res/
                ├── drawable/       # Custom cyber icons, rounded cards, gradient badges
                ├── layout/         # Material XML layouts for all screens
                ├── menu/           # Bottom navigation menu
                ├── values/         # Colors, Strings, Dimens, Themes, Styles
                └── xml/            # Network security cleartext config
```
=======
# Ai_Cyber_Security
A comprehensive research project exploring AI-powered cyber security mechanisms, automated threat detection, and resilient digital defense architectures.
>>>>>>> e8e44acd007b77a0c686fc1d12801d42b7e7674b
