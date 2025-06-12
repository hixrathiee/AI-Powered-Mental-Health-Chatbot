# AI-Powered Mental Health Chatbot 🤖🧠💬

A personalized conversational agent designed to support mental well-being by detecting user emotions and responding with empathetic and helpful replies. This project integrates deep learning for emotion detection and natural language processing (NLP) for generating meaningful conversations.

## 🚀 Features

- 🗣️ Emotion Detection from User Input (Text)
- 🤗 Empathetic and supportive chatbot responses
- 🔍 Real-time conversation flow
- 💻 Easy to run locally
- 🔒 Model files excluded (to prevent large file errors)

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **AI/ML:** PyTorch (Emotion Detection Model)
- **NLP Model:** BERT
- **Version Control:** Git & GitHub
- **Others:** Git LFS (for large model handling - model not included)

## 📦 Folder Structure

 backend/
│ ├── app.py # Backend server code
│ ├── model/ # ML model files
│ └── requirements.txt # Python dependencies
│
├── frontend/
│ ├── index.html # Frontend HTML
│ ├── style.css # CSS styling
│ └── script.js # Chatbot frontend logic
│
└── .gitignore # Ignoring large model files
 ## Note
The ML model files (.safetensors) are excluded from this repository to avoid GitHub file size limits. You can train or download your own models and place them in the backend/emotion_model/ folder.
