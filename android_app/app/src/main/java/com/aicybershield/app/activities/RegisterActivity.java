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

public class RegisterActivity extends AppCompatActivity {

    private TextInputEditText etName, etEmailReg, etPasswordReg;
    private ProgressBar registerProgressBar;
    private MaterialButton btnRegister;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        etName = findViewById(R.id.etName);
        etEmailReg = findViewById(R.id.etEmailReg);
        etPasswordReg = findViewById(R.id.etPasswordReg);
        registerProgressBar = findViewById(R.id.registerProgressBar);
        btnRegister = findViewById(R.id.btnRegister);
        TextView txtGoToLogin = findViewById(R.id.txtGoToLogin);

        btnRegister.setOnClickListener(v -> performRegister());
        txtGoToLogin.setOnClickListener(v -> finish());
    }

    private void performRegister() {
        String name = etName.getText() != null ? etName.getText().toString().trim() : "";
        String email = etEmailReg.getText() != null ? etEmailReg.getText().toString().trim() : "";
        String password = etPasswordReg.getText() != null ? etPasswordReg.getText().toString().trim() : "";

        if (TextUtils.isEmpty(name)) {
            etName.setError("Please enter your name");
            return;
        }
        if (TextUtils.isEmpty(email)) {
            etEmailReg.setError("Please enter your email");
            return;
        }
        if (TextUtils.isEmpty(password) || password.length() < 6) {
            etPasswordReg.setError("Password must be at least 6 characters");
            return;
        }

        registerProgressBar.setVisibility(View.VISIBLE);
        btnRegister.setEnabled(false);

        FirebaseAuthHelper.getInstance().register(this, name, email, password, new FirebaseAuthHelper.AuthCallback() {
            @Override
            public void onSuccess(String userName, String userEmail) {
                registerProgressBar.setVisibility(View.GONE);
                Toast.makeText(RegisterActivity.this, "Account created successfully! Please sign in.", Toast.LENGTH_LONG).show();
                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                startActivity(intent);
                finish();
            }

            @Override
            public void onFailure(String errorMessage) {
                registerProgressBar.setVisibility(View.GONE);
                btnRegister.setEnabled(true);
                Toast.makeText(RegisterActivity.this, errorMessage, Toast.LENGTH_LONG).show();
            }
        });
    }
}
