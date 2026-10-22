package com.aicybershield.app;

import android.app.Application;
import com.google.firebase.FirebaseApp;

public class CyberShieldApp extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        try {
            FirebaseApp.initializeApp(this);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
