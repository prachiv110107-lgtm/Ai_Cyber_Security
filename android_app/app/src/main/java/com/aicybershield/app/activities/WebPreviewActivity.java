package com.aicybershield.app.activities;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.aicybershield.app.R;
import com.aicybershield.app.utils.Constants;

public class WebPreviewActivity extends AppCompatActivity {

    private WebView webViewSafe;
    private ProgressBar webLoadingProgress;
    private TextView txtWebUrl;
    private String targetUrl = "https://www.wikipedia.org";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_web_preview);

        if (getIntent().hasExtra(Constants.EXTRA_TARGET)) {
            targetUrl = getIntent().getStringExtra(Constants.EXTRA_TARGET);
        }

        if (!targetUrl.startsWith("http://") && !targetUrl.startsWith("https://")) {
            targetUrl = "https://" + targetUrl;
        }

        ImageView btnWebBack = findViewById(R.id.btnWebBack);
        ImageView btnWebExternal = findViewById(R.id.btnWebExternal);
        txtWebUrl = findViewById(R.id.txtWebUrl);
        webLoadingProgress = findViewById(R.id.webLoadingProgress);
        webViewSafe = findViewById(R.id.webViewSafe);

        txtWebUrl.setText(targetUrl);
        btnWebBack.setOnClickListener(v -> finish());

        btnWebExternal.setOnClickListener(v -> {
            Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(targetUrl));
            startActivity(browserIntent);
        });

        setupWebView();
        webViewSafe.loadUrl(targetUrl);
    }

    private void setupWebView() {
        WebSettings settings = webViewSafe.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);

        webViewSafe.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return false;
            }

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                webLoadingProgress.setVisibility(View.VISIBLE);
                txtWebUrl.setText(url);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                webLoadingProgress.setVisibility(View.GONE);
            }
        });

        webViewSafe.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                webLoadingProgress.setProgress(newProgress);
            }
        });
    }

    @Override
    public void onBackPressed() {
        if (webViewSafe.canGoBack()) {
            webViewSafe.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
