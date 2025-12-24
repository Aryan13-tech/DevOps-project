/***********************
 * DOM ELEMENTS
 ***********************/
const authModal = document.getElementById("authModal");
const modalTitle = document.getElementById("modalTitle");

const imageEl = document.getElementById("image");
const cpuEl = document.getElementById("cpu");
const ramEl = document.getElementById("ram");
const portEl = document.getElementById("port");
const commandEl = document.getElementById("command");

const createBtn = document.querySelector(".left button");
const envList = document.getElementById("envList");

/***********************
 * STATE
 ***********************/
let environments = [];

/***********************
 * LOGIN / REGISTER
 ***********************/
function openModal(type) {
  authModal.style.display = "flex";
  modalTitle.innerText = type === "login" ? "Login" : "Register";
}

function closeModal() {
  authModal.style.display = "none";
}

/***********************
 * CREATE ENV
 ***********************/
async function createEnv() {
  const image = imageEl.value;
  const cpu = cpuEl.value.trim();
  const ram = ramEl.value.trim();
  const port = portEl.value.trim();
  const command = commandEl.value.trim();

  if (!cpu || !ram || !port || !command) {
    alert("Please fill all fields");
    return;
  }

  createBtn.disabled = true;
  createBtn.innerText = "Creating...";

  try {
    const res = await fetch("http://localhost:5000/create-env", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image, port, command })
    });

    const data = await res.json();

    environments.push({
      id: data.containerName,
      image,
      cpu,
      ram,
      port,
      status: "Starting"
    });

    renderEnvs();
  } catch (err) {
    alert("Failed to create environment");
    console.error(err);
  }

  createBtn.disabled = false;
  createBtn.innerText = "Create Environment";
}

/***********************
 * RENDER
 ***********************/
function renderEnvs() {
  envList.innerHTML = "";

  if (environments.length === 0) {
    envList.innerHTML = `<p class="empty">No environment created yet.</p>`;
    return;
  }

  environments.forEach(env => {
    const div = document.createElement("div");
    div.className = "env-card";

    div.innerHTML = `
      <p><b>Image:</b> ${env.image}</p>
      <p><b>CPU:</b> ${env.cpu}</p>
      <p><b>RAM:</b> ${env.ram} MB</p>
      <p><b>Status:</b> <span class="status">${env.status}</span></p>

      <div class="actions">
        <button class="btn start" onclick="startEnv('${env.id}')">Start</button>
        <button class="btn stop" onclick="stopEnv('${env.id}')">Stop</button>
        <button class="btn delete" onclick="deleteEnv('${env.id}')">Delete</button>

        <button class="btn port" id="port-${env.id}" disabled>
          Port ${env.port} (Starting…)
        </button>
      </div>

      <div class="logs-box">
        <pre id="logs-${env.id}">Waiting for logs...</pre>
      </div>
    `;

    envList.appendChild(div);

    startLogPolling(env.id);
    checkPortReady(env.id, env.port);
  });
}

/***********************
 * LOGS
 ***********************/
function startLogPolling(name) {
  setInterval(async () => {
    try {
      const res = await fetch(`http://localhost:5000/docker-logs/${name}`);
      const data = await res.json();
      document.getElementById(`logs-${name}`).innerText =
        data.logs || "No logs yet";
    } catch {}
  }, 3000);
}

/***********************
 * PORT READY CHECK
 ***********************/
function checkPortReady(name, port) {
  const btn = document.getElementById(`port-${name}`);

  const timer = setInterval(async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/port-status/${name}/${port}`
      );
      const data = await res.json();

      if (data.ready) {
        btn.disabled = false;
        btn.innerText = `Open Port ${port}`;
        btn.onclick = () =>
          window.open(`http://localhost:${port}`, "_blank");
        clearInterval(timer);

        environments.forEach(e => {
          if (e.id === name) e.status = "Running";
        });
      }
    } catch {}
  }, 3000);
}

/***********************
 * ACTIONS
 ***********************/
function stopEnv(id) {
  fetch("http://localhost:5000/stop-env", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
}

function startEnv(id) {
  fetch("http://localhost:5000/start-env", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
}

function deleteEnv(id) {
  fetch("http://localhost:5000/delete-env", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });

  environments = environments.filter(e => e.id !== id);
  renderEnvs();
}
