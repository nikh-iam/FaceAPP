package com.example.faceapi

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.YuvImage
import android.util.Log
import android.view.Surface
import android.widget.Toast
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.CameraController
import androidx.camera.view.LifecycleCameraController
import androidx.camera.view.PreviewView
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import java.io.ByteArrayOutputStream

@Composable
fun CameraPreview(viewModel: FaceRecognitionViewModel) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val lastSentTime = remember { mutableStateOf(0L) }

    // Initialize the LifecycleCameraController
    val cameraController = remember {
        LifecycleCameraController(context).apply {
            // Enable desired use cases
            setEnabledUseCases(
                CameraController.IMAGE_ANALYSIS or
                        CameraController.IMAGE_CAPTURE or
                        CameraController.VIDEO_CAPTURE
            )
            // Bind the controller to the lifecycle
            bindToLifecycle(lifecycleOwner)

            // Set the image analysis analyzer
            setImageAnalysisAnalyzer(
                ContextCompat.getMainExecutor(context),
                ImageAnalysis.Analyzer { image ->
                    try {
                        val currentTime = System.currentTimeMillis()
                        // Throttle image sending to once every 500ms
                        if (viewModel.isConnected.value && currentTime - lastSentTime.value > 500) {
                            Log.d("CameraPreview", "Processing image")
                            val bitmap = image.toBitmap(cameraSelector)
                            viewModel.sendImage(bitmap)
                            Log.d("CameraPreview", "Image sent to server")
                            lastSentTime.value = currentTime
                        }
                    } catch (e: Exception) {
                        Log.e("CameraPreview", "Error analyzing image", e)
                    } finally {
                        image.close()
                    }
                }
            )
        }
    }

    // Display the camera preview
    AndroidView(
        modifier = Modifier.fillMaxSize(),
        factory = { ctx ->
            PreviewView(ctx).apply {
                scaleType = PreviewView.ScaleType.FILL_START
                rotation = 0f
                implementationMode = PreviewView.ImplementationMode.COMPATIBLE
                controller = cameraController
                (controller as LifecycleCameraController).cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA
            }
        },
        onRelease = {
            cameraController.unbind()
        }
    )
}

private fun ImageProxy.toBitmap(cameraSelector: CameraSelector): Bitmap {
    val yBuffer = planes[0].buffer
    val uBuffer = planes[1].buffer
    val vBuffer = planes[2].buffer

    val ySize = yBuffer.remaining()
    val uSize = uBuffer.remaining()
    val vSize = vBuffer.remaining()

    val nv21 = ByteArray(ySize + uSize + vSize).apply {
        yBuffer.get(this, 0, ySize)
        vBuffer.get(this, ySize, vSize)
        uBuffer.get(this, ySize + vSize, uSize)
    }

    val yuvImage = YuvImage(nv21, ImageFormat.NV21, width, height, null)
    val out = ByteArrayOutputStream().apply {
        yuvImage.compressToJpeg(Rect(0, 0, width, height), 90, this)
    }

    val bitmap = BitmapFactory.decodeByteArray(out.toByteArray(), 0, out.size())

    val isFrontCamera = cameraSelector == CameraSelector.DEFAULT_FRONT_CAMERA
    val rotationDegrees = imageInfo.rotationDegrees

    val matrix = Matrix().apply {
        // For front camera, we need to:
        // 1. Flip horizontally (mirror effect)
        // 2. Rotate based on device orientation
        if (isFrontCamera) {
            postScale(-1f, 1f, width / 2f, height / 2f) // Horizontal flip
        }

        // Correct rotation based on device orientation
        // Note: Front camera typically needs 270° rotation in portrait
        val correctedRotation = when {
            isFrontCamera -> (rotationDegrees + 180) % 360
            else -> rotationDegrees
        }
        postRotate(correctedRotation.toFloat())
    }

    return Bitmap.createBitmap(
        bitmap,
        0, 0,
        bitmap.width,
        bitmap.height,
        matrix,
        true
    ).also { bitmap.recycle() }
}

