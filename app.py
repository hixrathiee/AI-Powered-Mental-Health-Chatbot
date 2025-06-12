from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from flask_cors import CORS

app = Flask(__name__, static_folder='static')  # static folder for frontend assets
CORS(app)

# Load your saved model and tokenizer
MODEL_PATH = Path(__file__).parent / "emotion_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()

# Emotion labels - confirm order matches your model!
EMOTIONS = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']

# Keyword lists to improve classification reliability
emotion_keywords = {
    "sadness": ["sad", "unhappy", "depressed", "cry"],
    "joy": ["happy", "joy", "glad", "delighted"],
    "anger": ["angry", "mad", "furious", "annoyed"],
    "disgust": ["disgusted", "gross", "nasty", "ew"],
    "fear": ["scared", "afraid", "fearful", "nervous"],
    "neutral": [],
    "surprise": ["surprised", "shocked", "amazed"]
} 

# Emotion-based responses with suggestions
responses = {
    "sadness": {
        "default": "I'm sorry you're feeling this way. Would you like to talk about what's bothering you?",
        "suggestion": "You could try journaling your thoughts or reaching out to a close friend for support."
    },
    "joy": {
        "default": "This is wonderful to hear! What specifically is bringing you joy right now?",
        "suggestion": "How about sharing your happiness with others or trying a new activity to celebrate?"
    },
    "anger": {
        "default": "I sense this situation is upsetting you. Would it help to talk through it calmly?",
        "suggestion": "Consider trying deep breathing exercises or physical activity like punching a pillow to release tension."
    },
    "disgust": {
        "default": "That sounds really unpleasant. I'm here to listen if you want to share more details.",
        "suggestion": "You might want to distance yourself from the situation and focus on something uplifting."
    },
    "fear": {
        "default": "It's completely normal to feel apprehensive. Remember you're safe here.",
        "suggestion": "Try grounding techniques: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
    },
    "neutral": {
        "default": "Thank you for sharing. Is there anything specific you'd like to discuss?",
        "suggestion": "How about trying a mindfulness exercise or exploring a new hobby today?"
    },
    "surprise": {
        "default": "Unexpected situations can be challenging. Would you like to explore this further?",
        "suggestion": "Try writing down your thoughts to process the surprise, or discuss it with someone you trust."
    }
}

def keyword_override(text, predicted_emotion, confidence):
    text_lower = text.lower()
    for emo, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            if emo != predicted_emotion or confidence < 0.5:
                return emo
    return predicted_emotion

def generate_response(user_input, emotion):
    suggestion_triggers = ['suggest', 'advice', 'help', 'what should i do', 'recommend', 'tips']
    wants_suggestion = any(trigger in user_input.lower() for trigger in suggestion_triggers)

    if wants_suggestion:
        return responses[emotion].get('suggestion', "Try taking deep breaths and focusing on the present moment.")
    return responses[emotion].get('default', "Thank you for sharing. How can I support you today?")

# Serve index.html from static folder on root
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# API endpoint for chat messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        if not message:
            return jsonify({"response": "Please enter a message.", "emotion": None}), 400

        inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            conf, pred = torch.max(probs, dim=1)
            emotion = EMOTIONS[pred.item()]
            confidence = conf.item()

        # Apply keyword override logic
        emotion = keyword_override(message, emotion, confidence)

        # Generate response based on detected emotion and user input
        response = generate_response(message, emotion)

        return jsonify({"response": response, "emotion": emotion})

    except Exception as e:
        return jsonify({"response": "Something went wrong. Please try again later.", "emotion": None, "error": str(e)}), 500

# 404 handler for unmatched routes
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
