#!/bin/bash

# Setup script for GrayVideo Enhanced on macOS/Linux

echo ""
echo "=========================================="
echo "GrayVideo Enhanced - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "[OK] Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "[OK] Dependencies installed successfully"
echo ""

# Create snapshots directory
if [ ! -d snapshots ]; then
    mkdir snapshots
    echo "[OK] Snapshots directory created"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start using GrayVideo Enhanced:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the application:"
echo "     python video_processor.py"
echo ""
echo "For help with command-line options:"
echo "  python video_processor.py --help"
echo ""
