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
    logging.warning("⚠️ Gemini not available (API key missing or SDK issue)")

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
# Helper: Safe JSON Extraction
# =============================
def extract_json(text: str):
    """
    Extract JSON safely even if Gemini adds text around it
    """
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

    # ===== TRY GEMINI (ONLINE AI) =====
    if client:
        try:
            prompt = f"""
You are a senior software engineer and DevOps expert.

Analyze the error below and respond ONLY with valid JSON.
DO NOT add explanations outside JSON.

JSON FORMAT (MANDATORY):
{{
  "explanation": "Clear explanation in simple language",
  "causes": ["Cause 1", "Cause 2"],
  "solutions": ["Solution 1", "Solution 2"]
}}

ERROR MESSAGE:
{error_text}
"""

            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=prompt
            )

            raw_text = response.text.strip()
            logging.info(f"🧠 Gemini raw response:\n{raw_text}")

            try:
                parsed = extract_json(raw_text)
            except Exception:
                logging.warning("⚠️ Gemini JSON parse failed, returning safe fallback")

                return jsonify({
                    "success": True,
                    "source": "gemini",
                    "explanation": raw_text[:600],
                    "causes": [
                        "Complex or application-specific issue",
                        "State or logic mismatch"
                    ],
                    "solutions": [
                        "Check logs around this error",
                        "Review recent code changes",
                        "Add validation and error handling"
                    ]
                })

            return jsonify({
                "success": True,
                "source": "gemini",
                "explanation": parsed.get("explanation", "No explanation provided"),
                "causes": parsed.get("causes", []),
                "solutions": parsed.get("solutions", [])
            })

        except Exception as e:
            logging.error(f"❌ Gemini failed: {e}")

    # ===== OFFLINE FALLBACK =====
    result = fallback_analysis(error_text)
    return jsonify({
        "success": True,
        "source": "rule-based",
        "explanation": result["explanation"],
        "causes": result["causes"],
        "solutions": result["solutions"]
    })

# =============================
# Run Server
# =============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=(ENV == "development")
    )
