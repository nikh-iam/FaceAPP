package com.example.faceapi

import android.graphics.Bitmap
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.*
import okio.ByteString
import okio.ByteString.Companion.toByteString
import org.json.JSONArray
import java.io.ByteArrayOutputStream

class FaceRecognitionViewModel : ViewModel() {
    private val _hasCameraPermission = MutableStateFlow(false)
    val hasCameraPermission: StateFlow<Boolean> = _hasCameraPermission.asStateFlow()

    private val _isConnected = MutableStateFlow(false)
    val isConnected: StateFlow<Boolean> = _isConnected.asStateFlow()

    private val _lastDetection = MutableStateFlow("")
    val lastDetection: StateFlow<String> = _lastDetection.asStateFlow()

    private val client = OkHttpClient()
    private var webSocket: WebSocket? = null

    init {
        connectWebSocket()
    }

    fun updateCameraPermission(granted: Boolean) {
        _hasCameraPermission.value = granted
    }

    fun connectWebSocket() {
        viewModelScope.launch {
            try {
                val request = Request.Builder()
                    .url("ws://127.0.0.1:8000/ws")
                    .build()
                webSocket = client.newWebSocket(request, object : WebSocketListener() {
                    override fun onOpen(webSocket: WebSocket, response: Response) {
                        _isConnected.value = true
                    }

                    override fun onMessage(webSocket: WebSocket, text: String) {
                        processServerResponse(text)
                    }

                    override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                        _isConnected.value = false
                    }

                    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                        _isConnected.value = false
                        Log.e("WebSocket", "Error: ${t.message}", t)
                    }
                })
            } catch (e: Exception) {
                Log.e("WebSocket", "Connection Error", e)
                _isConnected.value = false
            }
        }
    }

    private fun processServerResponse(text: String) {
        try {
            val jsonArray = JSONArray(text)
            val result = StringBuilder()

            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                result.append("${obj.getString("label")}\n")
            }

            _lastDetection.value = jsonArray.toString().trim()
        } catch (e: Exception) {
            Log.e("FaceRecognition", "Error parsing JSON", e)
        }
    }

    fun sendImage(bitmap: Bitmap) {
        viewModelScope.launch {
            Log.d("Send Image", "Preparing for image transmission")
            try {
                if (webSocket == null || !_isConnected.value) {
                    Log.e("FaceRecognition", "WebSocket is not connected")
                    return@launch
                }

                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 90, stream)
                val byteArray = stream.toByteArray()

                // Convert ByteArray to ByteString before sending
                val byteString = byteArray.toByteString()
                webSocket?.send(byteString)

            } catch (e: Exception) {
                Log.e("FaceRecognition", "Error sending image", e)
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        webSocket?.close(1000, "ViewModel cleared")
        client.dispatcher.executorService.shutdown()
    }
}
