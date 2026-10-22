package com.aicybershield.app.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.aicybershield.app.R;
import java.util.List;

public class IndicatorsAdapter extends RecyclerView.Adapter<IndicatorsAdapter.ViewHolder> {

    private final Context context;
    private final List<String> indicators;
    private final String status;

    public IndicatorsAdapter(Context context, List<String> indicators, String status) {
        this.context = context;
        this.indicators = indicators;
        this.status = status;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_indicator, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        String indicator = indicators.get(position);
        holder.txtText.setText(indicator);

        if ("safe".equalsIgnoreCase(status)) {
            holder.imgIcon.setImageResource(R.drawable.ic_status_safe);
        } else if ("suspicious".equalsIgnoreCase(status)) {
            holder.imgIcon.setImageResource(R.drawable.ic_status_suspicious);
        } else {
            holder.imgIcon.setImageResource(R.drawable.ic_status_dangerous);
        }
    }

    @Override
    public int getItemCount() {
        return indicators != null ? indicators.size() : 0;
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        ImageView imgIcon;
        TextView txtText;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imgIcon = itemView.findViewById(R.id.imgIndicatorIcon);
            txtText = itemView.findViewById(R.id.txtIndicatorText);
        }
    }
}
