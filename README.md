# FaceAPI
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/nikh-iam/FaceAPI)

FaceAPI is a real-time face recognition backend built with FastAPI. It leverages the `insightface` library for high-accuracy face detection and recognition, providing a robust solution for identity verification systems via a simple WebSocket interface.

## Features

-   **Real-Time Recognition**: Processes video frames for face detection and identification in real-time.
-   **High Accuracy**: Utilizes the `insightface` toolkit (`buffalo_s` model) for state-of-the-art performance.
-   **WebSocket API**: Enables seamless, low-latency communication for streaming applications.
-   **Scalable & Modular**: Built with a clean service-oriented architecture for easy extension and maintenance.
-   **Easy Setup**: Includes a script to easily build and manage your own face database.

## How It Works

1.  **Embedding Extraction**: A provided script (`extract_embeddings.py`) processes a directory of images (`faces_db`). For each person, it generates an average face embedding (a vector representation of the face) and saves it.
2.  **Server Initialization**: On startup, the FastAPI server loads all the pre-computed face embeddings from the `face_embeddings` directory into memory.
3.  **Real-Time Processing**: The client sends image frames via a WebSocket connection. For each frame, the server detects faces, extracts their embeddings, and compares them against the loaded embeddings using cosine similarity to find the best match.
4.  **Response**: The server sends back a JSON object containing the labels of the recognized faces.

## Setup and Installation

Follow these steps to get the FaceAPI server running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/nikh-iam/faceapi.git
cd faceapi
```

### 2. Install Dependencies

Ensure you have Python 3.8 or higher installed. Then, install the required packages using pip.

```bash
pip install -r requirements.txt
```

### 3. Build the Face Database

You need to provide images for the identities you want to recognize.

1.  Create a directory named `faces_db`.
2.  Inside `faces_db`, create a subdirectory for each person you want to add. The subdirectory name will be used as the person's label (e.g., `john_doe`).
3.  Place one or more clear images of the person inside their respective subdirectory. The script works best when images contain only one face.

Your directory structure should look like this:

```
faceapi/
├── faces_db/
│   ├── person_one/
│   │   ├── image1.jpg
│   │   └── image2.png
│   └── person_two/
│       ├── image3.jpg
│       └── image4.jpeg
└── ... (other project files)
```

### 4. Generate Face Embeddings

Run the `extract_embeddings.py` script to process the images in `faces_db` and generate the embedding files. These will be saved in the `face_embeddings` directory.

```bash
python extract_embeddings.py
```
This script will detect new persons in the `faces_db` directory, compute their average face embeddings, and save them as `.pkl` files.

### 5. Start the Server

Run the `main.py` script to start the FastAPI server.

```bash
python main.py
```

The server will be running on `http://0.0.0.0:8000`.

## API Usage

The server exposes two main endpoints: an HTTP endpoint for status checks and a WebSocket endpoint for face recognition.

### Status Check

You can check if the server is running and has loaded the face identities by sending a `GET` request to the root URL.

**Request:**
`GET http://0.0.0.0:8000/`

**Success Response (Status 200):**
Indicates the server is running and provides a count of the loaded identities.
```json
{
  "status": "Face Recognition Server is running",
  "faces_uploaded_count": 2
}
```

**Error Response (Status 503):**
Indicates that the server is running but no face embeddings were found. Ensure you have successfully run the `extract_embeddings.py` script.
```json
{
  "status_message": "Server not ready. No available faces found, please upload.",
  "no_faces_uploaded": 0
}
```

### Face Recognition (WebSocket)

The primary functionality is exposed via a WebSocket endpoint for real-time communication.

**Endpoint:**
`ws://0.0.0.0:8000/ws`

**Client to Server:**
Connect to the WebSocket endpoint and send image frames as raw **bytes**.

**Server to Client:**
The server responds with a JSON array containing the recognized faces. Each object in the array includes the label of the identified person. If a face is detected but not recognized, its label will be "Unknown".

**Example Response:**
```json
[
  {
    "label": "person_one"
  },
  {
    "label": "Unknown"
  }
]
```
If no faces are detected in a frame, the server will respond with an error message:
```json
{
  "error": "No valid face detected",
  "code": 404
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
