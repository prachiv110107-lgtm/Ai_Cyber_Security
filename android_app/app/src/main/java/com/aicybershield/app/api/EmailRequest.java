package com.aicybershield.app.api;

import com.google.gson.annotations.SerializedName;

public class EmailRequest {
    @SerializedName("sender")
    private String sender;

    @SerializedName("subject")
    private String subject;

    @SerializedName("content")
    private String content;

    public EmailRequest(String sender, String subject, String content) {
        this.sender = sender;
        this.subject = subject;
        this.content = content;
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
