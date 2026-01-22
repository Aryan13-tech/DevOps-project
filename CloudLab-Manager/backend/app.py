from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import logging
import time
from error_rules import ERROR_RULES

# =========================
# PROMETHEUS IMPORTS
# =========================
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# =========================
# Setup
# =========================
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_AVAILABLE = False
client = None
types = None

# -------------------------
# Initialize Gemini (SAFE)
# -------------------------
if GEMINI_API_KEY:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
        logging.info("Gemini AI enabled")
    except Exception as e:
        GEMINI_AVAILABLE = False
        logging.warning("Gemini disabled safely: %s", e)
else:
    logging.info("GEMINI_API_KEY not set — running in rule-only mode")

app = Flask(__name__)
CORS(app)

# =========================
# PROMETHEUS METRICS
# =========================

REQUEST_COUNT = Counter(
    "cloudlab_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "cloudlab_http_request_latency_seconds",
    "HTTP request latency",
    ["endpoint"]
)

ERROR_ANALYSIS_COUNT = Counter(
    "cloudlab_error_analysis_total",
    "Total error analysis requests",
    ["source"]
)

# =========================
# Global Request Tracking
# =========================
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    resp_time = time.time() - getattr(request, "start_time", time.time())
    endpoint = request.path

    REQUEST_COUNT.labels(
        request.method,
        endpoint,
        response.status_code
    ).inc()

    REQUEST_LATENCY.labels(endpoint=endpoint).observe(resp_time)

    return response

# =========================
# Rule matcher
# =========================
def match_rule(error_text: str):
    for rule in ERROR_RULES:
        if rule["pattern"].search(error_text):
            return rule
    return None

# =========================
# AI fallback
# =========================
def analyze_with_gemini(error_text: str):
    if not client or not types:
        raise RuntimeError("Gemini client not initialized")

    prompt = f"""
You are a senior software engineer.

Respond ONLY in valid JSON exactly in this format:

{{
  "summary": "short explanation",
  "why_it_happened": ["reason 1", "reason 2"],
  "how_to_fix": ["step 1", "step 2"],
  "real_world_tip": "practical production advice"
}}

Error:
{error_text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=512,
        ),
    )

    if not response or not getattr(response, "text", None):
        raise ValueError("Empty AI response")

    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("AI returned non-JSON output")

    return json.loads(text[start:end])

# =========================
# Health check
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "ai_available": GEMINI_AVAILABLE
    })

# =========================
# METRICS ENDPOINT ✅ FIXED
# =========================
@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# =========================
# Main API Route
# =========================
@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid JSON payload"
        }), 400

    error_text = str(data.get("error", "")).strip()

    if not error_text:
        return jsonify({
            "success": False,
            "message": "No error provided"
        }), 400

    rule = match_rule(error_text)
    if rule:
        ERROR_ANALYSIS_COUNT.labels(source="rule-engine").inc()
        return jsonify({
            "success": True,
            "error_category": rule["category"],
            "source": "rule-engine",
            "summary": rule["summary"],
            "why_it_happened": rule["why_it_happened"],
            "how_to_fix": rule["how_to_fix"],
            "real_world_tip": rule["real_world_tip"]
        })

    if GEMINI_AVAILABLE:
        try:
            ai = analyze_with_gemini(error_text)
            ERROR_ANALYSIS_COUNT.labels(source="gemini-ai").inc()
            return jsonify({
                "success": True,
                "error_category": "Unknown / AI",
                "source": "gemini-ai",
                "summary": ai.get("summary", ""),
                "why_it_happened": ai.get("why_it_happened", []),
                "how_to_fix": ai.get("how_to_fix", []),
                "real_world_tip": ai.get("real_world_tip", "")
            })
        except Exception as e:
            logging.warning("AI failed safely: %s", e)

    ERROR_ANALYSIS_COUNT.labels(source="fallback").inc()
    return jsonify({
        "success": True,
        "error_category": "Unknown",
        "source": "fallback",
        "summary": "The error could not be classified automatically.",
        "why_it_happened": [
            "The error is uncommon, incomplete, or not yet in the rule base"
        ],
        "how_to_fix": [
            "Check application logs",
            "Search official documentation",
            "Add a new rule if this error repeats"
        ],
        "real_world_tip": "Production systems improve by converting repeated unknown errors into rules."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
