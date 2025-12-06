# SEP Banking Application

A modern, full-stack banking application built with Vue.js (Frontend) and Flask (Backend).

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Git**: For cloning the repository.
- **Python 3.8+**: For the backend server.
- **Node.js (LTS) & npm**: For the frontend application.

---

## Installation & Setup

These instructions apply to **macOS**, **Linux**, and **Windows (via WSL)**.

> **Note for Windows Users**: We strongly recommend using **WSL (Windows Subsystem for Linux)** with Ubuntu. The commands below should be run inside your WSL terminal.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Banking Application-3"
```

### 2. Backend Setup (Flask)

Open a terminal (Terminal on Mac, WSL on Windows) and navigate to the project root:

```bash
cd backend
```

**Create a virtual environment:**

```bash
# macOS / Linux / WSL
python3 -m venv venv
```

**Activate the virtual environment:**

```bash
# macOS / Linux / WSL
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup (Vue.js)

Open a **new** terminal tab/window and navigate to the frontend directory:

```bash
cd frontend
```

**Install Node dependencies:**

```bash
npm install
```

---

## Running the Application

You will need two running terminal processes: one for the backend and one for the frontend.

### 1. Start the Backend Server

In your **backend** terminal (with `venv` activated):

```bash
# Ensure you are in the /backend directory
python3 app.py
```
*The backend server typically runs on `http://127.0.0.1:5000`.*

### 2. Start the Frontend Application

In your **frontend** terminal:

```bash
# Ensure you are in the /frontend directory
npm run serve
```
*The frontend development server will start, usually accessible at [`http://localhost:8080`](http://localhost:8080).*

---

## 🛠 Troubleshooting

### Common Issues

**1. `ModuleNotFoundError` in Backend**
- **Cause**: Virtual environment not activated or packages not installed.
- **Fix**: Ensure you see `(venv)` in your terminal prompt. Run `source venv/bin/activate` and then `pip install -r requirements.txt` again.

**2. Port Already in Use**
- **backend**: If port 5000 is taken, find and kill the process or edit `app.py` to use a different port.
- **frontend**: If port 8080 is taken, `npm run serve` will usually verify if you want to use a different port (e.g., 8081). Allow it to do so.

**3. Frontend dependency errors (`gyp`, `node-sass`, etc.)**
- **Fix**: frequent with older Node versions. Ensure you are using a stable Node version (v16 or v18 recommended). Try deleting `node_modules` and `package-lock.json` and running `npm install` again.

**4. Windows PowerShell/CMD**
- If you are forcefully trying to use PowerShell instead of WSL, commands like `source` won't work. Use `.\venv\Scripts\activate` instead. However, **WSL is strictly recommended** for compatibility.
