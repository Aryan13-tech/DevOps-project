# 🌩️ CloudLab  
## A Real-World DevOps CI/CD & Cloud Monitoring System with Intelligent Error Explanation

CloudLab is a **production-style DevOps project** that demonstrates how a modern cloud-native application can be built, deployed, monitored, and maintained using real-world tools and practices.

At its core, CloudLab provides an **Intelligent Error Explanation Engine** for developers, wrapped inside a complete **CI/CD, containerization, cloud deployment, and monitoring pipeline**, making it ideal for students and engineers learning DevOps in practice.

---

## 📌 Key Highlights

- 🔁 Jenkins CI/CD Pipeline  
- 🐳 Dockerized Frontend & Backend  
- ☁️ Deployed on AWS EC2  
- 📊 Prometheus Metrics & Grafana Dashboards  
- 🧠 Rule-Based Error Explanation Engine  
- 🛠️ Production-like Architecture  
- 🔍 Observability & Error Handling  
- 📦 Real-world DevOps Workflow  

---

## 📘 Project Overview

CloudLab is designed to bridge the gap between **classroom DevOps concepts** and **real-world cloud deployment practices**.

It allows users to:
- Submit technical error messages  
- Receive clear explanations, causes, and solutions  
- While being deployed and managed like a real production system using DevOps practices  

This makes CloudLab not just an application, but a **complete DevOps learning system**.

---

## ❗ Problem Statement

Traditional error messages are:
- Hard to understand  
- Too technical for beginners  
- Do not provide clear solutions  

At the same time, most academic projects do not:
- Use CI/CD pipelines  
- Include monitoring & logging  
- Follow real-world deployment patterns  

CloudLab solves both problems by combining:  
> 🧠 **Error Explanation System** + 🚀 **Real-world DevOps Pipeline**

---

## 💡 Solution Approach

CloudLab follows a **full DevOps lifecycle**, from code to cloud:

1. Developers push code to GitHub  
2. Jenkins automatically builds and tests  
3. Docker images are created for frontend & backend  
4. Images are pushed to Docker Hub  
5. EC2 pulls and runs containers  
6. Prometheus scrapes application metrics  
7. Grafana visualizes system health  
8. Users interact with the web interface for error explanation  

---

## 🏗️ System Architecture

```
Developer → GitHub → Jenkins → Docker → AWS EC2
                                  ↓
                           Prometheus → Grafana
                                  ↓
                             CloudLab App
```

---

## ⚙️ Tech Stack

### 🚀 DevOps & Cloud
- Jenkins (CI/CD)
- Docker & Docker Hub
- AWS EC2
- GitHub
- Linux (Ubuntu)
- Nginx (optional reverse proxy)

### 📊 Monitoring & Observability
- Prometheus  
- Grafana  
- Custom Flask `/metrics` endpoint  

### 🖥️ Frontend
- HTML5  
- CSS3  
- JavaScript (Vanilla)  
- Fetch API  

### ⚙️ Backend
- Python  
- Flask  
- Flask-CORS  
- Prometheus Client  
- dotenv  
- Logging module  

---

## 🧠 Core Feature: Intelligent Error Explanation Engine

CloudLab analyzes technical errors using rule-based logic.

### Supported Error Types

| Category     | Examples                              |
|--------------|----------------------------------------|
Programming    | NameError, SyntaxError, TypeError      |
System         | Port in use, Permission denied         |
File           | File not found                         |
Network        | Connection refused                    |
Module         | ModuleNotFoundError                   |

### Output Includes:
- Simple explanation  
- Possible causes  
- Suggested solutions  

---

## 📁 Project Structure

```bash
CloudLab/
│
├── backend/
│   ├── app.py
│   ├── error_rules.py
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── Dockerfile
│
├── monitoring/
│   ├── prometheus.yml
│
├── jenkins/
│   ├── Jenkinsfile
│
├── docker-compose.yml
└── README.md
```

---

## 🔁 CI/CD Pipeline (Jenkins)

### Pipeline Stages

1. Checkout Source Code  
2. Build Docker Images  
3. Push Images to Docker Hub  
4. Deploy Containers on EC2  
5. Restart Services Automatically  

This ensures:
- Zero manual deployment  
- Faster releases  
- Reduced human error  

---

## 🐳 Containerization

Both frontend and backend are containerized:

- Isolated environments  
- Consistent deployment  
- Easy scaling  
- Faster rollback  

---

## ☁️ AWS Deployment

CloudLab is deployed on:
- AWS EC2 (Ubuntu)
- Docker Engine  

### Open Ports

| Service     | Port       |
|-------------|------------|
Frontend      | 3000 / 80  |
Backend API   | 5000       |
Prometheus    | 9090       |
Grafana       | 3000       |

---

## 📊 Monitoring & Observability

### Prometheus
- Scrapes metrics from Flask `/metrics`  
- Tracks:
  - Request count  
  - Response time  
  - Error rates  

### Grafana
- Visualizes:
  - Application health  
  - API performance  
  - System uptime  

---

## 🧪 API Endpoints

| Endpoint     | Method | Description                |
|--------------|--------|----------------------------|
`/analyze`     | POST   | Analyze error message      |
`/health`      | GET    | Backend health check       |
`/metrics`     | GET    | Prometheus metrics         |

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/CloudLab.git
cd CloudLab
docker-compose up --build
```

### Access

- Frontend → http://localhost:3000  
- Backend → http://localhost:5000  
- Prometheus → http://localhost:9090  
- Grafana → http://localhost:3000  

---

## 🎯 Learning Outcomes

By building CloudLab, you learn:
- CI/CD pipelines  
- Docker & container orchestration  
- Cloud deployment  
- Monitoring & alerting  
- Backend error handling  
- Real-world DevOps practices  

---

## 📚 Use Case

CloudLab is ideal for:
- Engineering students  
- DevOps beginners  
- Final year projects  
- Portfolio projects  
- DevOps demonstrations  

---

## 🔮 Future Enhancements

- Kubernetes deployment  
- Auto-scaling  
- AI-based error analysis  
- Alerting with Alertmanager  
- Centralized logging (ELK Stack)  
- Authentication & role-based access  

---

## 👨‍💻 Author

**Aryan Sarvaiya**  
DevOps & Cloud Enthusiast  
Project: CloudLab – Real-World DevOps System  
