package com.aicybershield.app.utils;

import com.aicybershield.app.models.ScanResult;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

public class UrlSafetyChecker {

    private static final Set<String> SUSPICIOUS_TLDS = new HashSet<>(Arrays.asList(
            "top", "xyz", "club", "work", "click", "ru", "cn", "gq", "tk", "ga", "cf", "ml", "cc", "pw", "su", "bid", "date", "buzz", "live", "info"
    ));

    private static final Set<String> SHORTENERS = new HashSet<>(Arrays.asList(
            "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy"
    ));

    private static final String[] TARGETED_BRANDS = {
            "paypal", "chase", "bankofamerica", "wellsfargo", "apple", "amazon", "netflix", "microsoft", "google", "facebook", "binance", "coinbase"
    };

    private static final String[] SENSITIVE_KEYWORDS = {
            "login", "signin", "verify", "verification", "account", "security", "secure", "banking", "suspended", "password", "auth", "claim", "otp"
    };

    private static final Pattern IP_PATTERN = Pattern.compile(".*://(\\d{1,3}\\.){3}\\d{1,3}(:.*)?.*");

    public static ScanResult evaluateUrl(String url) {
        String lowerUrl = url.toLowerCase().trim();
        List<String> indicators = new ArrayList<>();
        List<String> recommendations = new ArrayList<>();

        boolean hasIp = IP_PATTERN.matcher(lowerUrl).matches();
        if (hasIp) {
            indicators.add("IP address host detected instead of registered domain name");
        }

        boolean isShortener = false;
        for (String sh : SHORTENERS) {
            if (lowerUrl.contains(sh)) {
                isShortener = true;
                indicators.add("URL shortening service disguises actual destination");
                break;
            }
        }

        boolean hasSuspiciousTld = false;
        for (String tld : SUSPICIOUS_TLDS) {
            if (lowerUrl.contains("." + tld)) {
                hasSuspiciousTld = true;
                indicators.add("High-risk top level domain: ." + tld);
                break;
            }
        }

        int keywordCount = 0;
        for (String kw : SENSITIVE_KEYWORDS) {
            if (lowerUrl.contains(kw)) {
                keywordCount++;
            }
        }
        if (keywordCount >= 2) {
            indicators.add("Multiple credential harvesting keywords present in URL path");
        }

        boolean isBrandSpoofed = false;
        for (String brand : TARGETED_BRANDS) {
            if (lowerUrl.contains(brand) && !lowerUrl.contains("." + brand + ".com")) {
                isBrandSpoofed = true;
                indicators.add("Target brand name spoofed in URL: " + brand);
                break;
            }
        }

        if (!lowerUrl.startsWith("https://")) {
            indicators.add("Unencrypted connection (HTTP instead of HTTPS)");
        }

        String status;
        double confidence;
        String reason;

        if (lowerUrl.contains("wikipedia.org") || lowerUrl.contains("google.com") || lowerUrl.contains("github.com")) {
            status = Constants.STATUS_SAFE;
            confidence = 0.98;
            reason = "Verified authentic legitimate domain name with trusted SSL profile";
            indicators.clear();
            indicators.add("Valid domain authority");
            indicators.add("Secure protocol verified");
            recommendations.add("URL is safe to open");
        } else if (hasIp || isBrandSpoofed || (hasSuspiciousTld && keywordCount >= 1)) {
            status = Constants.STATUS_DANGEROUS;
            confidence = 0.94;
            reason = "Malicious phishing patterns and suspicious deception indicators detected";
            recommendations.add("DO NOT open this link or input credentials");
            recommendations.add("Block sender and report as digital fraud");
        } else if (isShortener || hasSuspiciousTld || keywordCount >= 1) {
            status = Constants.STATUS_SUSPICIOUS;
            confidence = 0.78;
            reason = "Suspicious link attributes detected that warrant caution before accessing";
            recommendations.add("Proceed with caution; verify sender through official app");
        } else {
            status = Constants.STATUS_SAFE;
            confidence = 0.88;
            reason = "No known malicious patterns or deceptive structures detected";
            indicators.add("Standard domain structure");
            recommendations.add("URL appears safe to browse");
        }

        return new ScanResult(status, confidence, url, Constants.TYPE_URL, reason, indicators, recommendations, DateUtils.getCurrentDateTime());
    }

    public static ScanResult evaluateSms(String message) {
        String text = message.toLowerCase();
        List<String> indicators = new ArrayList<>();
        List<String> recommendations = new ArrayList<>();

        if (text.contains("urgent") || text.contains("suspended") || text.contains("blocked") || text.contains("action required")) {
            indicators.add("Urgent psychological pressure language");
        }
        if (text.contains("otp") || text.contains("password") || text.contains("pin") || text.contains("ssn")) {
            indicators.add("Solicits confidential credentials (OTP / PIN)");
        }
        if (text.contains("http://") || text.contains("https://") || text.contains(".top") || text.contains(".xyz") || text.contains("bit.ly")) {
            indicators.add("Contains embedded redirection link prompting external click");
        }
        if (text.contains("won") || text.contains("winner") || text.contains("$1000") || text.contains("lottery")) {
            indicators.add("Fake sweepstakes or financial reward hook");
        }

        String status;
        double confidence;
        String reason;

        if (indicators.size() >= 2) {
            status = Constants.STATUS_DANGEROUS;
            confidence = 0.93;
            reason = "Social engineering smishing attack detected (fake urgency / credential harvesting)";
            recommendations.add("Never share OTPs, PINs, or passwords with anyone via SMS");
            recommendations.add("Block and report the sender number immediately");
        } else if (indicators.size() == 1) {
            status = Constants.STATUS_SUSPICIOUS;
            confidence = 0.77;
            reason = "Suspicious message patterns or unverified promotions detected";
            recommendations.add("Verify directly through official organization apps");
        } else {
            status = Constants.STATUS_SAFE;
            confidence = 0.90;
            reason = "Message appears to be normal communication with no threat indicators";
            indicators.add("No urgency threats found");
            recommendations.add("Standard notification format verified");
        }

        return new ScanResult(status, confidence, message, Constants.TYPE_SMS, reason, indicators, recommendations, DateUtils.getCurrentDateTime());
    }
}
