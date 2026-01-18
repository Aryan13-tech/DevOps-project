from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import logging
import google.generativeai as genai
from error_rules import ERROR_RULES

# -------------------------
# Setup
# -------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_AVAILABLE = False

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True

app = Flask(__name__)
CORS(app)

# -------------------------
# Rule matcher
# -------------------------
def match_rule(error_text):
    for rule in ERROR_RULES:
        if rule["pattern"].search(error_text):
            return rule
    return None

# -------------------------
# AI fallback
# -------------------------
def analyze_with_gemini(error_text):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Respond ONLY in valid JSON:

{{
  "summary": "",
  "why_it_happened": [],
  "how_to_fix": [],
  "real_world_tip": ""
}}

Error:
{error_text}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])

# -------------------------
# API Route
# -------------------------
@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    data = request.get_json()
    error_text = data.get("error", "").strip()

    if not error_text:
        return jsonify({"success": False, "message": "No error provided"}), 400

    # Rule-based first
    rule = match_rule(error_text)
    if rule:
        return jsonify({
            "success": True,
            "error_category": rule["category"],
            "source": "rule-engine",
            "summary": rule["summary"],
            "why_it_happened": rule["why_it_happened"],
            "how_to_fix": rule["how_to_fix"],
            "real_world_tip": rule["real_world_tip"]
        })

    # AI fallback
    if GEMINI_AVAILABLE:
        try:
            ai = analyze_with_gemini(error_text)
            return jsonify({
                "success": True,
                "error_category": "Unknown / AI",
                "source": "gemini-ai",
                **ai
            })
        except Exception as e:
            logging.error(e)

    # Final fallback
    return jsonify({
        "success": True,
        "error_category": "Unknown",
        "source": "fallback",
        "summary": "The error could not be classified automatically.",
        "why_it_happened": ["The error is uncommon or malformed"],
        "how_to_fix": ["Check logs and official documentation"],
        "real_world_tip": "Production systems rely on monitoring and logs for unknown issues."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
