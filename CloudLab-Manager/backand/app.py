from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

# Load env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", 5000))

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

# Gemini client
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "message": "Backend is running"
    })

# AI analysis
@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    data = request.get_json()
    if not data or "error" not in data:
        return jsonify({"success": False, "error": "No error provided"}), 400

    prompt = f"""
Explain this error in simple words.

ERROR:
{data['error']}

Give:
1. Explanation
2. Causes
3. Fix steps
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return jsonify({
        "success": True,
        "analysis": response.text
    })

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
