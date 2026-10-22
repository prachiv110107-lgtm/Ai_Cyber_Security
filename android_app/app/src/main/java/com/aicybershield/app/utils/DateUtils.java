package com.aicybershield.app.utils;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class DateUtils {
    public static String getCurrentDateTime() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        return sdf.format(new Date());
    }

    public static String formatShortDate(String dateTimeStr) {
        if (dateTimeStr == null || dateTimeStr.isEmpty()) return "Recent";
        try {
            SimpleDateFormat input = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
            Date date = input.parse(dateTimeStr);
            if (date != null) {
                SimpleDateFormat output = new SimpleDateFormat("MMM dd, hh:mm a", Locale.getDefault());
                return output.format(date);
            }
        } catch (Exception ignored) {}
        return dateTimeStr;
    }
}
