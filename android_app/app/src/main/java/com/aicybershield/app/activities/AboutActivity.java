package com.aicybershield.app.activities;

import android.os.Bundle;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;

public class AboutActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);

        ImageView btnBackAbout = findViewById(R.id.btnBackAbout);
        btnBackAbout.setOnClickListener(v -> finish());
    }
}
