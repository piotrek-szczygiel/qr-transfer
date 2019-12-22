package com.example.qrreceiver;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.WorkerThread;
import androidx.appcompat.app.AppCompatActivity;

import com.otaliastudios.cameraview.CameraView;
import com.otaliastudios.cameraview.frame.Frame;
import com.otaliastudios.cameraview.frame.FrameProcessor;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        CameraView camera = findViewById(R.id.camera);
        camera.setLifecycleOwner(this);

        camera.addFrameProcessor(new FrameProcessor() {
            @Override
            @WorkerThread
            public void process(@NonNull Frame frame) {
                if (frame.getDataClass() == byte[].class) {
                    byte[] data = frame.getData();
                }
            }
        });
    }
}
