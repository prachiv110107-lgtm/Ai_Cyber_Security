package com.aicybershield.app.activities;

import android.app.AlertDialog;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.api.ApiClient;
import com.aicybershield.app.api.UrlRequest;
import com.aicybershield.app.firebase.FirestoreHelper;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.models.ScanResult;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.aicybershield.app.utils.DateUtils;
import com.aicybershield.app.utils.UrlSafetyChecker;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ScanLinkActivity extends AppCompatActivity {

    private TextInputEditText etUrl;
    private ProgressBar progressBar;
    private MaterialButton btnAnalyzeUrl;
    private LocalStorageManager storageManager;

    private final String[] sampleLabels = {
            "SAFE: Wikipedia Article (https://www.wikipedia.org)",
            "SUSPICIOUS: Shortened Redirection Link (http://bit.ly/3x8Qz91)",
            "DANGEROUS: Fake PayPal Verification Portal (http://secure-paypal-login-verification-account.top/login.php)",
            "DANGEROUS: Chase Bank Security Alert Spoof (http://chase-bank-alert-update-auth.xyz/verify-account)"
    };

    private final String[] sampleUrls = {
            "https://www.wikipedia.org",
            "http://bit.ly/3x8Qz91",
            "http://secure-paypal-login-verification-account.top/login.php",
            "http://chase-bank-alert-update-auth.xyz/verify-account"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_link);
        storageManager = LocalStorageManager.getInstance(this);

        ImageView btnBack = findViewById(R.id.btnBack);
        etUrl = findViewById(R.id.etUrl);
        progressBar = findViewById(R.id.progressBar);
        btnAnalyzeUrl = findViewById(R.id.btnAnalyzeUrl);
        MaterialButton btnPasteClipboard = findViewById(R.id.btnPasteClipboard);
        MaterialButton btnTryDemoSamples = findViewById(R.id.btnTryDemoSamples);

        btnBack.setOnClickListener(v -> finish());

        // Check if intent passed a shared URL
        if (getIntent().hasExtra(Constants.EXTRA_TARGET)) {
            String target = getIntent().getStringExtra(Constants.EXTRA_TARGET);
            etUrl.setText(target);
        }

        btnPasteClipboard.setOnClickListener(v -> pasteFromClipboard());
        btnTryDemoSamples.setOnClickListener(v -> showSampleDialog());
        btnAnalyzeUrl.setOnClickListener(v -> analyzeUrl());
    }

    private void pasteFromClipboard() {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        if (clipboard != null && clipboard.hasPrimaryClip()) {
            ClipData clipData = clipboard.getPrimaryClip();
            if (clipData != null && clipData.getItemCount() > 0) {
                CharSequence text = clipData.getItemAt(0).getText();
                if (text != null) {
                    etUrl.setText(text.toString().trim());
                    Toast.makeText(this, "URL pasted from clipboard", Toast.LENGTH_SHORT).show();
                    return;
                }
            }
        }
        Toast.makeText(this, "Clipboard is empty", Toast.LENGTH_SHORT).show();
    }

    private void showSampleDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Select Demo URL Sample")
                .setItems(sampleLabels, (dialog, which) -> {
                    etUrl.setText(sampleUrls[which]);
                })
                .show();
    }

    private void analyzeUrl() {
        String url = etUrl.getText() != null ? etUrl.getText().toString().trim() : "";
        if (TextUtils.isEmpty(url)) {
            etUrl.setError("Please enter or paste a URL to analyze");
            return;
        }

        progressBar.setVisibility(View.VISIBLE);
        btnAnalyzeUrl.setEnabled(false);

        ApiClient.getApiService(this).predictUrl(new UrlRequest(url)).enqueue(new Callback<ScanResult>() {
            @Override
            public void onResponse(@NonNull Call<ScanResult> call, @NonNull Response<ScanResult> response) {
                progressBar.setVisibility(View.GONE);
                btnAnalyzeUrl.setEnabled(true);

                if (response.isSuccessful() && response.body() != null) {
                    handleScanResult(response.body());
                } else {
                    fallbackLocalAnalysis(url);
                }
            }

            @Override
            public void onFailure(@NonNull Call<ScanResult> call, @NonNull Throwable t) {
                progressBar.setVisibility(View.GONE);
                btnAnalyzeUrl.setEnabled(true);
                fallbackLocalAnalysis(url);
            }
        });
    }

    private void fallbackLocalAnalysis(String url) {
        ScanResult localResult = UrlSafetyChecker.evaluateUrl(url);
        handleScanResult(localResult);
    }

    private void handleScanResult(ScanResult result) {
        ScanHistoryItem historyItem = new ScanHistoryItem(
                String.valueOf(System.currentTimeMillis()),
                Constants.TYPE_URL,
                result.getTarget(),
                result.getStatus(),
                result.getReason(),
                result.getConfidence(),
                DateUtils.getCurrentDateTime(),
                result
        );

        storageManager.addScanHistoryItem(historyItem);
        FirestoreHelper.getInstance().syncScanResult(storageManager.getUserProfile().getEmail(), historyItem);

        Intent intent = new Intent(this, ResultActivity.class);
        intent.putExtra(Constants.EXTRA_SCAN_RESULT, result);
        startActivity(intent);
    }
}
