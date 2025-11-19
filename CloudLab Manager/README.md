## 🌩️ CloudLab Manager

 A full-stack DevOps project that allows users to create, manage, and delete Docker-based development environments through a clean web interface.
CloudLab Manager demonstrates real-world DevOps concepts including container automation, API development, and deployment workflows.


## 📘 Overview
---
 CloudLab Manager is a web platform where users can dynamically generate isolated environments (Docker containers) using an intuitive UI.
The backend automatically generates Dockerfiles, builds images, runs containers, and provides APIs to manage their lifecycle.

🔹 Fully automated environment creation
🔹 Modern Flask backend with Docker SDK
🔹 Responsive dashboard UI (updated)
🔹 Optional JSON/SQLite storage
🔹 Extensible DevOps-ready architecture


## ⚙️ Tech Stack
🖥️ Frontend

HTML5

CSS3

JavaScript (Vanilla JS)

Fetch API (for calling Flask APIs)

🔥 Backend

Python 3.x

Flask

Docker SDK for Python

JSON / SQLite (optional database)

🐳 DevOps & Tools

Docker Engine

Docker Compose

Git

Linux / Shell scripting
---

## 🧩 Features

✔ Create Docker environments dynamically
✔ Auto-generate Dockerfiles based on user input
✔ Build Docker images from UI
✔ Run, stop, delete containers
✔ View container logs
✔ Store metadata in JSON or SQLite
✔ Clean, updated UI for Dashboard
✔ Extendable for cloud deployment (AWS / Terraform optional)

---

## 🏗️ Project Structure
 ```bash
cloudlab-manager/
│
├── backend/
│   ├── app.py
│   ├── docker_service.py
│   ├── file_service.py
│   ├── db.json        # optional storage
│   ├── Docker/
│   │     └── generated/
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```
---
## 📸 UI Preview 

The UI is designed to look clean, similar to modern dashboards:

Sidebar-free minimal layout

“Create Docker Environment” section (left)

“Running Containers” section (right)

Action buttons (Start/Stop/Delete/Logs)

Logout button and CloudLab branding
---

## 🚀 How to Run Locally
🧰 Prerequisites

Python 3.10+

Docker Engine installed

Git installed

---

## 🔧 Setup Steps
1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/cloudlab-manager.git
cd cloudlab-manager
```
2️⃣ Setup backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
3️⃣ Start backend
```bash
python app.py
```
Backend will run at:
👉 http://localhost:8000

4️⃣ Run frontend

Open:
```bash
frontend/index.html
```

---




