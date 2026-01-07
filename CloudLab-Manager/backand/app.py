from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import re

try:
    from google import genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# =============================
# Load env
# =============================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", 5000))

# =============================
# Flask app
# =============================
app = Flask(__name__)
CORS(app)

# =============================
# Gemini client
# =============================
client = None
if GEMINI_AVAILABLE and API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("✅ Gemini connected")
    except Exception as e:
        print("❌ Gemini init failed:", e)
        client = None

# =============================
# Health
# =============================
@app.route("/health")
def health():
    return jsonify({"status": "OK"})

# =============================
# Offline fallback
# =============================
def fallback_analysis(error):
    e = error.lower()

    if "no module named" in e:
        return {
            "explanation": "A required Python package is missing.",
            "causes": ["Dependency not installed", "Wrong virtual environment"],
            "solutions": ["Run pip install <package>", "Activate correct venv"]
        }

    if "exit code 1" in e:
        return {
            "explanation": "The process exited with a generic failure.",
            "causes": ["Command error", "Build/runtime failure"],
            "solutions": ["Check logs", "Run command manually"]
        }

    if "failed to pull image" in e:
        return {
            "explanation": "Container image could not be downloaded.",
            "causes": ["Wrong image name", "Private registry", "No internet"],
            "solutions": ["Check image name", "Login to registry", "Check network"]
        }

    return {
        "explanation": "This error could not be classified automatically.",
        "causes": ["Unknown or complex error"],
        "solutions": ["Search documentation", "Check logs"]
    }

# =============================
# Helper: extract JSON safely
# =============================
def extract_json(text):
    """
    Removes markdown and extra text, returns pure JSON
    """
    text = text.strip()

    # Remove ```json ``` wrappers
    text = re.sub(r"```json|```", "", text)

    # Extract first JSON object
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("No JSON found")

    return json.loads(match.group())

# =============================
# Analyze API
# =============================
@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    data = request.get_json()
    error_text = data.get("error", "").strip()

    if not error_text:
        return jsonify({"success": False, "message": "No error provided"}), 400

    # ===== TRY ONLINE (GEMINI) =====
    if client:
        try:
            prompt = f"""
You are a senior DevOps engineer.

Return ONLY JSON in this format:
{{
  "explanation": "...",
  "causes": ["..."],
  "solutions": ["..."]
}}

ERROR:
{error_text}
"""

            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=prompt
            )

            parsed = extract_json(response.text)

            return jsonify({
                "success": True,
                "source": "gemini",
                "explanation": parsed["explanation"],
                "causes": parsed["causes"],
                "solutions": parsed["solutions"]
            })

        except Exception as e:
            print("⚠️ Gemini failed:", e)

    # ===== OFFLINE FALLBACK =====
    result = fallback_analysis(error_text)
    return jsonify({
        "success": True,
        "source": "rule-based",
        **result
    })

# =============================
# Run
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
