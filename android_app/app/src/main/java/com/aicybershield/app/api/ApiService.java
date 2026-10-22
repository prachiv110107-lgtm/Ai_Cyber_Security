package com.aicybershield.app.api;

import com.aicybershield.app.models.ChallengeQuestion;
import com.aicybershield.app.models.ScanResult;
import java.util.List;
import java.util.Map;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;

public interface ApiService {

    @POST("predict-url")
    Call<ScanResult> predictUrl(@Body UrlRequest request);

    @POST("predict-sms")
    Call<ScanResult> predictSms(@Body SmsRequest request);

    @POST("predict-email")
    Call<ScanResult> predictEmail(@Body EmailRequest request);

    @POST("predict-qr")
    Call<ScanResult> predictQr(@Body QrRequest request);

    @GET("challenge-questions")
    Call<List<ChallengeQuestion>> getChallengeQuestions(
            @Query("difficulty") String difficulty,
            @Query("count") Integer count,
            @Query("exclude_ids") String excludeIds
    );

    @GET("challenge-questions")
    Call<List<ChallengeQuestion>> getChallengeQuestions(@Query("difficulty") String difficulty);

    @GET("health")
    Call<Map<String, Object>> checkHealth();
}
