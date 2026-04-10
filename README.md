## FaceServer  
[📄 View Documentation](https://docs.google.com/document/d/1K3CEjjBcdOEUCAMlSaeYWp8-r5Uyj-Q8hgMIiTWSH-4/edit?usp=sharing)  
[🌐 Public API](http://202.191.66.163:2215/)

FaceServer is a real-time face recognition backend powered by FastAPI, supporting both HTTP and WebSocket protocols. It includes anti-spoofing and depth verification mechanisms, making it ideal for secure identity verification systems.

---

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone http://gitserver/t0667/faceserver.git
cd faceserver
```

#### 2. Install Dependencies
Make sure you have Python 3.8+ installed. Then install required packages:
```bash
pip install -r requirements.txt
```

#### 3. Start the Server
Run the server using the following command:
```bash
python main.py
```
This will start the FastAPI server on `http://0.0.0.0:8000`

---

### WebSocket API Usage

To integrate face recognition into your frontend:

- Connect to the WebSocket endpoint:
```txt
ws://0.0.0.0:8000/ws
```

- Send image frames in `bytes` format.
- The server will respond with an array of detected face labels:
```json
[
  {"label": "person1"},
  {"label": "person2"}
]
```

---

### Server Status Check

You can verify the server status by visiting:

```
GET http://0.0.0.0:8000/
```

---

### Features

- Real-time face detection and recognition
- WebSocket support for seamless streaming
- Modular architecture for easy extension
- Easier debugging