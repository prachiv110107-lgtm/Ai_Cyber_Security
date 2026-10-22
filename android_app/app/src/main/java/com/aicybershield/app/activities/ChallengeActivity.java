package com.aicybershield.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import com.aicybershield.app.R;
import com.aicybershield.app.firebase.FirestoreHelper;
import com.aicybershield.app.models.ChallengeQuestion;
import com.aicybershield.app.storage.ChallengeRepository;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import java.util.ArrayList;
import java.util.List;

public class ChallengeActivity extends AppCompatActivity {

    private String difficulty = Constants.DIFFICULTY_BEGINNER;
    private List<ChallengeQuestion> questionList = new ArrayList<>();
    private int currentQuestionIndex = 0;
    private int correctScore = 0;
    private int wrongScore = 0;
    private boolean isAnswered = false;

    private TextView txtDifficultyBadge;
    private TextView txtQuestionCount;
    private ProgressBar quizProgressBar;
    private TextView txtQuestionBody;

    private LinearLayout btnOptionA, btnOptionB, btnOptionC, btnOptionD;
    private TextView txtOptionTextA, txtOptionTextB, txtOptionTextC, txtOptionTextD;

    private MaterialCardView cardFeedback;
    private TextView txtFeedbackStatus, txtFeedbackCorrectAnswer, txtFeedbackExplanation, txtFeedbackTip;
    private MaterialButton btnNextQuestion;

