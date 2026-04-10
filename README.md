# FaceAPI Android Client

This branch contains the **Android frontend application** for the FaceAPI system, built using **Kotlin**.

⚠️ This is currently a **basic Android project setup** intended to act as the foundation for a real-time face recognition client.

---

## 🔗 Related Branches

* 🔹 Backend (BE/dev):
  https://github.com/nikh-iam/FaceAPI/tree/BE/dev

* 🔹 Main Project Overview:
  https://github.com/nikh-iam/FaceAPI

---

## 🧠 Purpose

This Android app is designed to:

* Capture camera input
* Send frames to backend via WebSocket
* Receive face recognition results
* Display results in real-time

🚧 **Note:** Full functionality (CameraX, WebSocket streaming, recognition UI) is **under development**.

---

## 🛠️ Tech Stack

* Kotlin
* Android SDK
* Gradle (Kotlin DSL)

---

## 📂 Project Structure

```id="s8fh2k"
FaceAPI/
 ├── app/                 # Main Android application module
 ├── gradle/              # Gradle configuration
 ├── build.gradle.kts     # Project build config
 ├── gradle.properties
 ├── gradlew
 └── settings.gradle.kts
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the frontend branch

```bash id="l2md9a"
git clone -b FE/dev https://github.com/nikh-iam/FaceAPI.git
cd FaceAPI
```

---

### 2️⃣ Open in Android Studio

* Open **Android Studio**
* Click **Open**
* Select the project folder

---

### 3️⃣ Sync Gradle

* Let Gradle sync automatically
* If not, click **"Sync Project with Gradle Files"**

---

### 4️⃣ Run the App

* Connect an Android device or start an emulator
* Click **Run ▶️**
* If running on a physical device manually,
```
# Check connected devices
adb devices

# Build the project
./gradlew build
```
---

## 🔄 Current Status

✅ Project initialized
✅ Gradle (Kotlin DSL) configured
✅ Basic Android structure ready

🚧 In Progress:

* Camera integration (CameraX)
* WebSocket communication
* Backend integration
* UI for recognition results

---

## 🔗 Backend Integration (Planned)

This app will connect to:

👉 https://github.com/nikh-iam/FaceAPI/tree/BE/dev

Planned flow:

1. User authentication
2. WebSocket connection
3. Frame streaming
4. Face recognition response handling

---

## 📌 Development Notes

* This branch is **frontend-only**
* Backend must be used for full functionality
* Designed for modular expansion

---

## 🔮 Future Enhancements

* CameraX real-time streaming
* WebSocket integration (OkHttp)
* Face detection overlays
* Liveness detection UI
* Jetpack Compose UI upgrade

---

## 🤝 Contribution

This branch is under active development. Contributions and improvements are welcome.

---

## 📌 Summary

This is the **Android client foundation** for the FaceAPI system, intended to evolve into a real-time face recognition interface connected to the backend.

---
