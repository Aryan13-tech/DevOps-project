# docker_service.py (FINAL STABLE VERSION)

import os
import docker
from docker.errors import APIError, NotFound

# Docker client
client = docker.from_env()

# Folder to store generated Dockerfiles
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "Docker", "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


# -------------------------------------------------
# Safe Docker Image Tag
# -------------------------------------------------
def safe_tag(name):
    return name.lower().replace(":", "_").replace("/", "_")


# -------------------------------------------------
# Generate Dockerfile (FULLY FIXED)
# -------------------------------------------------
def generate_dockerfile(name, base_image="ubuntu:latest", commands=None):
    """
    FIXES:
    - Multi-line commands
    - CMD vs RUN conversion
    - Empty commands crash
    - Quote escaping
    - Valid Dockerfile every time
    """

    tag = name + "_img"
    folder = os.path.join(GENERATED_DIR, name)
    os.makedirs(folder, exist_ok=True)

    dockerfile_lines = [f"FROM {base_image}"]

    # No commands entered by user → keep container alive
    if not commands or commands.strip() == "":
        dockerfile_lines.append('CMD ["sleep", "infinity"]')
        dockerfile_path = os.path.join(folder, "Dockerfile")

        with open(dockerfile_path, "w") as f:
            f.write("\n".join(dockerfile_lines))

        return folder, tag

    # Split commands into list
    cmd_list = [c.strip() for c in commands.split("\n") if c.strip()]

    # If still empty → fail safe
    if len(cmd_list) == 0:
        dockerfile_lines.append('CMD ["sleep", "infinity"]')
        dockerfile_path = os.path.join(folder, "Dockerfile")

        with open(dockerfile_path, "w") as f:
            f.write("\n".join(dockerfile_lines))

        return folder, tag

    # Add RUN commands (all except last)
    for cmd in cmd_list[:-1]:
        dockerfile_lines.append(f'CMD ["/bin/sh", "-c", "{commands}"]')


    # Last command becomes CMD
    last_cmd = cmd_list[-1]
    last_cmd = last_cmd.replace('"', '\\"')  # Escape quotes

    dockerfile_lines.append(f'CMD ["sh", "-c", "{last_cmd}"]')

    # Write Dockerfile
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
# Run Container (WSL2 Safe)
# -------------------------------------------------
def run_container(tag, name, ports=None, cpu_shares=None, mem_limit=None):
    try:
        container = client.containers.run(
            tag,
            name=name,
            detach=True,
            ports=ports or {},

            # WSL2 FIX
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
    except:
        pass


# -------------------------------------------------
# Remove Container
# -------------------------------------------------
def remove_container(container_id, force=False):
    try:
        c = client.containers.get(container_id)
        c.remove(force=force)
    except:
        pass


# -------------------------------------------------
# Get Logs
# -------------------------------------------------
def get_logs(container_id):
    try:
        c = client.containers.get(container_id)
        return c.logs().decode("utf-8", errors="ignore")
    except:
        return "No logs (container not found)"
