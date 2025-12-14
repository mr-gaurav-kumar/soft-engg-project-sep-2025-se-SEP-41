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

