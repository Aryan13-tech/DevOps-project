let environments = [];

/* ========= LOGIN / REGISTER ========= */
function openModal(type) {
  document.getElementById("authModal").style.display = "flex";
  document.getElementById("modalTitle").innerText =
    type === "login" ? "Login" : "Register";
}

function closeModal() {
  document.getElementById("authModal").style.display = "none";
}

/* ========= CREATE ENV ========= */
function createEnv() {
  const image = document.getElementById("image").value;
  const cpu = document.getElementById("cpu").value.trim();
  const ram = document.getElementById("ram").value.trim();
  const port = document.getElementById("port").value.trim();
  const command = document.getElementById("command").value.trim();

  if (!cpu || !ram || !port || !command) {
    alert("Please fill all fields");
    return;
  }

  if (port < 1001 || port > 9999) {
    alert("Port must be between 1001 and 9999");
    return;
  }

  const env = {
    id: Date.now(),
    image,
    cpu,
    ram,
    port,
    status: "Running"
  };

  environments.push(env);
  renderEnvs();
  clearForm();
}

/* ========= RENDER ========= */
function renderEnvs() {
  const list = document.getElementById("envList");
  list.innerHTML = "";

  if (environments.length === 0) {
    list.innerHTML = `<p class="empty">No environment created yet.</p>`;
    return;
  }

  environments.forEach(env => {
    const div = document.createElement("div");
    div.className = "env-card";

    div.innerHTML = `
      <p><b>Image:</b> ${env.image}</p>
      <p><b>CPU:</b> ${env.cpu}</p>
      <p><b>RAM:</b> ${env.ram} MB</p>
      <p><b>Port:</b> ${env.port}</p>
      <p><b>Status:</b>
        <span class="status ${env.status.toLowerCase()}">${env.status}</span>
      </p>

      <div class="actions">
        <button class="btn start"
          onclick="updateStatus(${env.id}, 'Running')"
          ${env.status === "Running" ? "disabled" : ""}>Start</button>

        <button class="btn stop"
          onclick="updateStatus(${env.id}, 'Stopped')"
          ${env.status === "Stopped" ? "disabled" : ""}>Stop</button>

        <button class="btn delete"
          onclick="deleteEnv(${env.id})">Delete</button>

        <button class="btn port"
          onclick="openPort(${env.port})">Port ${env.port}</button>
      </div>
    `;

    list.appendChild(div);
  });
}

/* ========= ACTIONS ========= */
function updateStatus(id, status) {
  environments.forEach(env => {
    if (env.id === id) env.status = status;
  });
  renderEnvs();
}

function deleteEnv(id) {
  environments = environments.filter(env => env.id !== id);
  renderEnvs();
}

function openPort(port) {
  window.open(`http://localhost:${port}`, "_blank");
}

function clearForm() {
  document.getElementById("cpu").value = "";
  document.getElementById("ram").value = "";
  document.getElementById("port").value = "";
  document.getElementById("command").value = "";
}
