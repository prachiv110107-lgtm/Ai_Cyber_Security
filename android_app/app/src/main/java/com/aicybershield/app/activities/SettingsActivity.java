package com.aicybershield.app.activities;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import com.aicybershield.app.R;
import com.aicybershield.app.api.ApiClient;
import com.aicybershield.app.storage.LocalStorageManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.switchmaterial.SwitchMaterial;
import com.google.android.material.textfield.TextInputEditText;
import java.util.Map;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SettingsActivity extends AppCompatActivity {

    private TextInputEditText etServerUrl;
    private TextView txtConnectionStatus;
    private LocalStorageManager storageManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        storageManager = LocalStorageManager.getInstance(this);

        ImageView btnBackSettings = findViewById(R.id.btnBackSettings);
        etServerUrl = findViewById(R.id.etServerUrl);
        txtConnectionStatus = findViewById(R.id.txtConnectionStatus);
        MaterialButton btnTestConnection = findViewById(R.id.btnTestConnection);
        MaterialButton btnSaveServerUrl = findViewById(R.id.btnSaveServerUrl);
        SwitchMaterial switchOfflineResilience = findViewById(R.id.switchOfflineResilience);

        btnBackSettings.setOnClickListener(v -> finish());

        etServerUrl.setText(storageManager.getServerBaseUrl());
        switchOfflineResilience.setChecked(storageManager.isOfflineResilienceEnabled());

        switchOfflineResilience.setOnCheckedChangeListener((buttonView, isChecked) -> {
            storageManager.setOfflineResilience(isChecked);
            Toast.makeText(this, isChecked ? "Offline Resilience Enabled" : "Offline Resilience Disabled", Toast.LENGTH_SHORT).show();
        });

        btnSaveServerUrl.setOnClickListener(v -> saveServerUrl());
        btnTestConnection.setOnClickListener(v -> testConnection());
    }

    private void saveServerUrl() {
        String url = etServerUrl.getText() != null ? etServerUrl.getText().toString().trim() : "";
        if (TextUtils.isEmpty(url)) {
            etServerUrl.setError("Please enter server URL");
            return;
        }
        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "http://" + url;
        }
        storageManager.setServerBaseUrl(url);
        Toast.makeText(this, "Backend server URL saved!", Toast.LENGTH_SHORT).show();
    }

    private void testConnection() {
        saveServerUrl();
        txtConnectionStatus.setVisibility(View.VISIBLE);
        txtConnectionStatus.setText("Testing connection to backend...");
        txtConnectionStatus.setTextColor(ContextCompat.getColor(this, R.color.text_secondary));

        ApiClient.getApiService(this).checkHealth().enqueue(new Callback<Map<String, Object>>() {
            @Override
            public void onResponse(@NonNull Call<Map<String, Object>> call, @NonNull Response<Map<String, Object>> response) {
                if (response.isSuccessful()) {
                    txtConnectionStatus.setText("✓ Connected! AI Cyber Shield Backend is Online.");
                    txtConnectionStatus.setTextColor(ContextCompat.getColor(SettingsActivity.this, R.color.safe_dark));
                } else {
                    txtConnectionStatus.setText("✕ Server returned error " + response.code());
                    txtConnectionStatus.setTextColor(ContextCompat.getColor(SettingsActivity.this, R.color.danger_dark));
                }
            }

            @Override
            public void onFailure(@NonNull Call<Map<String, Object>> call, @NonNull Throwable t) {
                txtConnectionStatus.setText("✕ Connection failed. Fallback heuristic engine is ready.");
                txtConnectionStatus.setTextColor(ContextCompat.getColor(SettingsActivity.this, R.color.suspicious_dark));
            }
        });
    }
}
