package com.example.faceapi

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            FaceRecognitionApp()
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FaceRecognitionApp() {
    val viewModel: FaceRecognitionViewModel = viewModel()
    val context = LocalContext.current
    val hasPermission = remember { mutableStateOf(false) }

    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasPermission.value = isGranted
        viewModel.updateCameraPermission(isGranted)
    }

    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            hasPermission.value = true
            viewModel.updateCameraPermission(true)
        } else {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    MaterialTheme {
        Scaffold(
            topBar = {
                CenterAlignedTopAppBar(
                    title = {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Face Recognition") // Main title

                            Text(
                                text = "Server: " + if (viewModel.isConnected.collectAsState().value) "Connected" else "Failed to connect",
                                color = if (viewModel.isConnected.collectAsState().value)
                                    MaterialTheme.colorScheme.primary
                                else
                                    MaterialTheme.colorScheme.error,
                                style = MaterialTheme.typography.bodySmall
                            )

                            if (viewModel.lastDetection.collectAsState().value.isNotEmpty()) {
                                Text(
                                    text = "Response from server: ${viewModel.lastDetection.collectAsState().value}",
                                    style = MaterialTheme.typography.bodySmall
                                )
                            }
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier.fillMaxSize().padding(padding),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                if (hasPermission.value) {
                    CameraPreview(viewModel = viewModel)
                } else {
                    Text("Camera permission required")
                }

                Spacer(Modifier.height(16.dp))


            }
        }
    }
}

