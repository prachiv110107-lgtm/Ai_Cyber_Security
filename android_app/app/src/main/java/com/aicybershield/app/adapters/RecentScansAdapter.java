package com.aicybershield.app.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.utils.Constants;
import com.aicybershield.app.utils.DateUtils;
import java.util.List;

public class RecentScansAdapter extends RecyclerView.Adapter<RecentScansAdapter.ViewHolder> {

    public interface OnItemClickListener {
        void onItemClick(ScanHistoryItem item);
    }

    private final Context context;
    private final List<ScanHistoryItem> itemList;
    private final OnItemClickListener listener;

    public RecentScansAdapter(Context context, List<ScanHistoryItem> itemList, OnItemClickListener listener) {
        this.context = context;
        this.itemList = itemList;
        this.listener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_recent_scan, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ScanHistoryItem item = itemList.get(position);

        holder.txtTarget.setText(item.getTarget());
        holder.txtDate.setText(DateUtils.formatShortDate(item.getTimestamp()) + " • " + item.getType());

        // Type icon
        if (Constants.TYPE_QR.equalsIgnoreCase(item.getType())) {
            holder.imgTypeIcon.setImageResource(R.drawable.ic_scan_qr);
        } else if (Constants.TYPE_SMS.equalsIgnoreCase(item.getType())) {
            holder.imgTypeIcon.setImageResource(R.drawable.ic_scan_sms);
        } else if (Constants.TYPE_EMAIL.equalsIgnoreCase(item.getType())) {
            holder.imgTypeIcon.setImageResource(R.drawable.ic_scan_email);
        } else {
            holder.imgTypeIcon.setImageResource(R.drawable.ic_scan_link);
        }

        // Status badge styling
        String status = item.getStatus();
        if (Constants.STATUS_DANGEROUS.equalsIgnoreCase(status)) {
            holder.txtStatusBadge.setText("Dangerous");
            holder.txtStatusBadge.setBackgroundResource(R.drawable.bg_badge_dangerous);
            holder.txtStatusBadge.setTextColor(ContextCompat.getColor(context, R.color.danger_dark));
        } else if (Constants.STATUS_SUSPICIOUS.equalsIgnoreCase(status)) {
            holder.txtStatusBadge.setText("Suspicious");
            holder.txtStatusBadge.setBackgroundResource(R.drawable.bg_badge_suspicious);
            holder.txtStatusBadge.setTextColor(ContextCompat.getColor(context, R.color.suspicious_dark));
        } else {
            holder.txtStatusBadge.setText("Safe");
            holder.txtStatusBadge.setBackgroundResource(R.drawable.bg_badge_safe);
            holder.txtStatusBadge.setTextColor(ContextCompat.getColor(context, R.color.safe_dark));
        }

        holder.itemView.setOnClickListener(v -> {
            if (listener != null) listener.onItemClick(item);
        });
    }

    @Override
    public int getItemCount() {
        return Math.min(itemList.size(), 5); // Display top 5 on home dashboard
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        ImageView imgTypeIcon;
        TextView txtTarget;
        TextView txtDate;
        TextView txtStatusBadge;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imgTypeIcon = itemView.findViewById(R.id.imgItemTypeIcon);
            txtTarget = itemView.findViewById(R.id.txtItemTarget);
            txtDate = itemView.findViewById(R.id.txtItemDate);
            txtStatusBadge = itemView.findViewById(R.id.txtItemStatusBadge);
        }
    }
}
