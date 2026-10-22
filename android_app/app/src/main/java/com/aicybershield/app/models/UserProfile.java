package com.aicybershield.app.models;

import java.io.Serializable;

public class UserProfile implements Serializable {
    private String uid;
    private String name;
    private String email;
    private int awarenessScore; // 0 - 100
    private int challengesCompleted;
    private int totalScans;

    public UserProfile() {
        this.awarenessScore = 75;
        this.challengesCompleted = 0;
        this.totalScans = 0;
    }

    public UserProfile(String uid, String name, String email, int awarenessScore, int challengesCompleted, int totalScans) {
        this.uid = uid;
        this.name = name;
        this.email = email;
        this.awarenessScore = awarenessScore;
        this.challengesCompleted = challengesCompleted;
        this.totalScans = totalScans;
    }

    public String getUid() {
        return uid;
    }

    public void setUid(String uid) {
        this.uid = uid;
    }

    public String getName() {
        return name != null ? name : "Cyber Defender";
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email != null ? email : "user@aicybershield.org";
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getAwarenessScore() {
        return awarenessScore;
    }

    public void setAwarenessScore(int awarenessScore) {
        this.awarenessScore = Math.max(0, Math.min(100, awarenessScore));
    }

    public int getChallengesCompleted() {
        return challengesCompleted;
    }

    public void setChallengesCompleted(int challengesCompleted) {
        this.challengesCompleted = challengesCompleted;
    }

    public int getTotalScans() {
        return totalScans;
    }

    public void setTotalScans(int totalScans) {
        this.totalScans = totalScans;
    }

    public String getRankLevel() {
        if (awarenessScore >= 90) return "Cyber Guardian (Level 3)";
        if (awarenessScore >= 75) return "Security Specialist (Level 2)";
        return "Cyber Apprentice (Level 1)";
    }
}
