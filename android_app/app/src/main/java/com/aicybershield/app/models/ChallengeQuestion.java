package com.aicybershield.app.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

public class ChallengeQuestion implements Serializable {
    @SerializedName("id")
    private int id;

    @SerializedName("difficulty")
    private String difficulty; // "beginner", "intermediate", "advanced"

    @SerializedName("question")
    private String question;

    @SerializedName("options")
    private List<String> options;

    @SerializedName("correct_index")
    private int correctIndex;

    @SerializedName("explanation")
    private String explanation;

    @SerializedName("tip")
    private String tip;

    public ChallengeQuestion() {}

    public ChallengeQuestion(int id, String difficulty, String question, List<String> options, int correctIndex, String explanation, String tip) {
        this.id = id;
        this.difficulty = difficulty;
        this.question = question;
        this.options = options;
        this.correctIndex = correctIndex;
        this.explanation = explanation;
        this.tip = tip;
    }

    public int getId() {
        return id;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public String getQuestion() {
        return question;
    }

    public List<String> getOptions() {
        return options;
    }

    public int getCorrectIndex() {
        return correctIndex;
    }

    public String getExplanation() {
        return explanation;
    }

    public String getTip() {
        return tip;
    }
}
