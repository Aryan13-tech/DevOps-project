import docker
from datetime import datetime

# Initialize Docker client
client = docker.from_env()

# ---------- Dashboard Stats ----------
def get_dashboard_stats():
    containers = client.containers.list(all=True)
    running = [c for c in containers if c.status == "running"]

    return {
        "total_labs": len(containers),
        "running_containers": len(running)
    }

# ---------- Containers List ----------
def get_container_list():
    result = []

    containers = client.containers.list(all=True)

    for c in containers:
        uptime = "N/A"

        if c.status == "running":
            started_at = c.attrs["State"]["StartedAt"]
            start_time = datetime.fromisoformat(started_at.replace("Z", ""))
            uptime = str(datetime.utcnow() - start_time).split(".")[0]

        result.append({
            "name": c.name,
            "image": c.image.tags[0] if c.image.tags else "unknown",
            "status": c.status,
            "uptime": uptime
        })

    return result
