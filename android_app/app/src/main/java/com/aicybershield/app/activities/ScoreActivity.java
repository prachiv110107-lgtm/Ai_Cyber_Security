package com.aicybershield.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.button.MaterialButton;

public class ScoreActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_score);

        int total = getIntent().getIntExtra(Constants.EXTRA_TOTAL, 10);
        int correct = getIntent().getIntExtra(Constants.EXTRA_CORRECT, 0);
        int wrong = getIntent().getIntExtra(Constants.EXTRA_WRONG, 0);
        String difficulty = getIntent().getStringExtra(Constants.EXTRA_DIFFICULTY);
        int percentage = (int) Math.round(((double) correct / (total > 0 ? total : 1)) * 100);

        TextView txtScoreFraction = findViewById(R.id.txtScoreFraction);
        TextView txtPercentageBadge = findViewById(R.id.txtPercentageBadge);
        TextView txtCorrectCount = findViewById(R.id.txtCorrectCount);
        TextView txtWrongCount = findViewById(R.id.txtWrongCount);
        MaterialButton btnBackHome = findViewById(R.id.btnBackHome);

        txtScoreFraction.setText(correct + " / " + total);
        txtCorrectCount.setText(String.valueOf(correct));
        txtWrongCount.setText(String.valueOf(wrong));

        String rank;
        if (percentage >= 85) {
            rank = "Cyber Guardian";
        } else if (percentage >= 60) {
            rank = "Security Specialist";
        } else {
            rank = "Cyber Apprentice";
        }

        String diffLabel = difficulty != null && !difficulty.isEmpty() 
                ? (difficulty.substring(0, 1).toUpperCase() + difficulty.substring(1).toLowerCase()) 
                : "Standard";

        txtPercentageBadge.setText(percentage + "% Accuracy • " + diffLabel + " (" + rank + ")");

        btnBackHome.setOnClickListener(v -> {
            Intent intent = new Intent(ScoreActivity.this, MainActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            startActivity(intent);
            finish();
        });
    }
}
