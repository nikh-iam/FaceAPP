# FaceAPP – Real-Time Face Recognition System

FaceAPP is a **real-time face recognition system** built with a modular architecture consisting of:

* ⚙️ Backend (FastAPI + InsightFace)
* 📱 Frontend (Android Kotlin client)

This repository is organized into separate branches for backend and frontend development.

---

## 📂 Project Structure (Branches)

### 🔹 Backend (BE/dev)

👉 https://github.com/nikh-iam/FaceAPI/tree/BE/dev

* FastAPI-based server
* Face detection & recognition (InsightFace)
* FAISS-based embedding search
* Authentication workflow
* WebSocket-based streaming support

📘 Includes a detailed README for setup and usage.

---

### 🔹 Frontend (FE/dev)

👉 https://github.com/nikh-iam/FaceAPI/tree/FE/dev

* Android application built with Kotlin
* Acts as a client for backend communication
* Designed for real-time camera streaming and recognition

📘 Includes standalone setup instructions.

⚠️ Note: Frontend features like camera streaming and WebSocket integration are currently under development.

---

## 🚀 How to Run the Full System

### Step 1: Setup Backend

Follow instructions here:
👉 https://github.com/nikh-iam/FaceAPI/tree/BE/dev

---

### Step 2: Setup Frontend (Android)

Follow instructions here:
👉 https://github.com/nikh-iam/FaceAPI/tree/FE/dev

---

### Step 3: Start the System

1. Start the backend server (FastAPI)
2. Run the Android application
3. Connect the app to the backend
4. Begin face recognition workflow (once fully implemented)

---

## 🔄 System Workflow (Target Architecture)

1. Client (Android app) connects to backend
2. User authentication is performed
3. WebSocket connection is established
4. Camera frames are streamed to backend
5. Backend processes:

   * Face detection
   * Embedding extraction
   * Face recognition
6. Results are sent back to the client

---

## 🧩 Key Features

* ⚡ Real-time face recognition pipeline
* 🧠 FAISS-based high-performance similarity search
* 🔐 Authentication-first system design
* 📡 WebSocket-based communication
* 📊 Multi-face handling and validation

---

## 🏗️ Architecture Overview

```
Android Client (Kotlin)
        ↓
   WebSocket / API
        ↓
Backend (FastAPI)
        ↓
Face Recognition Pipeline
(InsightFace + FAISS)
```

---

## 📌 Notes

* Backend must be running before the frontend
* Ensure correct API and WebSocket endpoints are configured
* Frontend is currently in early development stage
* Designed for scalability and future production deployment

---

## 🔮 Future Scope

* Liveness detection (MediaPipe)
* Advanced Android UI (Jetpack Compose)
* Full real-time streaming implementation
* Cloud deployment (AWS / Docker)
* Database integration for user and session management

---

## 🤝 Contribution

Feel free to contribute to either branch:

* Backend → BE/dev
* Frontend → FE/dev

---

## ⭐ Summary

FaceAPP provides a **scalable foundation for building real-time face recognition systems**, with clear separation between backend processing and client-side interaction.

---
