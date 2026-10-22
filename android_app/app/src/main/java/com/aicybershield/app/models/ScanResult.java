package com.aicybershield.app.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class ScanResult implements Serializable {
    @SerializedName("status")
    private String status; // "safe", "suspicious", "dangerous"

    @SerializedName("confidence")
    private double confidence;

    @SerializedName("target")
    private String target;

    @SerializedName("type")
    private String type; // "URL", "SMS", "EMAIL", "QR Code"

    @SerializedName("reason")
    private String reason;

    @SerializedName("indicators")
    private List<String> indicators;

    @SerializedName("recommendations")
    private List<String> recommendations;

    @SerializedName("timestamp")
    private String timestamp;

    public ScanResult() {
        this.indicators = new ArrayList<>();
        this.recommendations = new ArrayList<>();
    }

    public ScanResult(String status, double confidence, String target, String type, String reason, List<String> indicators, List<String> recommendations, String timestamp) {
        this.status = status;
        this.confidence = confidence;
        this.target = target;
        this.type = type;
        this.reason = reason;
        this.indicators = indicators != null ? indicators : new ArrayList<>();
        this.recommendations = recommendations != null ? recommendations : new ArrayList<>();
        this.timestamp = timestamp;
    }

    public String getStatus() {
        return status != null ? status.toLowerCase() : "safe";
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public double getConfidence() {
        return confidence;
    }

    public int getConfidencePercent() {
        return (int) Math.round(confidence * 100);
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getTarget() {
        return target != null ? target : "";
    }

    public void setTarget(String target) {
        this.target = target;
    }

    public String getType() {
        return type != null ? type : "URL";
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getReason() {
        return reason != null ? reason : "Analysis completed successfully.";
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public List<String> getIndicators() {
        return indicators != null ? indicators : new ArrayList<>();
    }

    public void setIndicators(List<String> indicators) {
        this.indicators = indicators;
    }

    public List<String> getRecommendations() {
        return recommendations != null ? recommendations : new ArrayList<>();
    }

    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }

    public String getTimestamp() {
        return timestamp != null ? timestamp : "";
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public boolean isSafe() {
        return "safe".equalsIgnoreCase(status);
    }

    public boolean isSuspicious() {
        return "suspicious".equalsIgnoreCase(status);
    }

    public boolean isDangerous() {
        return "dangerous".equalsIgnoreCase(status);
    }
}
