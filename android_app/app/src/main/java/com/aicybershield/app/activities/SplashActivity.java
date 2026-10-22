package com.aicybershield.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.firebase.FirebaseAuthHelper;

public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        ImageView imgShield = findViewById(R.id.imgSplashShield);

        // Subtle glowing shield pulse animation
        AlphaAnimation pulse = new AlphaAnimation(0.6f, 1.0f);
        pulse.setDuration(900);
        pulse.setRepeatMode(Animation.REVERSE);
        pulse.setRepeatCount(Animation.INFINITE);
        imgShield.startAnimation(pulse);

        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            boolean loggedIn = FirebaseAuthHelper.getInstance().isUserLoggedIn();
            Intent intent = new Intent(SplashActivity.this, loggedIn ? MainActivity.class : LoginActivity.class);
            startActivity(intent);
            finish();
        }, 1800);
    }
}
