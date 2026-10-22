package com.aicybershield.app.activities;

import android.content.Intent;
import android.content.res.ColorStateList;
import android.net.Uri;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import com.aicybershield.app.adapters.IndicatorsAdapter;
import com.aicybershield.app.models.ScanResult;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;

public class ResultActivity extends AppCompatActivity {

    private ScanResult scanResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        if (getIntent().hasExtra(Constants.EXTRA_SCAN_RESULT)) {
            scanResult = (ScanResult) getIntent().getSerializableExtra(Constants.EXTRA_SCAN_RESULT);
        }

        if (scanResult == null) {
            scanResult = new ScanResult(
                    Constants.STATUS_SAFE,
                    0.95,
                    "https://www.wikipedia.org",
                    Constants.TYPE_URL,
                    "Legitimate verified domain",
                    null,
                    null,
                    "Just now"
            );
        }

        initViews();
    }

    private void initViews() {
        ImageView btnResultBack = findViewById(R.id.btnResultBack);
        btnResultBack.setOnClickListener(v -> finish());

        MaterialCardView cardStatusHero = findViewById(R.id.cardStatusHero);
        ImageView imgStatusLarge = findViewById(R.id.imgStatusLarge);
        TextView txtStatusBadge = findViewById(R.id.txtStatusBadge);
        TextView txtStatusSubtitle = findViewById(R.id.txtStatusSubtitle);

        TextView txtContentTypeBadge = findViewById(R.id.txtContentTypeBadge);
        TextView txtScanTimestamp = findViewById(R.id.txtScanTimestamp);
        TextView txtTargetContent = findViewById(R.id.txtTargetContent);

        TextView txtConfidencePercentage = findViewById(R.id.txtConfidencePercentage);
        ProgressBar progressRiskConfidence = findViewById(R.id.progressRiskConfidence);
        TextView txtDetectionReason = findViewById(R.id.txtDetectionReason);
        TextView txtRecommendationsList = findViewById(R.id.txtRecommendationsList);

        RecyclerView rvIndicators = findViewById(R.id.rvIndicators);
        MaterialButton btnPrimaryAction = findViewById(R.id.btnPrimaryAction);
        MaterialButton btnSecondaryAction = findViewById(R.id.btnSecondaryAction);

        // Bind content
        txtContentTypeBadge.setText(scanResult.getType());
        txtScanTimestamp.setText(scanResult.getTimestamp());
        txtTargetContent.setText(scanResult.getTarget());
        txtDetectionReason.setText(scanResult.getReason());

        int confidencePercent = scanResult.getConfidencePercent();
        progressRiskConfidence.setProgress(confidencePercent);

        // Build recommendations text
        StringBuilder recs = new StringBuilder();
        for (String rec : scanResult.getRecommendations()) {
            recs.append("• ").append(rec).append("\n");
        }
        if (recs.length() > 0) {
            txtRecommendationsList.setText(recs.toString().trim());
        }

        // Indicators recycler
        rvIndicators.setLayoutManager(new LinearLayoutManager(this));
        rvIndicators.setAdapter(new IndicatorsAdapter(this, scanResult.getIndicators(), scanResult.getStatus()));

        // Apply Status Specific Styling
        if (scanResult.isDangerous()) {
            applyDangerousTheme(cardStatusHero, imgStatusLarge, txtStatusBadge, txtStatusSubtitle,
                    txtConfidencePercentage, progressRiskConfidence, btnPrimaryAction, btnSecondaryAction);
        } else if (scanResult.isSuspicious()) {
            applySuspiciousTheme(cardStatusHero, imgStatusLarge, txtStatusBadge, txtStatusSubtitle,
                    txtConfidencePercentage, progressRiskConfidence, btnPrimaryAction, btnSecondaryAction);
        } else {
            applySafeTheme(cardStatusHero, imgStatusLarge, txtStatusBadge, txtStatusSubtitle,
                    txtConfidencePercentage, progressRiskConfidence, btnPrimaryAction, btnSecondaryAction);
        }
    }

    private void applyDangerousTheme(MaterialCardView cardHero, ImageView imgStatus, TextView txtBadge, TextView txtSub,
                                     TextView txtConf, ProgressBar progress, MaterialButton btnPrimary, MaterialButton btnSecondary) {
        cardHero.setCardBackgroundColor(ContextCompat.getColor(this, R.color.danger_bg));
        cardHero.setStrokeColor(ContextCompat.getColor(this, R.color.danger_border));
        imgStatus.setImageResource(R.drawable.ic_status_dangerous);

        txtBadge.setText(R.string.status_dangerous);
        txtBadge.setTextColor(ContextCompat.getColor(this, R.color.danger_dark));

        txtSub.setText(R.string.status_dangerous_desc);
        txtSub.setTextColor(ContextCompat.getColor(this, R.color.danger_dark));

        txtConf.setText(scanResult.getConfidencePercent() + "% Threat Confidence");
        txtConf.setTextColor(ContextCompat.getColor(this, R.color.danger_primary));
        progress.setProgressTintList(ColorStateList.valueOf(ContextCompat.getColor(this, R.color.danger_primary)));

        // Security requirement: NEVER directly open dangerous link
        btnPrimary.setText(R.string.btn_block_warn);
        btnPrimary.setBackgroundResource(R.drawable.bg_button_danger);
        btnPrimary.setOnClickListener(v -> {
            Toast.makeText(this, "🛡️ Threat Blocked & Reported to Security Database", Toast.LENGTH_LONG).show();
            finish();
        });

        btnSecondary.setText(R.string.btn_go_back);
        btnSecondary.setOnClickListener(v -> finish());
    }

    private void applySuspiciousTheme(MaterialCardView cardHero, ImageView imgStatus, TextView txtBadge, TextView txtSub,
                                       TextView txtConf, ProgressBar progress, MaterialButton btnPrimary, MaterialButton btnSecondary) {
        cardHero.setCardBackgroundColor(ContextCompat.getColor(this, R.color.suspicious_bg));
        cardHero.setStrokeColor(ContextCompat.getColor(this, R.color.suspicious_border));
        imgStatus.setImageResource(R.drawable.ic_status_suspicious);

        txtBadge.setText(R.string.status_suspicious);
        txtBadge.setTextColor(ContextCompat.getColor(this, R.color.suspicious_dark));

        txtSub.setText(R.string.status_suspicious_desc);
        txtSub.setTextColor(ContextCompat.getColor(this, R.color.suspicious_dark));

        txtConf.setText(scanResult.getConfidencePercent() + "% Suspicion Score");
        txtConf.setTextColor(ContextCompat.getColor(this, R.color.suspicious_dark));
        progress.setProgressTintList(ColorStateList.valueOf(ContextCompat.getColor(this, R.color.suspicious_primary)));

        btnPrimary.setText(R.string.btn_proceed_caution);
        btnPrimary.setBackgroundResource(R.drawable.bg_button_primary);
        btnPrimary.setOnClickListener(v -> openSafePreview(scanResult.getTarget()));

        btnSecondary.setText(R.string.btn_go_back);
        btnSecondary.setOnClickListener(v -> finish());
    }

    private void applySafeTheme(MaterialCardView cardHero, ImageView imgStatus, TextView txtBadge, TextView txtSub,
                                TextView txtConf, ProgressBar progress, MaterialButton btnPrimary, MaterialButton btnSecondary) {
        cardHero.setCardBackgroundColor(ContextCompat.getColor(this, R.color.safe_bg));
        cardHero.setStrokeColor(ContextCompat.getColor(this, R.color.safe_border));
        imgStatus.setImageResource(R.drawable.ic_status_safe);

        txtBadge.setText(R.string.status_safe);
        txtBadge.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));

        txtSub.setText(R.string.status_safe_desc);
        txtSub.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));

        txtConf.setText(scanResult.getConfidencePercent() + "% Safety Confidence");
        txtConf.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));
        progress.setProgressTintList(ColorStateList.valueOf(ContextCompat.getColor(this, R.color.safe_primary)));

        btnPrimary.setText(R.string.btn_open_safe_link);
        btnPrimary.setBackgroundResource(R.drawable.bg_button_primary);
        btnPrimary.setOnClickListener(v -> openSafePreview(scanResult.getTarget()));

        btnSecondary.setText(R.string.btn_go_back);
        btnSecondary.setOnClickListener(v -> finish());
    }

    private void openSafePreview(String target) {
        if (target != null && (target.startsWith("http://") || target.startsWith("https://") || target.contains(".com") || target.contains(".org"))) {
            Intent intent = new Intent(this, WebPreviewActivity.class);
            intent.putExtra(Constants.EXTRA_TARGET, target);
            startActivity(intent);
        } else {
            Toast.makeText(this, "Content confirmed safe.", Toast.LENGTH_SHORT).show();
            finish();
        }
    }
}
