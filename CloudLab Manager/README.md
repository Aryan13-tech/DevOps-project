
## 🌩️ CloudLab Manager

A simple DevOps project to create, manage, and delete cloud environments using Docker and FastAPI.


---

## 📘 Overview


CloudLab Manager is a web-based application that helps users create and manage temporary environments (containers) dynamically.
It uses FastAPI as the backend, PostgreSQL for storage, and Docker to run environments automatically.

The project also includes Terraform to deploy the entire system on AWS EC2, demonstrating practical DevOps and Cloud Computing concepts.

---

## ⚙️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: FastAPI (Python)

Database: PostgreSQL

Containerization: Docker, Docker Compose

Infrastructure as Code: Terraform (AWS EC2)

Monitoring (optional): Prometheus, Grafana

---

## 🧩 Features

Create and delete containerized environments dynamically

Store environment details in a database

Simple and user-friendly interface

Deploy entire project on AWS using Terraform

Demonstrates DevOps automation and cloud deployment

---

## 🏗️ Project Structure

```bash
cloudlab-manager/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   └── docker_ops.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   └── index.html
│
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   └── provider.tf
│
└── docker-compose.yml
```

---

## 🚀 How to Run

### 🧰 Prerequisites

Docker & Docker Compose installed

Python 3.11+ installed

AWS account (for Terraform deployment)

---

## 🔧 Local Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/cloudlab-manager.git
cd cloudlab-manager

# Start backend and database
docker-compose up --build
```
Now open frontend/index.html in your browser and use the app.

## ✅ Example:

Enter image → nginx:latest

Enter port → 8081

Click Create Environment

Then open:
👉 http://localhost:8081 to see your container running.

--- 

## ☁️ Cloud Deployment (Terraform + AWS)

```bash
cd infra
terraform init
terraform apply
```

Terraform will:

Create an EC2 instance

Install Docker and deploy the project automatically

After deployment, visit:
👉 http://<EC2-public-IP>:8000

---

## 🧠 Future Improvements

Add authentication (login system)

Auto-delete expired environments

Add monitoring dashboard with Grafana

Support Kubernetes instead of Docker

---


