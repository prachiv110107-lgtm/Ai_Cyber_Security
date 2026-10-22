package com.aicybershield.app.activities;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.api.ApiClient;
import com.aicybershield.app.api.EmailRequest;
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

public class ScanEmailActivity extends AppCompatActivity {

    private TextInputEditText etSender, etSubject, etBody;
    private ProgressBar emailProgressBar;
    private MaterialButton btnAnalyzeEmail;
    private LocalStorageManager storageManager;

    private final String[] sampleLabels = {
            "SAFE: GitHub Dependabot Security Alert",
            "DANGEROUS: Microsoft 365 Password Expiration Spear Phishing",
            "DANGEROUS: Fake PayPal Unauthorized Login Alert"
    };

    private final String[][] sampleEmails = {
            {
                    "support@github.com",
                    "Security alert for your repository",
                    "We noticed a potential security vulnerability in your repository dependencies. Check the Dependabot alerts tab."
            },
            {
                    "admin@microsoft365-urgent-auth.pw",
                    "CRITICAL: Password Expiration Notice",
                    "Dear Employee, Your corporate Microsoft 365 password expires in 2 hours. To maintain access, you must immediately renew your corporate credentials at http://microsoft-office365-urgent-password-reset.pw/auth."
            },
            {
                    "security-alert@paypal-update-center.top",
                    "URGENT: Your account has been suspended!",
                    "Dear Customer, We detected unauthorized logins to your PayPal account. Your funds are temporarily frozen. Verify at http://secure-paypal-login-verification-account.top/login.php."
            }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_email);
        storageManager = LocalStorageManager.getInstance(this);

        ImageView btnBackEmail = findViewById(R.id.btnBackEmail);
        etSender = findViewById(R.id.etSender);
        etSubject = findViewById(R.id.etSubject);
        etBody = findViewById(R.id.etBody);
        emailProgressBar = findViewById(R.id.emailProgressBar);
        btnAnalyzeEmail = findViewById(R.id.btnAnalyzeEmail);
        MaterialButton btnTryDemoEmail = findViewById(R.id.btnTryDemoEmail);

        btnBackEmail.setOnClickListener(v -> finish());
        btnTryDemoEmail.setOnClickListener(v -> showDemoDialog());
        btnAnalyzeEmail.setOnClickListener(v -> analyzeEmail());
    }

    private void showDemoDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Select Demo Email Sample")
                .setItems(sampleLabels, (dialog, which) -> {
                    etSender.setText(sampleEmails[which][0]);
                    etSubject.setText(sampleEmails[which][1]);
                    etBody.setText(sampleEmails[which][2]);
                })
                .show();
    }

    private void analyzeEmail() {
        String sender = etSender.getText() != null ? etSender.getText().toString().trim() : "";
        String subject = etSubject.getText() != null ? etSubject.getText().toString().trim() : "";
        String body = etBody.getText() != null ? etBody.getText().toString().trim() : "";

        if (TextUtils.isEmpty(body) && TextUtils.isEmpty(subject)) {
            etBody.setError("Please enter email body or subject");
            return;
        }

        emailProgressBar.setVisibility(View.VISIBLE);
        btnAnalyzeEmail.setEnabled(false);

        ApiClient.getApiService(this).predictEmail(new EmailRequest(sender, subject, body)).enqueue(new Callback<ScanResult>() {
            @Override
            public void onResponse(@NonNull Call<ScanResult> call, @NonNull Response<ScanResult> response) {
                emailProgressBar.setVisibility(View.GONE);
                btnAnalyzeEmail.setEnabled(true);

                if (response.isSuccessful() && response.body() != null) {
                    handleScanResult(response.body());
                } else {
                    fallbackLocalEmailAnalysis(sender, subject, body);
                }
            }

            @Override
            public void onFailure(@NonNull Call<ScanResult> call, @NonNull Throwable t) {
                emailProgressBar.setVisibility(View.GONE);
                btnAnalyzeEmail.setEnabled(true);
                fallbackLocalEmailAnalysis(sender, subject, body);
            }
        });
    }

    private void fallbackLocalEmailAnalysis(String sender, String subject, String body) {
        ScanResult res = UrlSafetyChecker.evaluateSms(subject + " " + body);
        res.setType(Constants.TYPE_EMAIL);
        res.setTarget("[" + sender + "] " + subject);
        handleScanResult(res);
    }

    private void handleScanResult(ScanResult result) {
        ScanHistoryItem historyItem = new ScanHistoryItem(
                String.valueOf(System.currentTimeMillis()),
                Constants.TYPE_EMAIL,
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
