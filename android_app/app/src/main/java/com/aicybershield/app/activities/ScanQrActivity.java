package com.aicybershield.app.activities;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.aicybershield.app.R;
import com.aicybershield.app.api.ApiClient;
import com.aicybershield.app.api.QrRequest;
import com.aicybershield.app.firebase.FirestoreHelper;
import com.aicybershield.app.models.ScanHistoryItem;
import com.aicybershield.app.models.ScanResult;
import com.aicybershield.app.storage.LocalStorageManager;
import com.aicybershield.app.utils.Constants;
import com.aicybershield.app.utils.DateUtils;
import com.aicybershield.app.utils.UrlSafetyChecker;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.MultiFormatReader;
import com.google.zxing.RGBLuminanceSource;
import com.google.zxing.Result;
import com.google.zxing.common.HybridBinarizer;
import com.journeyapps.barcodescanner.BarcodeCallback;
import com.journeyapps.barcodescanner.BarcodeResult;
import com.journeyapps.barcodescanner.DecoratedBarcodeView;
import java.io.InputStream;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ScanQrActivity extends AppCompatActivity {

    private static final int CAMERA_PERMISSION_REQ = 101;
    private static final int GALLERY_PICK_REQ = 102;

    private DecoratedBarcodeView barcodeScannerView;
    private ProgressBar qrProgressBar;
    private boolean isTorchOn = false;
    private boolean hasScanned = false;
    private LocalStorageManager storageManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_qr);
        storageManager = LocalStorageManager.getInstance(this);

        barcodeScannerView = findViewById(R.id.barcodeScannerView);
        qrProgressBar = findViewById(R.id.qrProgressBar);
        ImageView btnBackQr = findViewById(R.id.btnBackQr);
        ImageView btnToggleTorch = findViewById(R.id.btnToggleTorch);
        ImageView btnPickGallery = findViewById(R.id.btnPickGallery);

        btnBackQr.setOnClickListener(v -> finish());

        btnToggleTorch.setOnClickListener(v -> {
            if (isTorchOn) {
                barcodeScannerView.setTorchOff();
                isTorchOn = false;
            } else {
                barcodeScannerView.setTorchOn();
                isTorchOn = true;
            }
        });

        btnPickGallery.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_PICK);
            intent.setType("image/*");
            startActivityForResult(intent, GALLERY_PICK_REQ);
        });

        checkCameraPermissionAndStart();
    }

    private void checkCameraPermissionAndStart() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_REQ);
        } else {
            startScanning();
        }
    }

    private void startScanning() {
        barcodeScannerView.decodeContinuous(new BarcodeCallback() {
            @Override
            public void barcodeResult(BarcodeResult result) {
                if (result.getText() != null && !hasScanned) {
                    hasScanned = true;
                    barcodeScannerView.pause();
                    analyzeQrCode(result.getText());
                }
            }
        });
    }

    private void analyzeQrCode(String qrData) {
        qrProgressBar.setVisibility(View.VISIBLE);

        ApiClient.getApiService(this).predictQr(new QrRequest(qrData)).enqueue(new Callback<ScanResult>() {
            @Override
            public void onResponse(@NonNull Call<ScanResult> call, @NonNull Response<ScanResult> response) {
                qrProgressBar.setVisibility(View.GONE);
                if (response.isSuccessful() && response.body() != null) {
                    handleScanResult(response.body());
                } else {
                    fallbackLocalQrAnalysis(qrData);
                }
            }

            @Override
            public void onFailure(@NonNull Call<ScanResult> call, @NonNull Throwable t) {
                qrProgressBar.setVisibility(View.GONE);
                fallbackLocalQrAnalysis(qrData);
            }
        });
    }

    private void fallbackLocalQrAnalysis(String qrData) {
        ScanResult res = UrlSafetyChecker.evaluateUrl(qrData);
        res.setType(Constants.TYPE_QR);
        handleScanResult(res);
    }

    private void handleScanResult(ScanResult result) {
        ScanHistoryItem historyItem = new ScanHistoryItem(
                String.valueOf(System.currentTimeMillis()),
                Constants.TYPE_QR,
                result.getTarget(),
                result.getStatus(),
                result.getReason(),
                result.getConfidence(),
                DateUtils.getCurrentDateTime(),
                result
        );

        storageManager.addScanHistoryItem(historyItem);
        FirestoreHelper.getInstance().syncScanResult(storageManager.getUserProfile().getEmail(), historyItem);

        Intent intent = new Intent(this, ResultActivity.class);
        intent.putExtra(Constants.EXTRA_SCAN_RESULT, result);
        startActivity(intent);
        finish();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == GALLERY_PICK_REQ && resultCode == RESULT_OK && data != null && data.getData() != null) {
            try {
                Uri imageUri = data.getData();
                InputStream imageStream = getContentResolver().openInputStream(imageUri);
                Bitmap bitmap = BitmapFactory.decodeStream(imageStream);
                if (bitmap != null) {
                    decodeBitmapQr(bitmap);
                }
            } catch (Exception e) {
                Toast.makeText(this, "Failed to load image from gallery", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void decodeBitmapQr(Bitmap bitmap) {
        try {
            int[] intArray = new int[bitmap.getWidth() * bitmap.getHeight()];
            bitmap.getPixels(intArray, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());
            RGBLuminanceSource source = new RGBLuminanceSource(bitmap.getWidth(), bitmap.getHeight(), intArray);
            BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(source));
            Result result = new MultiFormatReader().decode(binaryBitmap);
            if (result != null && result.getText() != null) {
                analyzeQrCode(result.getText());
            } else {
                Toast.makeText(this, "No QR Code detected in image", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Toast.makeText(this, "Could not decode QR code from image", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERMISSION_REQ) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startScanning();
            } else {
                Toast.makeText(this, "Camera permission is required to scan QR codes", Toast.LENGTH_LONG).show();
                finish();
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        hasScanned = false;
        if (barcodeScannerView != null) barcodeScannerView.resume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (barcodeScannerView != null) barcodeScannerView.pause();
    }
}
