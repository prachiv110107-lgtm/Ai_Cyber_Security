package com.aicybershield.app.fragments;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import com.aicybershield.app.R;
import com.aicybershield.app.activities.ChallengeActivity;
import com.aicybershield.app.storage.ChallengeRepository;
import com.aicybershield.app.models.UserProfile;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;

public class ChallengeFragment extends Fragment {

    private String selectedDifficulty = Constants.DIFFICULTY_BEGINNER;
    private RadioButton radioBeginner, radioIntermediate, radioAdvanced;
    private MaterialCardView cardBeginner, cardIntermediate, cardAdvanced;
    private TextView txtStatTotalQuestions, txtStatCompleted, txtStatScore;
    private MaterialButton btnStartChallenge;
    private LocalStorageManager storageManager;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_challenge, container, false);
        storageManager = LocalStorageManager.getInstance(requireContext());

        initViews(view);
        loadStats();
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        loadStats();
    }

    private void initViews(View view) {
        txtStatTotalQuestions = view.findViewById(R.id.txtStatTotalQuestions);
        txtStatCompleted = view.findViewById(R.id.txtStatCompleted);
        txtStatScore = view.findViewById(R.id.txtStatScore);

        cardBeginner = view.findViewById(R.id.cardBeginner);
        cardIntermediate = view.findViewById(R.id.cardIntermediate);
        cardAdvanced = view.findViewById(R.id.cardAdvanced);

        radioBeginner = view.findViewById(R.id.radioBeginner);
        radioIntermediate = view.findViewById(R.id.radioIntermediate);
        radioAdvanced = view.findViewById(R.id.radioAdvanced);

        btnStartChallenge = view.findViewById(R.id.btnStartChallenge);

        cardBeginner.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_BEGINNER));
        cardIntermediate.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_INTERMEDIATE));
        cardAdvanced.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_ADVANCED));

        radioBeginner.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_BEGINNER));
        radioIntermediate.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_INTERMEDIATE));
        radioAdvanced.setOnClickListener(v -> selectDifficulty(Constants.DIFFICULTY_ADVANCED));

        btnStartChallenge.setOnClickListener(v -> {
            Intent intent = new Intent(requireContext(), ChallengeActivity.class);
            intent.putExtra(Constants.EXTRA_DIFFICULTY, selectedDifficulty);
            startActivity(intent);
        });

        // Default selection
        selectDifficulty(Constants.DIFFICULTY_BEGINNER);
    }

    private void selectDifficulty(String difficulty) {
        this.selectedDifficulty = difficulty;
        if (!isAdded()) return;

        boolean isBeg = Constants.DIFFICULTY_BEGINNER.equalsIgnoreCase(difficulty);
        boolean isInt = Constants.DIFFICULTY_INTERMEDIATE.equalsIgnoreCase(difficulty);
        boolean isAdv = Constants.DIFFICULTY_ADVANCED.equalsIgnoreCase(difficulty);

        radioBeginner.setChecked(isBeg);
        radioIntermediate.setChecked(isInt);
        radioAdvanced.setChecked(isAdv);

        int colorStrokeDefault = ContextCompat.getColor(requireContext(), R.color.card_stroke);
        int colorBeg = ContextCompat.getColor(requireContext(), R.color.beginner_primary);
        int colorInt = ContextCompat.getColor(requireContext(), R.color.intermediate_primary);
        int colorAdv = ContextCompat.getColor(requireContext(), R.color.advanced_primary);

        cardBeginner.setStrokeColor(isBeg ? colorBeg : colorStrokeDefault);
        cardBeginner.setStrokeWidth(isBeg ? 6 : 2);

        cardIntermediate.setStrokeColor(isInt ? colorInt : colorStrokeDefault);
        cardIntermediate.setStrokeWidth(isInt ? 6 : 2);

        cardAdvanced.setStrokeColor(isAdv ? colorAdv : colorStrokeDefault);
        cardAdvanced.setStrokeWidth(isAdv ? 6 : 2);

        String levelLabel = isBeg ? "Beginner" : (isInt ? "Intermediate" : "Advanced");
        btnStartChallenge.setText("Start " + levelLabel + " Quiz (10 Qs) 🚀");
    }

    private void loadStats() {
        if (!isAdded()) return;
        UserProfile profile = storageManager.getUserProfile();
        
        int totalQuestions = ChallengeRepository.getInstance().getTotalQuestionsCount(requireContext());
        if (totalQuestions <= 0) totalQuestions = 300;
        
        txtStatTotalQuestions.setText(String.valueOf(totalQuestions));
        txtStatCompleted.setText(String.valueOf(profile.getChallengesCompleted()));
        txtStatScore.setText(profile.getAwarenessScore() + "%");
    }
}
