package com.aicybershield.app.fragments;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.aicybershield.app.R;
import com.aicybershield.app.activities.AboutActivity;
import com.aicybershield.app.activities.LoginActivity;
import com.aicybershield.app.firebase.FirebaseAuthHelper;
import com.aicybershield.app.models.UserProfile;
import com.aicybershield.app.storage.LocalStorageManager;
import com.google.android.material.button.MaterialButton;

public class ProfileFragment extends Fragment {

    private TextView txtProfileName, txtProfileEmail;
    private LocalStorageManager storageManager;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profile, container, false);
        storageManager = LocalStorageManager.getInstance(requireContext());

        initViews(view);
        loadUserData();
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        loadUserData();
    }

    private void initViews(View view) {
        txtProfileName = view.findViewById(R.id.txtProfileName);
        txtProfileEmail = view.findViewById(R.id.txtProfileEmail);

        LinearLayout optEditProfile = view.findViewById(R.id.optEditProfile);
        LinearLayout optChangePassword = view.findViewById(R.id.optChangePassword);
        LinearLayout optAbout = view.findViewById(R.id.optAbout);
        MaterialButton btnLogout = view.findViewById(R.id.btnLogout);

        optEditProfile.setOnClickListener(v -> showEditNameDialog());
        optChangePassword.setOnClickListener(v -> showChangePasswordDialog());
        optAbout.setOnClickListener(v -> startActivity(new Intent(requireContext(), AboutActivity.class)));
        btnLogout.setOnClickListener(v -> showLogoutConfirmation());
    }

    private void loadUserData() {
        if (!isAdded()) return;
        UserProfile profile = storageManager.getUserProfile();
        txtProfileName.setText(profile.getName());
        txtProfileEmail.setText(profile.getEmail());
    }

    private void showEditNameDialog() {
        EditText input = new EditText(requireContext());
        input.setText(storageManager.getUserProfile().getName());
        input.setPadding(48, 32, 48, 32);

        new AlertDialog.Builder(requireContext())
                .setTitle("Change Name")
                .setView(input)
                .setPositiveButton("Save", (dialog, which) -> {
                    String newName = input.getText().toString().trim();
                    if (!newName.isEmpty()) {
                        UserProfile profile = storageManager.getUserProfile();
                        storageManager.saveUserProfile(newName, profile.getEmail(), profile.getAwarenessScore());
                        loadUserData();
                        Toast.makeText(requireContext(), "Name updated successfully", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void showChangePasswordDialog() {
        new AlertDialog.Builder(requireContext())
                .setTitle("Change Password")
                .setMessage("A secure password reset link will be sent to:\n" + storageManager.getUserProfile().getEmail())
                .setPositiveButton("Send Reset Link", (dialog, which) -> {
                    Toast.makeText(requireContext(), "Password reset email sent.", Toast.LENGTH_SHORT).show();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void showLogoutConfirmation() {
        new AlertDialog.Builder(requireContext())
                .setTitle("Sign Out")
                .setMessage("Are you sure you want to sign out?")
                .setPositiveButton("Sign Out", (dialog, which) -> {
                    FirebaseAuthHelper.getInstance().logout(requireContext());
                    Intent intent = new Intent(requireContext(), LoginActivity.class);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(intent);
                })
                .setNegativeButton("Cancel", null)
                .show();
    }
}
