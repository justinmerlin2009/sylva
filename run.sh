#!/bin/bash

# Sylva Drone Simulation - Single Command Launcher
# TamAir - Conrad Challenge 2026

set -e

echo "========================================"
echo "    SYLVA Environmental Monitoring"
echo "    Drone Simulation System"
echo "    TamAir - Conrad Challenge 2026"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is required but not installed.${NC}"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down Sylva...${NC}"

    # Kill background processes
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
    fi
    if [ ! -z "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null || true
    fi

    echo -e "${GREEN}Sylva shutdown complete.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Install Python dependencies if needed
echo -e "${BLUE}[1/5] Checking Python dependencies...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Install Node dependencies if needed
echo -e "${BLUE}[2/5] Checking Node.js dependencies...${NC}"
cd dashboard
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install --silent
fi
cd ..

# Generate simulation data if not exists
echo -e "${BLUE}[3/5] Checking simulation data...${NC}"
if [ ! -f "data/detections/all_detections.geojson" ]; then
    echo "Generating simulation data..."
    python -m simulation.data_generator
fi

# Start API server
echo -e "${BLUE}[4/5] Starting API server on port 8000...${NC}"
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Wait for API to be ready
sleep 2

# Start dashboard
echo -e "${BLUE}[5/5] Starting dashboard on port 3000...${NC}"
cd dashboard
npm run dev &
DASHBOARD_PID=$!
cd ..

# Wait a moment for services to start
sleep 3

echo ""
echo "========================================"
echo -e "${GREEN}Sylva is running!${NC}"
echo "========================================"
echo ""
echo -e "Dashboard:  ${BLUE}http://localhost:3000${NC}"
echo -e "API:        ${BLUE}http://localhost:8000${NC}"
echo -e "API Docs:   ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Keep script running
wait
