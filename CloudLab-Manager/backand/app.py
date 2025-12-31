from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

# Load env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

@app.route("/test", methods=["GET"])
def test():
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Explain ModuleNotFoundError in simple words"
    )
    return jsonify({
        "response": response.text
    })

@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    data = request.json
    error_message = data.get("error")

    if not error_message:
        return jsonify({"error": "No error message provided"}), 400

    prompt = f"""
    Explain this error in simple words:
    {error_message}

    Also give:
    - Possible causes
    - Step-by-step solutions
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return jsonify({
        "analysis": response.text
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
