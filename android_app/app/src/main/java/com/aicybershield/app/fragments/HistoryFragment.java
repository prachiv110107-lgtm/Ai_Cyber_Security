package com.aicybershield.app.fragments;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import com.aicybershield.app.activities.ResultActivity;
import com.aicybershield.app.adapters.HistoryAdapter;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.models.ScanResult;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.google.android.material.chip.ChipGroup;
import java.util.List;

public class HistoryFragment extends Fragment {

    private RecyclerView rvHistory;
    private LinearLayout layoutEmptyHistory;
    private HistoryAdapter adapter;
    private LocalStorageManager storageManager;
    private ChipGroup chipGroupFilters;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_history, container, false);
        storageManager = LocalStorageManager.getInstance(requireContext());

        rvHistory = view.findViewById(R.id.rvHistory);
        layoutEmptyHistory = view.findViewById(R.id.layoutEmptyHistory);
        chipGroupFilters = view.findViewById(R.id.chipGroupFilters);
        TextView btnClearHistory = view.findViewById(R.id.btnClearHistory);

        rvHistory.setLayoutManager(new LinearLayoutManager(requireContext()));

        btnClearHistory.setOnClickListener(v -> showClearHistoryDialog());

        setupFilterChips();
        loadHistory();
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        loadHistory();
    }

    private void setupFilterChips() {
        chipGroupFilters.setOnCheckedStateChangeListener((group, checkedIds) -> {
            if (checkedIds.isEmpty() || adapter == null) return;
            int id = checkedIds.get(0);
            if (id == R.id.chipLinks) {
                adapter.filterByType("Links");
            } else if (id == R.id.chipQr) {
                adapter.filterByType("QR Codes");
            } else if (id == R.id.chipSms) {
                adapter.filterByType("SMS");
            } else if (id == R.id.chipEmail) {
                adapter.filterByType("Email");
            } else {
                adapter.filterByType("all");
            }
        });
    }

    private void loadHistory() {
        List<ScanHistoryItem> list = storageManager.getScanHistory();
        if (list.isEmpty()) {
            rvHistory.setVisibility(View.GONE);
            layoutEmptyHistory.setVisibility(View.VISIBLE);
        } else {
            rvHistory.setVisibility(View.VISIBLE);
            layoutEmptyHistory.setVisibility(View.GONE);

            adapter = new HistoryAdapter(requireContext(), list, item -> {
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
            rvHistory.setAdapter(adapter);
        }
    }

    private void showClearHistoryDialog() {
        new AlertDialog.Builder(requireContext())
                .setTitle("Clear Scan History")
                .setMessage("Are you sure you want to clear all your scan records? This action cannot be undone.")
                .setPositiveButton("Clear All", (dialog, which) -> {
                    storageManager.clearHistory();
                    loadHistory();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }
}
