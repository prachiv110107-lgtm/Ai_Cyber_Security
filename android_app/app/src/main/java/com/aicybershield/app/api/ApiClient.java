package com.aicybershield.app.api;

import android.content.Context;
import com.aicybershield.app.storage.LocalStorageManager;
import java.util.concurrent.TimeUnit;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    private static Retrofit retrofit = null;
    private static String currentBaseUrl = "";

    public static synchronized ApiService getApiService(Context context) {
        String baseUrl = LocalStorageManager.getInstance(context).getServerBaseUrl();
        if (!baseUrl.endsWith("/")) {
            baseUrl += "/";
        }

        if (retrofit == null || !baseUrl.equals(currentBaseUrl)) {
            currentBaseUrl = baseUrl;

            HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
            logging.setLevel(HttpLoggingInterceptor.Level.BODY);

            OkHttpClient okHttpClient = new OkHttpClient.Builder()
                    .addInterceptor(logging)
                    .connectTimeout(15, TimeUnit.SECONDS)
                    .readTimeout(15, TimeUnit.SECONDS)
                    .writeTimeout(15, TimeUnit.SECONDS)
                    .retryOnConnectionFailure(true)
                    .build();

            try {
                retrofit = new Retrofit.Builder()
                        .baseUrl(currentBaseUrl)
                        .client(okHttpClient)
                        .addConverterFactory(GsonConverterFactory.create())
                        .build();
            } catch (Exception e) {
                // Fallback to default emulator IP if invalid
                retrofit = new Retrofit.Builder()
                        .baseUrl("http://10.0.2.2:5000/")
                        .client(okHttpClient)
                        .addConverterFactory(GsonConverterFactory.create())
                        .build();
            }
        }
        return retrofit.create(ApiService.class);
    }
}
