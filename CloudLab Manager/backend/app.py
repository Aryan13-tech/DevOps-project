# app.py
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os, jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash


SECRET_KEY = "CLOUDLAB_SECRET_123"

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}})

_USERS = {}          # in-memory user store
_CONTAINERS = []     # in-memory container store

def create_token(username):
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }
    # PyJWT returns str for modern versions
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def require_auth(req):
    auth_header = req.headers.get("Authorization", "")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("user")
    except Exception:
        return None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:p>')
def staticfiles(p):
    return send_from_directory(app.static_folder, p)

# ---------------- AUTH ROUTES ---------------- #

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json or {}
    u = data.get("username")
    p = data.get("password")

    if not u or not p:
        return "Missing username/password", 400
    if u in _USERS:
        return "User already exists", 400

    _USERS[u] = generate_password_hash(p)
    return jsonify({"message": "registered"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    u = data.get("username")
    p = data.get("password")

    if u not in _USERS:
        return "User not found", 404
    if not check_password_hash(_USERS[u], p):
        return "Invalid password", 401

    token = create_token(u)
    return jsonify({"token": token, "username": u})


# ---------------- CONTAINER ROUTES ---------------- #

@app.route("/api/container/create", methods=["POST"])
def container_create():
    user = require_auth(request)
    if not user:
        return "Unauthorized", 401

    data = request.json or {}

    name = data.get("name") or data.get("image") or f"env-{len(_CONTAINERS)+1}"
    image = data.get("image") or "ubuntu:latest"

    container = {
        "name": name,
        "ContainerID": (name + "000000000")[:12],
        "Image": image,
        "Status": "running",
        "owner": user,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    _CONTAINERS.append(container)

    return jsonify({"message": "created", "name": name}), 201


@app.route("/api/container/list", methods=["GET"])
def container_list():
    user = require_auth(request)
    if not user:
        # For non-authenticated callers return empty list (frontend expects [])
        return jsonify([])

    # Return only containers owned by this user
    return jsonify([c for c in _CONTAINERS if c.get("owner") == user])


@app.route("/api/container/start/<name>", methods=["POST"])
def container_start(name):
    user = require_auth(request)
    if not user:
        return "Unauthorized", 401

    for c in _CONTAINERS:
        if c.get("name") == name and c.get("owner") == user:
            c["Status"] = "running"
            return jsonify({"message": "started"})
    return "Not found", 404


@app.route("/api/container/stop/<name>", methods=["POST"])
def container_stop(name):
    user = require_auth(request)
    if not user:
        return "Unauthorized", 401

    for c in _CONTAINERS:
        if c.get("name") == name and c.get("owner") == user:
            c["Status"] = "exited"
            return jsonify({"message": "stopped"})
    return "Not found", 404


@app.route("/api/container/delete/<name>", methods=["DELETE"])
def container_delete(name):
    user = require_auth(request)
    if not user:
        return "Unauthorized", 401

    global _CONTAINERS
    before = len(_CONTAINERS)
    _CONTAINERS = [
        c for c in _CONTAINERS
        if not (c.get("name") == name and c.get("owner") == user)
    ]
    if len(_CONTAINERS) < before:
        return jsonify({"message": "deleted"})
    return "Not found", 404


@app.route("/api/container/logs/<name>", methods=["GET"])
def container_logs(name):
    user = require_auth(request)
    if not user:
        return "Unauthorized", 401

    # Demo logs - replace with real docker logs later
    logs = f"Demo logs for {name}\nCreated by: {user}\n---\nLine 1\nLine 2\n"
    return Response(logs, mimetype="text/plain")


if __name__ == "__main__":
    # Helpful debug print on startup
    print(">>> STARTING app.py (pid:", os.getpid(), ")")
    app.run(host="0.0.0.0", port=8000, debug=True)
