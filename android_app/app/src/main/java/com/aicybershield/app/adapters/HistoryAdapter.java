package com.aicybershield.app.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.utils.Constants;
import java.util.ArrayList;
import java.util.List;

public class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.ViewHolder> {

    public interface OnItemClickListener {
        void onItemClick(ScanHistoryItem item);
    }

    private final Context context;
    private List<ScanHistoryItem> fullList;
    private List<ScanHistoryItem> filteredList;
    private final OnItemClickListener listener;

    public HistoryAdapter(Context context, List<ScanHistoryItem> list, OnItemClickListener listener) {
        this.context = context;
        this.fullList = list != null ? list : new ArrayList<>();
        this.filteredList = new ArrayList<>(this.fullList);
        this.listener = listener;
    }

    public void updateData(List<ScanHistoryItem> newList) {
        this.fullList = newList != null ? newList : new ArrayList<>();
        this.filteredList = new ArrayList<>(this.fullList);
        notifyDataSetChanged();
    }

    public void filterByType(String type) {
        filteredList.clear();
        if ("all".equalsIgnoreCase(type) || type.isEmpty()) {
            filteredList.addAll(fullList);
        } else {
            for (ScanHistoryItem item : fullList) {
                if (item.getType().equalsIgnoreCase(type) ||
                        (type.equalsIgnoreCase("Links") && item.getType().equalsIgnoreCase("URL")) ||
                        (type.equalsIgnoreCase("QR Codes") && item.getType().equalsIgnoreCase("QR Code"))) {
                    filteredList.add(item);
                }
            }
        }
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_history, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ScanHistoryItem item = filteredList.get(position);

        holder.txtType.setText(item.getType());
        holder.txtDate.setText(item.getTimestamp());
        holder.txtContent.setText(item.getTarget());
        holder.txtReason.setText(item.getReason());

        String status = item.getStatus();
        if (Constants.STATUS_DANGEROUS.equalsIgnoreCase(status)) {
            holder.txtBadge.setText("Dangerous");
            holder.txtBadge.setBackgroundResource(R.drawable.bg_badge_dangerous);
            holder.txtBadge.setTextColor(ContextCompat.getColor(context, R.color.danger_dark));
        } else if (Constants.STATUS_SUSPICIOUS.equalsIgnoreCase(status)) {
            holder.txtBadge.setText("Suspicious");
            holder.txtBadge.setBackgroundResource(R.drawable.bg_badge_suspicious);
            holder.txtBadge.setTextColor(ContextCompat.getColor(context, R.color.suspicious_dark));
        } else {
            holder.txtBadge.setText("Safe");
            holder.txtBadge.setBackgroundResource(R.drawable.bg_badge_safe);
            holder.txtBadge.setTextColor(ContextCompat.getColor(context, R.color.safe_dark));
        }

        holder.itemView.setOnClickListener(v -> {
            if (listener != null) listener.onItemClick(item);
        });
    }

    @Override
    public int getItemCount() {
        return filteredList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView txtType;
        TextView txtDate;
        TextView txtBadge;
        TextView txtContent;
        TextView txtReason;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            txtType = itemView.findViewById(R.id.txtHistoryType);
            txtDate = itemView.findViewById(R.id.txtHistoryDate);
            txtBadge = itemView.findViewById(R.id.txtHistoryBadge);
            txtContent = itemView.findViewById(R.id.txtHistoryContent);
            txtReason = itemView.findViewById(R.id.txtHistoryReason);
        }
    }
}
