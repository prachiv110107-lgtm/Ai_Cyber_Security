package com.aicybershield.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.firebase.FirebaseAuthHelper;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;

public class LoginActivity extends AppCompatActivity {

    private TextInputEditText etEmail, etPassword;
    private ProgressBar loginProgressBar;
    private MaterialButton btnLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        loginProgressBar = findViewById(R.id.loginProgressBar);
        btnLogin = findViewById(R.id.btnLogin);
        TextView txtGoToRegister = findViewById(R.id.txtGoToRegister);

        btnLogin.setOnClickListener(v -> performLogin());

        txtGoToRegister.setOnClickListener(v -> startActivity(new Intent(LoginActivity.this, RegisterActivity.class)));
    }

    private void performLogin() {
        String email = etEmail.getText() != null ? etEmail.getText().toString().trim() : "";
        String password = etPassword.getText() != null ? etPassword.getText().toString().trim() : "";

        if (TextUtils.isEmpty(email)) {
            etEmail.setError("Please enter your email");
            return;
        }
        if (TextUtils.isEmpty(password)) {
            etPassword.setError("Please enter your password");
            return;
        }

        loginProgressBar.setVisibility(View.VISIBLE);
        btnLogin.setEnabled(false);

        FirebaseAuthHelper.getInstance().login(this, email, password, new FirebaseAuthHelper.AuthCallback() {
            @Override
            public void onSuccess(String userName, String userEmail) {
                loginProgressBar.setVisibility(View.GONE);
                Toast.makeText(LoginActivity.this, "Welcome, " + userName + "!", Toast.LENGTH_SHORT).show();
                startActivity(new Intent(LoginActivity.this, MainActivity.class));
                finish();
            }

            @Override
            public void onFailure(String errorMessage) {
                loginProgressBar.setVisibility(View.GONE);
                btnLogin.setEnabled(true);
                Toast.makeText(LoginActivity.this, errorMessage, Toast.LENGTH_LONG).show();
            }
        });
    }
}
