# GIROBANK Application - Setup Commands

## Quick Setup (Run in Terminal)

Copy and paste these commands into your terminal on Mac:

```bash
# 1. Clone the repository
git clone -b sajal-customer-frontend-working https://github.com/mr-gaurav-kumar/soft-engg-project-sep-2025-se-SEP-41.git Banking-Application-3

# 2. Navigate to project directory
cd Banking-Application-3

# 3. Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir -p models

# 4. Create .env file for email (optional)
cat > .env << EOF
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOF

# 5. Frontend Setup
cd ../frontend
npm install --legacy-peer-deps

# 6. Download AI Model (Required for AI features)
# The model file is too large for Git. You need to download it manually:
# Model: mistral-7b-instruct-v0.2.Q4_K_M.gguf
# Place it in: backend/models/
# You can download from Hugging Face or other model repositories

# 7. Run the Application
# Open two terminal windows:

# Terminal 1 - Backend:
cd backend
source venv/bin/activate
python3 app.py

# Terminal 2 - Frontend:
cd frontend
npm run serve

# Access the application:
# Frontend: http://localhost:8080
# Backend API: http://127.0.0.1:5000
```

## Automated Setup Script

Alternatively, use the provided setup script:

```bash
# Make script executable
chmod +x setup_and_run.sh

# Run the setup script
./setup_and_run.sh

# After setup, run the application
./run_app.sh
```

## Prerequisites

Before running, ensure you have:
- Python 3.8 or higher
- Node.js (LTS version) and npm
- Git

## Important Notes

1. **AI Model**: The AI model file (mistral-7b-instruct-v0.2.Q4_K_M.gguf) is not included in the repository due to size. You must download it separately and place it in `backend/models/` directory.

2. **Email Configuration**: For email functionality (OTP sending, dispute emails), configure the `.env` file in the `backend/` directory with your SMTP credentials.

3. **Database**: The SQLite database will be automatically created on first run at `backend/instance/banking.db`.

4. **Installation Time**: 
   - Backend dependencies: 5-10 minutes (llama-cpp-python takes longest)
   - Frontend dependencies: 2-5 minutes

## Troubleshooting

- If `llama-cpp-python` installation fails, try: `CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python`
- If npm install fails, try: `npm install --legacy-peer-deps --force`
- For port conflicts, change ports in `app.py` (backend) or `vue.config.js` (frontend)

