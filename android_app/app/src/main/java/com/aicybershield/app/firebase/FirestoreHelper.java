package com.aicybershield.app.firebase;

import android.util.Log;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.utils.DateUtils;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.SetOptions;
import java.util.HashMap;
import java.util.Map;

public class FirestoreHelper {
    private static final String TAG = "FirestoreHelper";
    private static FirestoreHelper instance;
    private FirebaseFirestore db;

    private FirestoreHelper() {
        initDb();
    }

    private void initDb() {
        try {
            db = FirebaseFirestore.getInstance();
        } catch (Exception e) {
            Log.e(TAG, "Firestore initialization error: " + e.getMessage());
            db = null;
        }
    }

    public static synchronized FirestoreHelper getInstance() {
        if (instance == null) {
            instance = new FirestoreHelper();
        }
        return instance;
    }

    public void createUserDoc(String name, String email) {
        if (db == null) initDb();
        if (db == null || email == null) return;

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("name", name != null ? name : "User");
            data.put("email", email);
            data.put("createdAt", DateUtils.getCurrentDateTime());
            data.put("awarenessScore", 0);
            data.put("challengesCompleted", 0);

            db.collection("users")
                    .document(email)
                    .set(data, SetOptions.merge())
                    .addOnSuccessListener(aVoid -> Log.d(TAG, "User document successfully created: " + email))
                    .addOnFailureListener(e -> Log.e(TAG, "Error writing user document: " + e.getMessage()));
        } catch (Exception e) {
            Log.e(TAG, "Exception in createUserDoc: " + e.getMessage());
        }
    }

    public void syncScanResult(String userEmail, ScanHistoryItem item) {
        if (db == null) initDb();
        if (db == null || userEmail == null || item == null) return;

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("type", item.getType());
            data.put("target", item.getTarget());
            data.put("status", item.getStatus());
            data.put("reason", item.getReason());
            data.put("confidence", item.getConfidence());
            data.put("timestamp", item.getTimestamp());

            db.collection("users")
                    .document(userEmail)
                    .collection("scans")
                    .add(data)
                    .addOnSuccessListener(doc -> Log.d(TAG, "Scan synced to Firestore with ID: " + doc.getId()))
                    .addOnFailureListener(e -> Log.e(TAG, "Failed to sync scan: " + e.getMessage()));
        } catch (Exception e) {
            Log.e(TAG, "Exception in syncScanResult: " + e.getMessage());
        }
    }

    public void updateChallengeScore(String userEmail, int score) {
        if (db == null) initDb();
        if (db == null || userEmail == null) return;

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("awarenessScore", score);
            data.put("lastQuizDate", DateUtils.getCurrentDateTime());

            db.collection("users")
                    .document(userEmail)
                    .set(data, SetOptions.merge())
                    .addOnSuccessListener(aVoid -> Log.d(TAG, "Awareness score updated: " + score))
                    .addOnFailureListener(e -> Log.e(TAG, "Failed to update score: " + e.getMessage()));
        } catch (Exception e) {
            Log.e(TAG, "Exception in updateChallengeScore: " + e.getMessage());
        }
    }
}
