const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

/* =========================
   TEST API
========================= */
app.get("/", (req, res) => {
  res.json({ message: "CloudLab Manager Backend is running 🚀" });
});

/* =========================
   CREATE ENVIRONMENT
========================= */
app.post("/create-env", (req, res) => {
  const { image, port, command } = req.body;

  if (!image || !port || !command) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const containerName = `cloudlab_${Date.now()}`;

  // IMPORTANT: keep container alive using tail -f
  const dockerCmd = `
    docker run -d \
    --name ${containerName} \
    -p ${port}:${port} \
    --label cloudlab=true \
    ${image} sh -c "${command} && tail -f /dev/null"
  `;

  exec(dockerCmd, (error, stdout, stderr) => {
    if (error) {
      console.error(stderr);
      return res.status(500).json({
        error: "Failed to create Docker environment",
        details: stderr
      });
    }

    res.json({
      message: "Environment created successfully",
      containerId: stdout.trim(),
      containerName
    });
  });
});

/* =========================
   LIST ENVIRONMENTS
========================= */
app.get("/envs", (req, res) => {
  const cmd = `
    docker ps -a \
    --filter "label=cloudlab=true" \
    --format "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}"
  `;

  exec(cmd, (error, stdout) => {
    if (error) {
      return res.status(500).json({ error: "Failed to list environments" });
    }

    if (!stdout.trim()) {
      return res.json([]);
    }

    const envs = stdout
      .trim()
      .split("\n")
      .map(line => {
        const [id, name, image, status, ports] = line.split("|");
        return { id, name, image, status, ports };
      });

    res.json(envs);
  });
});

/* =========================
   START ENVIRONMENT
========================= */
app.post("/start-env", (req, res) => {
  const { id } = req.body;

  if (!id) {
    return res.status(400).json({ error: "Container ID required" });
  }

  exec(`docker start ${id}`, (error) => {
    if (error) {
      return res.status(500).json({ error: "Failed to start container" });
    }
    res.json({ message: "Container started successfully" });
  });
});

/* =========================
   STOP ENVIRONMENT
========================= */
app.post("/stop-env", (req, res) => {
  const { id } = req.body;

  if (!id) {
    return res.status(400).json({ error: "Container ID required" });
  }

  exec(`docker stop ${id}`, (error) => {
    if (error) {
      return res.status(500).json({ error: "Failed to stop container" });
    }
    res.json({ message: "Container stopped successfully" });
  });
});

/* =========================
   DELETE ENVIRONMENT
========================= */
app.delete("/delete-env", (req, res) => {
  const { id } = req.body;

  if (!id) {
    return res.status(400).json({ error: "Container ID required" });
  }

  exec(`docker rm -f ${id}`, (error) => {
    if (error) {
      return res.status(500).json({ error: "Failed to delete container" });
    }
    res.json({ message: "Container deleted successfully" });
  });
});

/* =========================
   START SERVER
========================= */
app.listen(PORT, () => {
  console.log(`✅ Backend running on http://localhost:${PORT}`);
});