    private LocalStorageManager storageManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_challenge);
        storageManager = LocalStorageManager.getInstance(this);

        if (getIntent().hasExtra(Constants.EXTRA_DIFFICULTY)) {
            difficulty = getIntent().getStringExtra(Constants.EXTRA_DIFFICULTY);
        }

        initViews();
        loadQuestions();
    }

    private void initViews() {
        ImageView btnBackChallenge = findViewById(R.id.btnBackChallenge);
        btnBackChallenge.setOnClickListener(v -> finish());

        txtDifficultyBadge = findViewById(R.id.txtDifficultyBadge);
        txtQuestionCount = findViewById(R.id.txtQuestionCount);
        quizProgressBar = findViewById(R.id.quizProgressBar);
        txtQuestionBody = findViewById(R.id.txtQuestionBody);

        btnOptionA = findViewById(R.id.btnOptionA);
        btnOptionB = findViewById(R.id.btnOptionB);
        btnOptionC = findViewById(R.id.btnOptionC);
        btnOptionD = findViewById(R.id.btnOptionD);

        txtOptionTextA = findViewById(R.id.txtOptionTextA);
        txtOptionTextB = findViewById(R.id.txtOptionTextB);
        txtOptionTextC = findViewById(R.id.txtOptionTextC);
        txtOptionTextD = findViewById(R.id.txtOptionTextD);

        cardFeedback = findViewById(R.id.cardFeedback);
        txtFeedbackStatus = findViewById(R.id.txtFeedbackStatus);
        txtFeedbackCorrectAnswer = findViewById(R.id.txtFeedbackCorrectAnswer);
        txtFeedbackExplanation = findViewById(R.id.txtFeedbackExplanation);
        txtFeedbackTip = findViewById(R.id.txtFeedbackTip);
        btnNextQuestion = findViewById(R.id.btnNextQuestion);

        formatDifficultyBadge();
        disableOptionViews();

        btnOptionA.setOnClickListener(v -> checkAnswer(0));
        btnOptionB.setOnClickListener(v -> checkAnswer(1));
        btnOptionC.setOnClickListener(v -> checkAnswer(2));
        btnOptionD.setOnClickListener(v -> checkAnswer(3));

        btnNextQuestion.setOnClickListener(v -> goToNextQuestion());
    }

    private void formatDifficultyBadge() {
        if (txtDifficultyBadge == null) return;
        String title;
        if (Constants.DIFFICULTY_ADVANCED.equalsIgnoreCase(difficulty)) {
            title = "Advanced";
            txtDifficultyBadge.setTextColor(ContextCompat.getColor(this, R.color.danger_dark));
            txtDifficultyBadge.setBackgroundResource(R.drawable.bg_badge_dangerous);
        } else if (Constants.DIFFICULTY_INTERMEDIATE.equalsIgnoreCase(difficulty)) {
            title = "Intermediate";
            txtDifficultyBadge.setTextColor(ContextCompat.getColor(this, R.color.suspicious_dark));
            txtDifficultyBadge.setBackgroundResource(R.drawable.bg_badge_suspicious);
        } else {
            title = "Beginner";
            txtDifficultyBadge.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));
            txtDifficultyBadge.setBackgroundResource(R.drawable.bg_badge_safe);
        }
        txtDifficultyBadge.setText(title);
    }

    private void loadQuestions() {
        ChallengeRepository.getInstance().getChallengeQuestions(this, difficulty, 10, new ChallengeRepository.ChallengeCallback() {
            @Override
            public void onSuccess(List<ChallengeQuestion> questions) {
                if (questions != null && !questions.isEmpty()) {
                    questionList = questions;
                    displayQuestion(0);
                } else {
                    ChallengeRepository.getInstance().loadFromLocalAssets(ChallengeActivity.this, difficulty, 10, new ChallengeRepository.ChallengeCallback() {
                        @Override
                        public void onSuccess(List<ChallengeQuestion> localQuestions) {
                            questionList = localQuestions;
                            displayQuestion(0);
                        }

                        @Override
                        public void onError(String errorMessage, List<ChallengeQuestion> fallbackQuestions) {
                            questionList = fallbackQuestions;
                            displayQuestion(0);
                        }
                    });
                }
            }

            @Override
            public void onError(String errorMessage, List<ChallengeQuestion> fallbackQuestions) {
                questionList = fallbackQuestions;
                displayQuestion(0);
            }
        });
    }

    private void displayQuestion(int index) {
        if (questionList == null || questionList.isEmpty()) {
            return;
        }

        if (index >= questionList.size()) {
            finishChallenge();
            return;
        }

        currentQuestionIndex = index;
        isAnswered = false;

        ChallengeQuestion q = questionList.get(index);
        txtQuestionCount.setText("Question " + (index + 1) + " of " + questionList.size());
        quizProgressBar.setProgress((int) (((float) (index + 1) / questionList.size()) * 100));

        txtQuestionBody.setText(q.getQuestion());

        List<String> options = q.getOptions();
        txtOptionTextA.setText(options.size() > 0 ? options.get(0) : "");
        txtOptionTextB.setText(options.size() > 1 ? options.get(1) : "");
        txtOptionTextC.setText(options.size() > 2 ? options.get(2) : "");
        txtOptionTextD.setText(options.size() > 3 ? options.get(3) : "");

        resetOptionStyles();
        cardFeedback.setVisibility(View.GONE);
        btnNextQuestion.setVisibility(View.GONE);
    }

    private void resetOptionStyles() {
        btnOptionA.setBackgroundResource(R.drawable.bg_button_option_default);
        btnOptionB.setBackgroundResource(R.drawable.bg_button_option_default);
        btnOptionC.setBackgroundResource(R.drawable.bg_button_option_default);
        btnOptionD.setBackgroundResource(R.drawable.bg_button_option_default);

        btnOptionA.setEnabled(true);
        btnOptionB.setEnabled(true);
        btnOptionC.setEnabled(true);
        btnOptionD.setEnabled(true);
    }

    private void disableOptionViews() {
        if (btnOptionA != null) btnOptionA.setEnabled(false);
        if (btnOptionB != null) btnOptionB.setEnabled(false);
        if (btnOptionC != null) btnOptionC.setEnabled(false);
        if (btnOptionD != null) btnOptionD.setEnabled(false);
    }

    private void checkAnswer(int selectedOptionIndex) {
        // Critical safety checks to prevent IndexOutOfBoundsException
        if (questionList == null || questionList.isEmpty() || currentQuestionIndex < 0 || currentQuestionIndex >= questionList.size()) {
            return;
        }

        if (isAnswered) return;
        isAnswered = true;

        // Disable further clicking on options for this question
        disableOptionViews();

        ChallengeQuestion q = questionList.get(currentQuestionIndex);
        int correctIndex = q.getCorrectIndex();

        LinearLayout[] optionViews = {btnOptionA, btnOptionB, btnOptionC, btnOptionD};

        if (selectedOptionIndex == correctIndex) {
            correctScore++;
            if (selectedOptionIndex >= 0 && selectedOptionIndex < optionViews.length) {
                optionViews[selectedOptionIndex].setBackgroundResource(R.drawable.bg_button_option_correct);
            }

            cardFeedback.setCardBackgroundColor(ContextCompat.getColor(this, R.color.safe_bg));
            cardFeedback.setStrokeColor(ContextCompat.getColor(this, R.color.safe_border));
            txtFeedbackStatus.setText("✓ Correct Answer!");
            txtFeedbackStatus.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));

            if (txtFeedbackCorrectAnswer != null) {
                txtFeedbackCorrectAnswer.setVisibility(View.GONE);
            }
        } else {
            wrongScore++;
            if (selectedOptionIndex >= 0 && selectedOptionIndex < optionViews.length) {
                optionViews[selectedOptionIndex].setBackgroundResource(R.drawable.bg_button_option_wrong);
            }
            if (correctIndex >= 0 && correctIndex < optionViews.length) {
                optionViews[correctIndex].setBackgroundResource(R.drawable.bg_button_option_correct);
            }

            cardFeedback.setCardBackgroundColor(ContextCompat.getColor(this, R.color.danger_bg));
            cardFeedback.setStrokeColor(ContextCompat.getColor(this, R.color.danger_border));
            txtFeedbackStatus.setText("✕ Incorrect Answer");
            txtFeedbackStatus.setTextColor(ContextCompat.getColor(this, R.color.danger_dark));

            if (txtFeedbackCorrectAnswer != null) {
                char correctLetter = (char) ('A' + correctIndex);
                String correctText = (correctIndex >= 0 && correctIndex < q.getOptions().size()) ? q.getOptions().get(correctIndex) : "";
                txtFeedbackCorrectAnswer.setText("Correct Answer: Option " + correctLetter + " - " + correctText);
                txtFeedbackCorrectAnswer.setTextColor(ContextCompat.getColor(this, R.color.safe_dark));
                txtFeedbackCorrectAnswer.setVisibility(View.VISIBLE);
            }
        }

        // Show comprehensive explanation & cyber tip in BOTH correct and incorrect cases
        txtFeedbackExplanation.setText(q.getExplanation());
        txtFeedbackTip.setText(q.getTip() != null && q.getTip().startsWith("💡") ? q.getTip() : "💡 Cyber Tip: " + q.getTip());

        cardFeedback.setVisibility(View.VISIBLE);
        btnNextQuestion.setVisibility(View.VISIBLE);

        if (currentQuestionIndex == questionList.size() - 1) {
            btnNextQuestion.setText(R.string.btn_finish_quiz);
        } else {
            btnNextQuestion.setText(R.string.btn_next_question);
        }
    }

    private void goToNextQuestion() {
        displayQuestion(currentQuestionIndex + 1);
    }

    private void finishChallenge() {
        int total = questionList.size();
        int finalScorePercent = (int) Math.round(((double) correctScore / (total > 0 ? total : 1)) * 100);

        storageManager.incrementChallengesCompleted();
        storageManager.updateAwarenessScore(finalScorePercent);
        FirestoreHelper.getInstance().updateChallengeScore(storageManager.getUserProfile().getEmail(), finalScorePercent);

        Intent intent = new Intent(this, ScoreActivity.class);
        intent.putExtra(Constants.EXTRA_TOTAL, total);
        intent.putExtra(Constants.EXTRA_CORRECT, correctScore);
        intent.putExtra(Constants.EXTRA_WRONG, wrongScore);
        intent.putExtra(Constants.EXTRA_SCORE, finalScorePercent);
        intent.putExtra(Constants.EXTRA_DIFFICULTY, difficulty);
        startActivity(intent);
        finish();
    }
}
