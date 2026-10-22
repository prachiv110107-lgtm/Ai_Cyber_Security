package com.aicybershield.app.api;

import com.google.gson.annotations.SerializedName;

public class UrlRequest {
    @SerializedName("url")
    private String url;

    public UrlRequest(String url) {
        this.url = url;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
