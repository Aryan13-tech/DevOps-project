import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Docker service functions
from docker_service import get_dashboard_stats, get_container_list

app = Flask(__name__)
CORS(app)

# Absolute path for users.json (IMPORTANT FIX)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# Ensure users.json exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# ---------- Helper Functions ----------
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- Auth APIs ----------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    users = load_users()
    if any(u["username"] == username for u in users):
        return jsonify({"success": False, "message": "User already exists"}), 400

    users.append({
        "username": username,
        "password": password
    })
    save_users(users)

    return jsonify({"success": True, "message": "Registration successful"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    user = next(
        (u for u in users if u["username"] == username and u["password"] == password),
        None
    )

    if user:
        return jsonify({"success": True, "message": "Login successful"})

    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# ---------- Dashboard APIs ----------
@app.route("/api/dashboard", methods=["GET"])
def dashboard_stats():
    return jsonify(get_dashboard_stats())

@app.route("/api/containers", methods=["GET"])
def containers_list():
    return jsonify(get_container_list())

# ---------- App Entry Point ----------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
