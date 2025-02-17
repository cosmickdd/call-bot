from flask import Flask, request # type: ignore
from twilio.twiml.voice_response import VoiceResponse # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Predefined answers for basic queries
FAQ_RESPONSES = {
    "what is your name": "My name is AI Assistant.",
    "who are you": "I am an AI call assistant designed to provide information about UTKARSH.",
    "what do you do": "I help answer questions about my creator.",
    "how can I contact you": "You can contact my creator via Ut0543700@gmail.com or as @cosmickdd on all social media.",
    "where are you located": "Currently, I am based online and available 24/7!"
}

@app.route("/", methods=['GET'])
def home():
    return "AI Call Center is Running!"

@app.route("/voice", methods=['POST'])
def voice():
    """Handles incoming voice calls and records user input"""
    response = VoiceResponse()
    response.say("Hello! You can ask me anything about my creator. Please speak after the beep.")
    
    # Record user's voice and transcribe it
    response.record(timeout=5, transcribe=True, transcribe_callback="/transcription")
    
    return str(response)

@app.route("/transcription", methods=['POST'])
def transcription():
    """Processes the transcribed text and provides a relevant response"""
    user_text = request.form.get("TranscriptionText", "").lower()
    print(f"User said: {user_text}")

    # Check if question is in predefined FAQ
    response_text = "I'm sorry, I didn't understand that."
    for question, answer in FAQ_RESPONSES.items():
        if question in user_text:
            response_text = answer
            break

    # Generate Twilio Voice response
    response = VoiceResponse()
    response.say(response_text)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
