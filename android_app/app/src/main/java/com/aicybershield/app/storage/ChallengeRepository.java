package com.aicybershield.app.storage;

import android.content.Context;
import androidx.annotation.NonNull;
import com.aicybershield.app.api.ApiClient;
import com.aicybershield.app.models.ChallengeQuestion;
import com.aicybershield.app.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ChallengeRepository {

    private static ChallengeRepository instance;
    private final Gson gson;
    private List<ChallengeQuestion> cachedAssetQuestions = null;

    public interface ChallengeCallback {
        void onSuccess(List<ChallengeQuestion> questions);
        void onError(String errorMessage, List<ChallengeQuestion> fallbackQuestions);
    }

    private ChallengeRepository() {
        this.gson = new Gson();
    }

    public static synchronized ChallengeRepository getInstance() {
        if (instance == null) {
            instance = new ChallengeRepository();
        }
        return instance;
    }

    /**
     * Loads randomized, anti-repetition challenge questions for the requested difficulty.
     * Loads from local asset bank directly for instant 0ms response and 100% reliability offline/online.
     */
    public void getChallengeQuestions(@NonNull Context context, String difficulty, int count, @NonNull ChallengeCallback callback) {
        String safeDifficulty = (difficulty != null && !difficulty.trim().isEmpty())
                ? difficulty.trim().toLowerCase()
                : Constants.DIFFICULTY_BEGINNER;

        int safeCount = count > 0 ? count : 10;
        loadFromLocalAssets(context, safeDifficulty, safeCount, callback);
    }

    /**
     * Offline local asset question loader supporting 100 questions per level with anti-repetition tracking.
     */
    public synchronized void loadFromLocalAssets(@NonNull Context context, String difficulty, int count, @NonNull ChallengeCallback callback) {
        try {
            List<ChallengeQuestion> allQuestions = getAllAssetQuestions(context);
            if (allQuestions == null || allQuestions.isEmpty()) {
                callback.onError("Asset questions empty", getHardcodedSafetyFallback(difficulty));
                return;
            }

            String targetDifficulty = (difficulty != null) ? difficulty.trim().toLowerCase() : Constants.DIFFICULTY_BEGINNER;
            List<ChallengeQuestion> pool = new ArrayList<>();
            for (ChallengeQuestion q : allQuestions) {
                if (targetDifficulty.equalsIgnoreCase(q.getDifficulty())) {
                    pool.add(q);
                }
            }

            if (pool.isEmpty()) {
                pool.addAll(allQuestions);
            }

            LocalStorageManager storage = LocalStorageManager.getInstance(context);
            Set<Integer> seenIds = storage.getSeenQuestionIds(targetDifficulty);

            List<ChallengeQuestion> unseen = new ArrayList<>();
            for (ChallengeQuestion q : pool) {
                if (!seenIds.contains(q.getId())) {
                    unseen.add(q);
                }
            }

            // If unseen pool has fewer than requested count, reset history and use full pool
            if (unseen.size() < count) {
                storage.clearSeenQuestionIds(targetDifficulty);
                unseen = new ArrayList<>(pool);
            }

            Collections.shuffle(unseen);
            int takeCount = Math.min(count, unseen.size());
            List<ChallengeQuestion> selected = new ArrayList<>(unseen.subList(0, takeCount));

            List<Integer> selectedIds = new ArrayList<>();
            for (ChallengeQuestion q : selected) {
                selectedIds.add(q.getId());
            }
            storage.addSeenQuestionIds(targetDifficulty, selectedIds);

            callback.onSuccess(selected);
        } catch (Exception e) {
            callback.onError("Error parsing local questions: " + e.getMessage(), getHardcodedSafetyFallback(difficulty));
        }
    }

    private synchronized List<ChallengeQuestion> getAllAssetQuestions(Context context) {
        if (cachedAssetQuestions != null && !cachedAssetQuestions.isEmpty()) {
            return cachedAssetQuestions;
        }

        try (InputStream is = context.getAssets().open("challenge_questions.json");
             InputStreamReader reader = new InputStreamReader(is, StandardCharsets.UTF_8)) {
            Type listType = new TypeToken<List<ChallengeQuestion>>() {}.getType();
            cachedAssetQuestions = gson.fromJson(reader, listType);
            return cachedAssetQuestions;
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }

    public synchronized int getTotalQuestionsCount(Context context) {
        List<ChallengeQuestion> all = getAllAssetQuestions(context);
        return all != null && !all.isEmpty() ? all.size() : 300;
    }

    private List<ChallengeQuestion> getHardcodedSafetyFallback(String difficulty) {
        List<ChallengeQuestion> list = new ArrayList<>();
        list.add(new ChallengeQuestion(
                1, "beginner",
                "You receive an SMS saying your bank account is blocked. What should you do?",
                java.util.Arrays.asList(
                        "Click the link immediately",
                        "Share the OTP with caller",
                        "Verify through official bank app or official customer care",
                        "Forward message to friends"
                ),
                2,
                "Banks never send urgent threats asking you to click SMS links.",
                "Always verify through official banking channels."
        ));
        return list;
    }
}
