package com.aicybershield.app.storage;

import android.content.Context;
import android.content.SharedPreferences;
import com.aicybershield.app.firebase.FirestoreHelper;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.models.UserProfile;
import com.aicybershield.app.utils.Constants;
import com.aicybershield.app.utils.DateUtils;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class LocalStorageManager {
    private static LocalStorageManager instance;
    private final SharedPreferences prefs;
    private final Gson gson;
    private static final String KEY_HISTORY = "key_scan_history";

    private LocalStorageManager(Context context) {
        prefs = context.getApplicationContext().getSharedPreferences(Constants.PREF_NAME, Context.MODE_PRIVATE);
        gson = new Gson();
    }

    public static synchronized LocalStorageManager getInstance(Context context) {
        if (instance == null) {
            instance = new LocalStorageManager(context);
        }
        return instance;
    }

    public void resetForNewUser(String name, String email) {
        clearHistory();
        setChallengesCompleted(0);
        clearAllSeenQuestionIds();
        saveUserProfile(name, email, 0);
    }

    public void addScanHistoryItem(ScanHistoryItem item) {
        List<ScanHistoryItem> list = getScanHistory();
        list.add(0, item); // Add to top of recent list
        saveHistoryList(list);

        // Realtime sync to Cloud Firestore
        try {
            UserProfile user = getUserProfile();
            String email = (user != null && user.getEmail() != null) ? user.getEmail() : "demo_user";
            FirestoreHelper.getInstance().syncScanResult(email, item);
        } catch (Exception ignored) {}
    }

    public List<ScanHistoryItem> getScanHistory() {
        String json = prefs.getString(KEY_HISTORY, null);
        if (json == null) return new ArrayList<>();
        Type type = new TypeToken<List<ScanHistoryItem>>() {}.getType();
        try {
            return gson.fromJson(json, type);
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }

    public void clearHistory() {
        saveHistoryList(new ArrayList<>());
    }

    private void saveHistoryList(List<ScanHistoryItem> list) {
        prefs.edit().putString(KEY_HISTORY, gson.toJson(list)).apply();
    }

    public String getServerBaseUrl() {
        return prefs.getString(Constants.KEY_SERVER_URL, Constants.DEFAULT_SERVER_URL);
    }

    public void setServerBaseUrl(String url) {
        prefs.edit().putString(Constants.KEY_SERVER_URL, url).apply();
    }

    public UserProfile getUserProfile() {
        String name = prefs.getString(Constants.KEY_USER_NAME, "New User");
        String email = prefs.getString(Constants.KEY_USER_EMAIL, "");
        int score = prefs.getInt(Constants.KEY_AWARENESS_SCORE, 0);
        int challenges = prefs.getInt(Constants.KEY_CHALLENGES_COMPLETED, 0);
        return new UserProfile("local_uid", name, email, score, challenges, getScanHistory().size());
    }

    public void saveUserProfile(String name, String email, int awarenessScore) {
        prefs.edit()
                .putString(Constants.KEY_USER_NAME, name)
                .putString(Constants.KEY_USER_EMAIL, email)
                .putInt(Constants.KEY_AWARENESS_SCORE, awarenessScore)
                .apply();
    }

    public void updateAwarenessScore(int score) {
        prefs.edit().putInt(Constants.KEY_AWARENESS_SCORE, score).apply();
    }

    public int getChallengesCompleted() {
        return prefs.getInt(Constants.KEY_CHALLENGES_COMPLETED, 0);
    }

    public void incrementChallengesCompleted() {
        int current = getChallengesCompleted();
        prefs.edit().putInt(Constants.KEY_CHALLENGES_COMPLETED, current + 1).apply();
    }

    public void setChallengesCompleted(int count) {
        prefs.edit().putInt(Constants.KEY_CHALLENGES_COMPLETED, Math.max(0, count)).apply();
    }

    public java.util.Set<Integer> getSeenQuestionIds(String difficulty) {
        String key = Constants.KEY_SEEN_QUESTIONS_PREFIX + (difficulty != null ? difficulty.toLowerCase() : "all");
        String json = prefs.getString(key, null);
        if (json == null) return new java.util.HashSet<>();
        Type type = new TypeToken<java.util.Set<Integer>>() {}.getType();
        try {
            java.util.Set<Integer> set = gson.fromJson(json, type);
            return set != null ? set : new java.util.HashSet<>();
        } catch (Exception e) {
            return new java.util.HashSet<>();
        }
    }

    public void addSeenQuestionIds(String difficulty, List<Integer> ids) {
        if (ids == null || ids.isEmpty()) return;
        String key = Constants.KEY_SEEN_QUESTIONS_PREFIX + (difficulty != null ? difficulty.toLowerCase() : "all");
        java.util.Set<Integer> existing = getSeenQuestionIds(difficulty);
        existing.addAll(ids);
        prefs.edit().putString(key, gson.toJson(existing)).apply();
    }

    public void clearSeenQuestionIds(String difficulty) {
        String key = Constants.KEY_SEEN_QUESTIONS_PREFIX + (difficulty != null ? difficulty.toLowerCase() : "all");
        prefs.edit().remove(key).apply();
    }

    public void clearAllSeenQuestionIds() {
        clearSeenQuestionIds(Constants.DIFFICULTY_BEGINNER);
        clearSeenQuestionIds(Constants.DIFFICULTY_INTERMEDIATE);
        clearSeenQuestionIds(Constants.DIFFICULTY_ADVANCED);
    }

    public String getCommaSeparatedSeenQuestionIds(String difficulty) {
        java.util.Set<Integer> set = getSeenQuestionIds(difficulty);
        if (set.isEmpty()) return "";
        StringBuilder sb = new StringBuilder();
        for (Integer id : set) {
            if (sb.length() > 0) sb.append(",");
            sb.append(id);
        }
        return sb.toString();
    }

    public boolean isOfflineResilienceEnabled() {
        return prefs.getBoolean(Constants.KEY_OFFLINE_RESILIENCE, true);
    }

    public void setOfflineResilience(boolean enabled) {
        prefs.edit().putBoolean(Constants.KEY_OFFLINE_RESILIENCE, enabled).apply();
    }
}
