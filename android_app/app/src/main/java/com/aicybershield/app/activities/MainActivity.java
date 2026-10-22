package com.aicybershield.app.activities;

import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import com.aicybershield.app.R;
import com.aicybershield.app.fragments.ChallengeFragment;
import com.aicybershield.app.fragments.HistoryFragment;
import com.aicybershield.app.fragments.HomeFragment;
import com.aicybershield.app.fragments.ProfileFragment;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNavigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottom_navigation);
        setupBottomNavigation();

        // Default to Home Fragment
        if (savedInstanceState == null) {
            loadFragment(new HomeFragment());
        }

        handleShareIntent(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        handleShareIntent(intent);
    }

    private void handleShareIntent(Intent intent) {
        if (intent != null && Intent.ACTION_SEND.equals(intent.getAction()) && "text/plain".equals(intent.getType())) {
            String sharedText = intent.getStringExtra(Intent.EXTRA_TEXT);
            if (sharedText != null && !sharedText.isEmpty()) {
                if (sharedText.startsWith("http://") || sharedText.startsWith("https://") || sharedText.contains(".com") || sharedText.contains(".org")) {
                    Intent scanIntent = new Intent(this, ScanLinkActivity.class);
                    scanIntent.putExtra(Constants.EXTRA_TARGET, sharedText);
                    startActivity(scanIntent);
                } else {
                    Intent smsIntent = new Intent(this, ScanSmsActivity.class);
                    smsIntent.putExtra(Constants.EXTRA_TARGET, sharedText);
                    startActivity(smsIntent);
                }
            }
        }
    }

    private void setupBottomNavigation() {
        bottomNavigationView.setOnItemSelectedListener(item -> {
            Fragment selectedFragment = null;
            int itemId = item.getItemId();

            if (itemId == R.id.nav_home) {
                selectedFragment = new HomeFragment();
            } else if (itemId == R.id.nav_history) {
                selectedFragment = new HistoryFragment();
            } else if (itemId == R.id.nav_challenge) {
                selectedFragment = new ChallengeFragment();
            } else if (itemId == R.id.nav_profile) {
                selectedFragment = new ProfileFragment();
            }

            if (selectedFragment != null) {
                loadFragment(selectedFragment);
                return true;
            }
            return false;
        });
    }

    public void navigateToTab(int menuItemId) {
        bottomNavigationView.setSelectedItemId(menuItemId);
    }

    private void loadFragment(Fragment fragment) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.fragment_container, fragment)
                .commit();
    }
}
