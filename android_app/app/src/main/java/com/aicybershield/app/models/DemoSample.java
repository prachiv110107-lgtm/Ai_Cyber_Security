package com.aicybershield.app.models;

public class DemoSample {
    private String label;
    private String status;
    private String value;
    private String sender;
    private String subject;
    private String content;

    public DemoSample(String label, String status, String value) {
        this.label = label;
        this.status = status;
        this.value = value;
    }

    public DemoSample(String label, String status, String sender, String subject, String content) {
        this.label = label;
        this.status = status;
        this.sender = sender;
        this.subject = subject;
        this.content = content;
    }

    public String getLabel() {
        return label;
    }

    public String getStatus() {
        return status;
    }

    public String getValue() {
        return value;
    }

    public String getSender() {
        return sender;
    }

    public String getSubject() {
        return subject;
    }

    public String getContent() {
        return content;
    }
}
