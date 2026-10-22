package com.aicybershield.app.fragments;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import com.aicybershield.app.activities.ChallengeActivity;
import com.aicybershield.app.activities.MainActivity;
import com.aicybershield.app.activities.ResultActivity;
import com.aicybershield.app.activities.ScanEmailActivity;
import com.aicybershield.app.activities.ScanLinkActivity;
import com.aicybershield.app.activities.ScanQrActivity;
import com.aicybershield.app.activities.ScanSmsActivity;
import com.aicybershield.app.activities.SettingsActivity;
import com.aicybershield.app.adapters.RecentScansAdapter;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.models.ScanResult;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.card.MaterialCardView;
import java.util.List;

public class HomeFragment extends Fragment {

    private RecyclerView rvRecentScans;
    private TextView txtEmptyRecentScans;
    private RecentScansAdapter adapter;
    private LocalStorageManager storageManager;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        storageManager = LocalStorageManager.getInstance(requireContext());

        initViews(view);
        loadRecentScans();
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        loadRecentScans();
    }

    private void initViews(View view) {
        MaterialCardView cardScanLink = view.findViewById(R.id.cardScanLink);
        MaterialCardView cardScanQr = view.findViewById(R.id.cardScanQr);
        MaterialCardView cardScanSms = view.findViewById(R.id.cardScanSms);
        MaterialCardView cardScanEmail = view.findViewById(R.id.cardScanEmail);
        CardView cardChallengeBanner = view.findViewById(R.id.cardChallengeBanner);
        TextView btnBannerStart = view.findViewById(R.id.btnBannerStart);
        ImageView btnQuickSettings = view.findViewById(R.id.btnQuickSettings);
        TextView txtViewAllHistory = view.findViewById(R.id.txtViewAllHistory);

        rvRecentScans = view.findViewById(R.id.rvRecentScans);
        txtEmptyRecentScans = view.findViewById(R.id.txtEmptyRecentScans);

        rvRecentScans.setLayoutManager(new LinearLayoutManager(requireContext()));

        cardScanLink.setOnClickListener(v -> startActivity(new Intent(requireContext(), ScanLinkActivity.class)));
        cardScanQr.setOnClickListener(v -> startActivity(new Intent(requireContext(), ScanQrActivity.class)));
        cardScanSms.setOnClickListener(v -> startActivity(new Intent(requireContext(), ScanSmsActivity.class)));
        cardScanEmail.setOnClickListener(v -> startActivity(new Intent(requireContext(), ScanEmailActivity.class)));

        View.OnClickListener startChallengeListener = v -> {
            Intent intent = new Intent(requireContext(), ChallengeActivity.class);
            intent.putExtra(Constants.EXTRA_DIFFICULTY, "beginner");
            startActivity(intent);
        };
        cardChallengeBanner.setOnClickListener(startChallengeListener);
        btnBannerStart.setOnClickListener(startChallengeListener);

        btnQuickSettings.setOnClickListener(v -> startActivity(new Intent(requireContext(), SettingsActivity.class)));

        txtViewAllHistory.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).navigateToTab(R.id.nav_history);
            }
        });
    }

    private void loadRecentScans() {
        List<ScanHistoryItem> list = storageManager.getScanHistory();
        if (list.isEmpty()) {
            rvRecentScans.setVisibility(View.GONE);
            txtEmptyRecentScans.setVisibility(View.VISIBLE);
        } else {
            rvRecentScans.setVisibility(View.VISIBLE);
            txtEmptyRecentScans.setVisibility(View.GONE);

            adapter = new RecentScansAdapter(requireContext(), list, item -> {
                ScanResult result = item.getFullResult();
                if (result == null) {
                    result = new ScanResult(
                            item.getStatus(),
                            item.getConfidence(),
                            item.getTarget(),
                            item.getType(),
                            item.getReason(),
                            null,
                            null,
                            item.getTimestamp()
                    );
                }
                Intent intent = new Intent(requireContext(), ResultActivity.class);
                intent.putExtra(Constants.EXTRA_SCAN_RESULT, result);
                startActivity(intent);
            });
            rvRecentScans.setAdapter(adapter);
        }
    }
}
