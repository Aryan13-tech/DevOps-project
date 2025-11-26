# docker_service.py  (FINAL + WSL2 FIXED VERSION)

import os
import docker
from docker.errors import APIError, NotFound

# Docker client
client = docker.from_env()

# Location where generated Dockerfiles will be stored
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "Docker", "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


# -------------------------------------------------
# Safe Docker Image Tag
# -------------------------------------------------
def safe_tag(name):
    return name.lower().replace(":", "_").replace("/", "_")


# -------------------------------------------------
# Generate Dockerfile
# -------------------------------------------------
def generate_dockerfile(name, base_image="ubuntu:latest", commands=None):
    """
    Generates a folder + Dockerfile for each user environment.
    The Dockerfile is minimal and uses CMD so output appears in logs.
    """
    tag = name + "_img"
    folder = os.path.join(GENERATED_DIR, name)
    os.makedirs(folder, exist_ok=True)

    dockerfile_lines = [f"FROM {base_image}"]

    if commands:
        dockerfile_lines.append(f"CMD {commands}")
    else:
        # default → keep container alive
        dockerfile_lines.append('CMD ["sleep", "infinity"]')

    dockerfile_path = os.path.join(folder, "Dockerfile")

    with open(dockerfile_path, "w") as f:
        f.write("\n".join(dockerfile_lines))

    return folder, tag


# -------------------------------------------------
# Build Docker Image
# -------------------------------------------------
def build_image(path, tag):
    try:
        client.images.build(path=path, tag=tag, rm=True)
    except APIError as e:
        raise RuntimeError(f"Build failed: {str(e)}")


# -------------------------------------------------
# Run Container (WSL2 safe)
# -------------------------------------------------
def run_container(tag, name, ports=None, cpu_shares=None, mem_limit=None):
    """
    WSL2 FIX:
    - cpu_shares causes cgroup errors on Windows/WSL2
    - so we completely disable it.
    """
    try:
        container = client.containers.run(
            tag,
            name=name,
            detach=True,
            ports=ports or {},

            # -----------------------------
            # WSL2 FIX → disable CPU limits
            # -----------------------------
            cpu_shares=None,

            mem_limit=mem_limit,
        )
        return container

    except APIError as e:
        raise RuntimeError(f"Run failed: {str(e)}")


# -------------------------------------------------
# Stop Container
# -------------------------------------------------
def stop_container(container_id):
    try:
        c = client.containers.get(container_id)
        c.stop()
    except NotFound:
        pass
    except Exception:
        pass


# -------------------------------------------------
# Remove Container
# -------------------------------------------------
def remove_container(container_id, force=False):
    try:
        c = client.containers.get(container_id)
        c.remove(force=force)
    except NotFound:
        pass
    except Exception:
        pass


# -------------------------------------------------
# Get Container Logs
# -------------------------------------------------
def get_logs(container_id):
    try:
        c = client.containers.get(container_id)
        return c.logs().decode("utf-8", errors="ignore")
    except Exception:
        return "No logs (container not found)"
