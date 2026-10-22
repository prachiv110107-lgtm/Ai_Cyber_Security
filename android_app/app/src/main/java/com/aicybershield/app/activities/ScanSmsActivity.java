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
import com.aicybershield.app.api.SmsRequest;
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

public class ScanSmsActivity extends AppCompatActivity {

    private TextInputEditText etSmsMessage;
    private ProgressBar smsProgressBar;
    private MaterialButton btnAnalyzeSms;
    private LocalStorageManager storageManager;

    private final String[] sampleLabels = {
            "SAFE: Uber Driver Arrival Notification",
            "SUSPICIOUS: $1000 Walmart Gift Card Sweepstakes",
            "DANGEROUS: Wells Fargo Account Suspension Alert & Token Link"
    };

    private final String[] sampleTexts = {
            "Uber: Your driver John is arriving in a Silver Toyota Camry (ABC-123).",
            "CONGRATULATIONS! You have been selected as the winner of a $1000 Walmart Gift Card! Click http://bit.ly/3x8Qz91 to claim.",
            "URGENT: Your Wells Fargo bank account is suspended due to unusual activity. Click http://wellsfarg0-online-security-token.club to restore access now."
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_sms);
        storageManager = LocalStorageManager.getInstance(this);

        ImageView btnBackSms = findViewById(R.id.btnBackSms);
        etSmsMessage = findViewById(R.id.etSmsMessage);
        smsProgressBar = findViewById(R.id.smsProgressBar);
        btnAnalyzeSms = findViewById(R.id.btnAnalyzeSms);
        MaterialButton btnPasteSms = findViewById(R.id.btnPasteSms);
        MaterialButton btnTryDemoSms = findViewById(R.id.btnTryDemoSms);

        btnBackSms.setOnClickListener(v -> finish());

        if (getIntent().hasExtra(Constants.EXTRA_TARGET)) {
            etSmsMessage.setText(getIntent().getStringExtra(Constants.EXTRA_TARGET));
        }

        btnPasteSms.setOnClickListener(v -> pasteFromClipboard());
        btnTryDemoSms.setOnClickListener(v -> showDemoDialog());
        btnAnalyzeSms.setOnClickListener(v -> analyzeSms());
    }

    private void pasteFromClipboard() {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        if (clipboard != null && clipboard.hasPrimaryClip()) {
            ClipData clipData = clipboard.getPrimaryClip();
            if (clipData != null && clipData.getItemCount() > 0) {
                CharSequence text = clipData.getItemAt(0).getText();
                if (text != null) {
                    etSmsMessage.setText(text.toString().trim());
                    Toast.makeText(this, "SMS pasted from clipboard", Toast.LENGTH_SHORT).show();
                    return;
                }
            }
        }
        Toast.makeText(this, "Clipboard is empty", Toast.LENGTH_SHORT).show();
    }

    private void showDemoDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Select Demo SMS Sample")
                .setItems(sampleLabels, (dialog, which) -> {
                    etSmsMessage.setText(sampleTexts[which]);
                })
                .show();
    }

    private void analyzeSms() {
        String msg = etSmsMessage.getText() != null ? etSmsMessage.getText().toString().trim() : "";
        if (TextUtils.isEmpty(msg)) {
            etSmsMessage.setError("Please paste SMS text to analyze");
            return;
        }

        smsProgressBar.setVisibility(View.VISIBLE);
        btnAnalyzeSms.setEnabled(false);

        ApiClient.getApiService(this).predictSms(new SmsRequest(msg)).enqueue(new Callback<ScanResult>() {
            @Override
            public void onResponse(@NonNull Call<ScanResult> call, @NonNull Response<ScanResult> response) {
                smsProgressBar.setVisibility(View.GONE);
                btnAnalyzeSms.setEnabled(true);

                if (response.isSuccessful() && response.body() != null) {
                    handleScanResult(response.body());
                } else {
                    fallbackLocalSmsAnalysis(msg);
                }
            }

            @Override
            public void onFailure(@NonNull Call<ScanResult> call, @NonNull Throwable t) {
                smsProgressBar.setVisibility(View.GONE);
                btnAnalyzeSms.setEnabled(true);
                fallbackLocalSmsAnalysis(msg);
            }
        });
    }

    private void fallbackLocalSmsAnalysis(String msg) {
        ScanResult res = UrlSafetyChecker.evaluateSms(msg);
        handleScanResult(res);
    }

    private void handleScanResult(ScanResult result) {
        ScanHistoryItem historyItem = new ScanHistoryItem(
                String.valueOf(System.currentTimeMillis()),
                Constants.TYPE_SMS,
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
