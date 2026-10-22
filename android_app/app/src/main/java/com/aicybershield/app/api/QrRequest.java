package com.aicybershield.app.api;

import com.google.gson.annotations.SerializedName;

public class QrRequest {
    @SerializedName("qr_data")
    private String qrData;

    public QrRequest(String qrData) {
        this.qrData = qrData;
    }

    public String getQrData() {
        return qrData;
    }

    public void setQrData(String qrData) {
        this.qrData = qrData;
    }
}
