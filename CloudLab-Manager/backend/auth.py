# auth.py  (FINAL VERSION)

import json
import os
import hashlib
import jwt
from functools import wraps
from flask import request, jsonify, g

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
SECRET_KEY = "CLOUDLAB_SUPER_SECRET_KEY"
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


# -------------------------------------------------
# Load / Save Users
# -------------------------------------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# -------------------------------------------------
# Password Security
# -------------------------------------------------
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------------------------
# User: Create + Verify
# -------------------------------------------------
def create_user(username: str, password: str):
    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": hash_password(password)
    }

    save_users(users)
    return True


def verify_user(username: str, password: str):
    users = load_users()
    if username not in users:
        return False

    return users[username]["password"] == hash_password(password)


# -------------------------------------------------
# JWT Token
# -------------------------------------------------
def generate_token(username):
    payload = {
        "username": username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_current_user():
    return getattr(g, "current_user", None)


# -------------------------------------------------
# Token Middleware
# -------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.current_user = data["username"]
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated
