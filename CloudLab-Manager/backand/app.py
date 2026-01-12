from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import re
import logging

# =============================
# Gemini Import (Safe)
# =============================
try:
    from google import genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

# =============================
# Load Environment
# =============================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", 5000))
ENV = os.getenv("ENV", "development")

# =============================
# Flask App
# =============================
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# =============================
# Gemini Client
# =============================
client = None
if GEMINI_AVAILABLE and API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        logging.info("✅ Gemini AI connected successfully")
    except Exception as e:
        logging.error(f"❌ Gemini init failed: {e}")
        client = None
else:
    logging.warning("⚠️ Gemini not available — Demo mode will be used")

# =============================
# Health Check
# =============================
@app.route("/health")
def health():
    return jsonify({"status": "OK", "env": ENV})

# =============================
# Offline Rule-Based Engine
# =============================
def fallback_analysis(error: str):
    e = error.lower()

    if "no module named" in e:
        return {
            "explanation": "Python cannot find the required module.",
            "causes": [
                "The package is not installed",
                "Wrong virtual environment"
            ],
            "solutions": [
                "Run pip install <package>",
                "Activate correct virtual environment"
            ]
        }

    if "connection refused" in e:
        return {
            "explanation": "The application failed to connect to the server.",
            "causes": [
                "Backend server is not running",
                "Wrong host or port"
            ],
            "solutions": [
                "Start backend service",
                "Verify host and port"
            ]
        }

    if "unauthorized" in e or "401" in e:
        return {
            "explanation": "Authentication failed.",
            "causes": [
                "Invalid API key",
                "Expired credentials"
            ],
            "solutions": [
                "Regenerate API key",
                "Check authentication headers"
            ]
        }

    return {
        "explanation": "This error could not be classified automatically.",
        "causes": ["Unknown or complex error"],
        "solutions": [
            "Search official documentation",
            "Check application logs"
        ]
    }

# =============================
# Demo Gemini (SIMULATED AI)
# =============================
def demo_gemini_response(error_text: str):
    return {
        "success": True,
        "source": "gemini-demo",
        "explanation": (
            "This error indicates a complex or application-specific issue that "
            "is not covered by predefined rules. It usually occurs due to "
            "unexpected logic flow or invalid state transitions in the system."
        ),
        "causes": [
            "Unexpected state transition",
            "Race condition or concurrency issue",
            "Missing validation or error handling logic"
        ],
        "solutions": [
            "Review recent code changes related to this feature",
            "Add state validation and guard checks",
            "Improve logging around this operation"
        ]
    }

# =============================
# Helper: Safe JSON Extraction
# =============================
def extract_json(text: str):
    text = text.strip()
    text = re.sub(r"```json|```", "", text)
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("No JSON found in Gemini response")
    return json.loads(match.group())

# =============================
# Analyze Error API
# =============================
@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    data = request.get_json(silent=True) or {}
    error_text = data.get("error", "").strip()

    if not error_text:
        return jsonify({
            "success": False,
            "message": "No error provided"
        }), 400

    # ===== TRY REAL GEMINI =====
    if client:
        try:
            prompt = f"""
You are a senior software engineer and DevOps expert.

Analyze the error below and respond ONLY with valid JSON.

FORMAT:
{{
  "explanation": "string",
  "causes": ["string"],
  "solutions": ["string"]
}}

ERROR:
{error_text}
"""

            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=prompt
            )

            raw_text = response.text.strip()
            logging.info(f"🧠 Gemini raw response:\n{raw_text}")

            parsed = extract_json(raw_text)

            return jsonify({
                "success": True,
                "source": "gemini",
                "explanation": parsed.get("explanation"),
                "causes": parsed.get("causes", []),
                "solutions": parsed.get("solutions", [])
            })

        except Exception as e:
            logging.warning(f"⚠️ Gemini failed, using DEMO mode: {e}")
            return jsonify(demo_gemini_response(error_text))

    # ===== GEMINI NOT AVAILABLE → DEMO MODE =====
    logging.info("ℹ️ Using Gemini DEMO mode")
    return jsonify(demo_gemini_response(error_text))

# =============================
# Run Server
# =============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=(ENV == "development")
    )
