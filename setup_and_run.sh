#!/bin/bash

# GIROBANK Banking Application - Setup and Run Script
# This script will clone the repository, install all dependencies, and run the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository URL
REPO_URL="https://github.com/mr-gaurav-kumar/soft-engg-project-sep-2025-se-SEP-41.git"
BRANCH="sajal-customer-frontend-working"
PROJECT_DIR="Banking-Application-3"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GIROBANK Application Setup Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if required tools are installed
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed. Please install Git first.${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed. Please install Node.js and npm.${NC}"
    exit 1
fi

echo -e "${GREEN}All prerequisites are installed!${NC}"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if we're already in the project directory
if [ -d "backend" ] && [ -d "frontend" ]; then
    echo -e "${YELLOW}Already in project directory. Skipping clone...${NC}"
    PROJECT_DIR="."
else
    # Clone or download the repository
    echo -e "${YELLOW}Downloading repository...${NC}"
    
    if [ -d "$PROJECT_DIR" ]; then
        echo -e "${YELLOW}Directory $PROJECT_DIR already exists. Removing it...${NC}"
        rm -rf "$PROJECT_DIR"
    fi
    
    git clone -b "$BRANCH" "$REPO_URL" "$PROJECT_DIR" || {
        echo -e "${RED}Git clone failed. Trying to download as ZIP...${NC}"
        curl -L "https://github.com/mr-gaurav-kumar/soft-engg-project-sep-2025-se-SEP-41/archive/refs/heads/$BRANCH.zip" -o "$PROJECT_DIR.zip"
        unzip -q "$PROJECT_DIR.zip"
        mv "soft-engg-project-sep-2025-se-SEP-41-$BRANCH" "$PROJECT_DIR"
        rm "$PROJECT_DIR.zip"
    }
    
    cd "$PROJECT_DIR"
    echo -e "${GREEN}Repository downloaded successfully!${NC}"
    echo ""
fi

# Backend Setup
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Setting up Backend (Flask)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

cd backend

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created!${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies (this may take several minutes)...${NC}"
echo -e "${YELLOW}Note: llama-cpp-python installation can take 10-15 minutes...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}Backend dependencies installed!${NC}"
echo ""

# Create models directory if it doesn't exist
echo -e "${YELLOW}Setting up AI model directory...${NC}"
mkdir -p models

# Check if model file exists
if [ ! -f "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf" ]; then
    echo -e "${YELLOW}AI model file not found in models directory.${NC}"
    echo -e "${YELLOW}You need to download the AI model manually.${NC}"
    echo -e "${YELLOW}Model: mistral-7b-instruct-v0.2.Q4_K_M.gguf${NC}"
    echo -e "${YELLOW}Place it in: backend/models/${NC}"
    echo -e "${YELLOW}You can download it from Hugging Face or other model repositories.${NC}"
    echo ""
else
    echo -e "${GREEN}AI model file found!${NC}"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file template...${NC}"
    cat > .env << EOF
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOF
    echo -e "${YELLOW}Please update .env file with your email credentials for email functionality.${NC}"
    echo ""
fi

cd ..

# Frontend Setup
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Setting up Frontend (Vue.js)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

cd frontend

# Install Node dependencies
echo -e "${YELLOW}Installing Node.js dependencies (this may take a few minutes)...${NC}"
npm install --legacy-peer-deps

echo -e "${GREEN}Frontend dependencies installed!${NC}"
echo ""

cd ..

# Setup complete
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create run script
echo -e "${YELLOW}Creating run script...${NC}"
cat > run_app.sh << 'RUNSCRIPT'
#!/bin/bash

# GIROBANK Application Runner
# This script starts both backend and frontend servers

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting GIROBANK Application..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend Server (Flask) on http://127.0.0.1:5000..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Frontend
echo "Starting Frontend Server (Vue.js) on http://localhost:8080..."
cd "$PROJECT_DIR/frontend"
npm run serve &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "Application is running!"
echo "Backend:  http://127.0.0.1:5000"
echo "Frontend: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=========================================="
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
RUNSCRIPT

chmod +x run_app.sh

echo -e "${GREEN}Run script created: run_app.sh${NC}"
echo ""

# Instructions
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Next Steps:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "1. ${YELLOW}If AI model is missing:${NC}"
echo "   Download mistral-7b-instruct-v0.2.Q4_K_M.gguf"
echo "   Place it in: backend/models/"
echo ""
echo -e "2. ${YELLOW}Configure email (optional):${NC}"
echo "   Edit backend/.env with your SMTP credentials"
echo ""
echo -e "3. ${YELLOW}Run the application:${NC}"
echo "   ./run_app.sh"
echo ""
echo -e "   Or manually:"
echo "   ${YELLOW}Terminal 1 (Backend):${NC}"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python3 app.py"
echo ""
echo "   ${YELLOW}Terminal 2 (Frontend):${NC}"
echo "   cd frontend"
echo "   npm run serve"
echo ""
echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""

