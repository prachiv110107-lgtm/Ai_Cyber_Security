package com.aicybershield.app.api;

import com.google.gson.annotations.SerializedName;

public class SmsRequest {
    @SerializedName("message")
    private String message;

    public SmsRequest(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
