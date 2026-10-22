package com.aicybershield.app.models;

import java.io.Serializable;

public class ScanHistoryItem implements Serializable {
    private String id;
    private String type; // "URL", "QR Code", "SMS", "Email"
    private String target;
    private String status; // "safe", "suspicious", "dangerous"
    private String reason;
    private double confidence;
    private String timestamp;
    private ScanResult fullResult;

    public ScanHistoryItem() {}

    public ScanHistoryItem(String id, String type, String target, String status, String reason, double confidence, String timestamp, ScanResult fullResult) {
        this.id = id;
        this.type = type;
        this.target = target;
        this.status = status;
        this.reason = reason;
        this.confidence = confidence;
        this.timestamp = timestamp;
        this.fullResult = fullResult;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getType() {
        return type != null ? type : "URL";
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getTarget() {
        return target != null ? target : "";
    }

    public void setTarget(String target) {
        this.target = target;
    }

    public String getStatus() {
        return status != null ? status.toLowerCase() : "safe";
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getReason() {
        return reason != null ? reason : "";
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getTimestamp() {
        return timestamp != null ? timestamp : "";
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public ScanResult getFullResult() {
        return fullResult;
    }

    public void setFullResult(ScanResult fullResult) {
        this.fullResult = fullResult;
    }
}
