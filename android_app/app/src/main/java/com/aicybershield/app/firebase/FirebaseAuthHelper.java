package com.aicybershield.app.firebase;

import android.content.Context;
import android.util.Log;
import com.aicybershield.app.storage.LocalStorageManager;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.UserProfileChangeRequest;

public class FirebaseAuthHelper {
    private static final String TAG = "FirebaseAuthHelper";
    private static FirebaseAuthHelper instance;
    private FirebaseAuth mAuth;

    public interface AuthCallback {
        void onSuccess(String userName, String email);
        void onFailure(String errorMessage);
    }

    private FirebaseAuthHelper() {
        initAuth();
    }

    private void initAuth() {
        try {
            mAuth = FirebaseAuth.getInstance();
        } catch (Exception e) {
            Log.e(TAG, "FirebaseAuth initialization failed: " + e.getMessage());
            mAuth = null;
        }
    }

    public static synchronized FirebaseAuthHelper getInstance() {
        if (instance == null) {
            instance = new FirebaseAuthHelper();
        }
        return instance;
    }

    public boolean isUserLoggedIn() {
        if (mAuth == null) initAuth();
        return mAuth != null && mAuth.getCurrentUser() != null;
    }

    public FirebaseUser getCurrentUser() {
        if (mAuth == null) initAuth();
        return mAuth != null ? mAuth.getCurrentUser() : null;
    }

    public void login(Context context, String email, String password, AuthCallback callback) {
        if (mAuth == null) initAuth();

        if (mAuth == null) {
            callback.onFailure("Firebase Authentication is not available on this device.");
            return;
        }

        try {
            mAuth.signInWithEmailAndPassword(email, password)
                    .addOnCompleteListener(task -> {
                        if (task.isSuccessful() && mAuth.getCurrentUser() != null) {
                            FirebaseUser user = mAuth.getCurrentUser();
                            String userEmail = user.getEmail() != null ? user.getEmail() : email;
                            String userName = user.getDisplayName() != null && !user.getDisplayName().isEmpty() ?
                                    user.getDisplayName() : userEmail.split("@")[0];

                            LocalStorageManager.getInstance(context).resetForNewUser(userName, userEmail);
                            FirestoreHelper.getInstance().createUserDoc(userName, userEmail);

                            callback.onSuccess(userName, userEmail);
                        } else {
                            String err = task.getException() != null ? task.getException().getMessage() : "Authentication failed";
                            Log.e(TAG, "Login failed: " + err);
                            callback.onFailure(err);
                        }
                    });
        } catch (Exception e) {
            Log.e(TAG, "Exception during login: " + e.getMessage());
            callback.onFailure(e.getMessage());
        }
    }

    public void register(Context context, String name, String email, String password, AuthCallback callback) {
        if (mAuth == null) initAuth();

        if (mAuth == null) {
            callback.onFailure("Firebase Authentication is not available on this device.");
            return;
        }

        try {
            mAuth.createUserWithEmailAndPassword(email, password)
                    .addOnCompleteListener(task -> {
                        if (task.isSuccessful() && mAuth.getCurrentUser() != null) {
                            FirebaseUser user = mAuth.getCurrentUser();

                            try {
                                UserProfileChangeRequest profileUpdates = new UserProfileChangeRequest.Builder()
                                        .setDisplayName(name)
                                        .build();
                                user.updateProfile(profileUpdates);
                            } catch (Exception ignored) {}

                            LocalStorageManager.getInstance(context).resetForNewUser(name, email);
                            FirestoreHelper.getInstance().createUserDoc(name, email);

                            // Sign out so user explicitly signs in from LoginActivity
                            try {
                                mAuth.signOut();
                            } catch (Exception ignored) {}

                            callback.onSuccess(name, email);
                        } else {
                            String err = task.getException() != null ? task.getException().getMessage() : "Registration failed";
                            Log.e(TAG, "Registration failed: " + err);
                            callback.onFailure(err);
                        }
                    });
        } catch (Exception e) {
            Log.e(TAG, "Exception during registration: " + e.getMessage());
            callback.onFailure(e.getMessage());
        }
    }

    public void logout(Context context) {
        if (mAuth == null) initAuth();
        if (mAuth != null) {
            try {
                mAuth.signOut();
            } catch (Exception ignored) {}
        }
    }
}
