import os
import docker
from flask import Flask, request, jsonify, Response, send_from_directory
from auth import (
    token_required,
    create_user,
    verify_user,
    generate_token,
    get_current_user,
)
from docker_service import (
    generate_dockerfile,
    build_image,
    run_container,
    stop_container,
    remove_container,
    get_logs,
    safe_tag,
)

app = Flask(__name__)

# Docker client
docker_client = docker.from_env()

# Memory storage
_CONTAINERS = []

# ----------------------------------------------------
# AUTH APIs
# ----------------------------------------------------
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if not create_user(username, password):
        return jsonify({"error": "Username already exists"}), 400

    return jsonify({"message": "User registered"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not verify_user(username, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username)
    return jsonify({"token": token, "username": username})


# ----------------------------------------------------
# UNIQUE CONTAINER NAME GENERATOR
# ----------------------------------------------------
def generate_unique_name(base="env"):
    number = 1
    while True:
        name = f"{base}-{number}"

        try:
            docker_client.containers.get(name)
            number += 1
            continue
        except docker.errors.NotFound:
            pass

        if any(c["name"] == name for c in _CONTAINERS):
            number += 1
            continue

        return name


# ----------------------------------------------------
# CREATE CONTAINER
# ----------------------------------------------------
@app.route("/api/container/create", methods=["POST"])
@token_required
def container_create():
    user = get_current_user()
    data = request.json or {}

    name = generate_unique_name()

    image = data.get("image") or "ubuntu:latest"
    commands = data.get("commands")
    cpu = data.get("cpu_limit")
    ram = data.get("ram_limit")
    port = data.get("port")

    if not port or not str(port).isdigit() or not (1 <= int(port) <= 65535):
        return jsonify({"error": "Invalid port"}), 400

    folder, tag = generate_dockerfile(safe_tag(name), image, commands)

    try:
        build_image(folder, tag)
    except Exception as e:
        return jsonify({"error": f"Image build failed: {e}"}), 500

    ports = {f"{port}/tcp": int(port)}

    try:
        container_obj = run_container(tag, name, ports, int(cpu) if cpu else None, ram)
    except Exception as e:
        return jsonify({"error": f"Run failed: {e}"}), 500

    entry = {
        "name": name,
        "ContainerID": container_obj.id[:12],
        "Image": tag,
        "Status": "running",
        "owner": user,
        "Port": port,
    }
    _CONTAINERS.append(entry)

    return jsonify({
        "message": "created",
        "name": name,
        "port": port,
        "id": container_obj.id
    }), 201


# ----------------------------------------------------
# LIST CONTAINERS
# ----------------------------------------------------
@app.route("/api/container/list", methods=["GET"])
@token_required
def list_containers():
    user = get_current_user()
    return jsonify([c for c in _CONTAINERS if c["owner"] == user])


# ----------------------------------------------------
# LOGS
# ----------------------------------------------------
@app.route("/api/container/logs/<name>", methods=["GET"])
@token_required
def logs(name):
    user = get_current_user()
    for c in _CONTAINERS:
        if c["name"] == name and c["owner"] == user:
            return Response(get_logs(c["ContainerID"]), mimetype="text/plain")
    return "Not found", 404


# ----------------------------------------------------
# STOP CONTAINER
# ----------------------------------------------------
@app.route("/api/container/stop/<name>", methods=["POST"])
@token_required
def stop(name):
    user = get_current_user()
    for c in _CONTAINERS:
        if c["name"] == name and c["owner"] == user:
            stop_container(c["ContainerID"])
            c["Status"] = "exited"
            return jsonify({"message": "stopped"})
    return "Not found", 404


# ----------------------------------------------------
# START CONTAINER
# ----------------------------------------------------
@app.route("/api/container/start/<name>", methods=["POST"])
@token_required
def start(name):
    user = get_current_user()
    for c in _CONTAINERS:
        if c["name"] == name and c["owner"] == user:

            port = c["Port"]
            mapping = {f"{port}/tcp": int(port)}

            try:
                new_c = run_container(c["Image"], c["name"], mapping)
                c["ContainerID"] = new_c.id[:12]
                c["Status"] = "running"
                return jsonify({"message": "started"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return "Not found", 404


# ----------------------------------------------------
# DELETE CONTAINER
# ----------------------------------------------------
@app.route("/api/container/delete/<name>", methods=["DELETE"])
@token_required
def delete(name):
    user = get_current_user()
    for c in list(_CONTAINERS):
        if c["name"] == name and c["owner"] == user:
            remove_container(c["ContainerID"], force=True)
            _CONTAINERS.remove(c)
            return jsonify({"message": "deleted"})
    return "Not found", 404


# ----------------------------------------------------
# Serve Frontend (STATIC FILES)  <-- PUT THIS LAST
# ----------------------------------------------------
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "..", "frontend")  # verify this name/case

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    # Protect API namespace from being served as static files
    if path.startswith("api"):
        return jsonify({"error": "API endpoint not found"}), 404

    # Serve index on root or fallback for SPA routes
    if path == "":
        return send_from_directory(FRONTEND_FOLDER, "index.html")

    # Try static file, fallback to index.html (for client routing)
    try:
        return send_from_directory(FRONTEND_FOLDER, path)
    except Exception:
        return send_from_directory(FRONTEND_FOLDER, "index.html")


# ----------------------------------------------------
# RUN SERVER
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
