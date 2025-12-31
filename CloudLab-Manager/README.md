# 🌩️ CloudLab Manager  
### Intelligent Error Explanation & Resolution Tool

CloudLab Manager is a hybrid error explanation platform that helps beginners and developers understand technical error messages in a simple, human-friendly way.  
It works offline for common errors and online using AI for advanced or unknown errors.

---

## 📘 Overview

CloudLab Manager converts confusing programming and system error messages into:

- Clear explanations  
- Possible causes  
- Step-by-step solutions  

Instead of searching forums or documentation, users can paste an error message and instantly understand what went wrong and how to fix it.

The system follows a real-life hybrid model:
- **Offline** → predefined common errors  
- **Online** → AI-based error analysis (Gemini)

---

## 🧠 Problem Statement

Programming and system error messages are often difficult to understand, especially for beginners.

Errors such as:
- Module not found  
- Port already in use  
- Permission denied  

do not clearly explain what happened, why it happened, or how to fix it.  
As a result, users waste a lot of time searching online.

---

## 💡 Proposed Solution

CloudLab Manager acts as an **Error Explanation Engine**.

### Working Flow
1. User pastes an error message  
2. System checks known errors (offline)  
3. If found → explanation is shown instantly  
4. If not found → user is prompted to connect to the internet  
5. AI analyzes the error and returns results  

---

## ⚙️ Tech Stack

### 🖥️ Frontend
- HTML5  
- CSS3  
- JavaScript (Vanilla JS)  
- Fetch API  

### ⚙️ Backend
- Node.js  
- Express.js  

### 🧠 AI Integration
- Gemini Pro API  

---

## 🏗️ Architecture

### Client–Server Architecture
- Frontend handles UI and user interaction  
- Backend securely communicates with AI  

### Hybrid Processing Model
- **Offline Mode** → Known error database (no internet required)  
- **Online Mode** → AI-based error analysis (internet required)  

---

## 🧩 Features

- Offline support for common known errors  
- Online AI-based analysis for unknown errors  
- Beginner-friendly explanations  
- Error categorization (System / Network / Language)  
- Copy solution feature  
- Loading state for better user experience  
- Responsive and clean UI  
- Secure API key handling  

---

## 🧪 Known Errors Supported (Offline)

- Module not found  
- Port already in use  
- Permission denied  
- Command not found  
- File not found  
- Syntax error  
- Null / undefined reference  

---

## 🌐 Online AI Support

For errors not found in offline mode:
- User is prompted to connect to the internet  
- Error is sent to Gemini AI  
- AI returns explanation, causes, and solutions  

---

## 🏗️ Project Structure

```bash
cloudlab-manager/
│
├── backend/
│   ├── server.js
│   ├── .env
│   ├── package.json
│
├── frontend/
│   ├── index.html
│
└── README.md
