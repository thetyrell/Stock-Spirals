#!/bin/bash

# Spiral Stock Chart - Quick Start Script
# This script helps you test the application locally before deploying

echo "========================================="
echo "Spiral Stock Chart - Local Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Start the backend server in the background
echo ""
echo "🚀 Starting backend server..."
python3 backend.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend server running on http://localhost:5000"
else
    echo "❌ Failed to start backend server"
    exit 1
fi

# Start a simple HTTP server for the frontend
echo ""
echo "🌐 Starting frontend server..."
python3 -m http.server 8080 &
FRONTEND_PID=$!

sleep 2

echo ""
echo "========================================="
echo "✅ Application is ready!"
echo "========================================="
echo ""
echo "📱 Open your browser and visit:"
echo "   http://localhost:8080/index.html"
echo ""
echo "🔧 Backend API is running at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to press Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; deactivate; echo '✅ Servers stopped'; exit" INT

# Keep script running
wait
