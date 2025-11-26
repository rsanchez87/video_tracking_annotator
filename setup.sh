#!/bin/bash
# Quick setup script for Soccer Ball Annotation project

echo "======================================"
echo "Soccer Ball Annotation - Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "✗ Python 3 not found. Please install Python 3.7+"; exit 1; }
echo "✓ Python found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt || { echo "✗ Failed to install dependencies"; exit 1; }
echo "✓ Dependencies installed"
echo ""

# Download YOLOv8n model
echo "Downloading YOLOv8n model..."
if [ ! -f "models/yolov8n.pt" ]; then
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P models/ || {
        echo "✗ Failed to download model"
        echo "  You can download it manually from:"
        echo "  https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        exit 1
    }
    echo "✓ Model downloaded"
else
    echo "✓ Model already exists"
fi
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p videos annotations
echo "✓ Directories created"
echo ""

echo "======================================"
echo "✓ Setup complete!"
echo "======================================"
echo ""
echo "Quick start:"
echo "  1. Place your video in videos/ folder"
echo "  2. Run: python motion_detector/annotator.py videos/your_video.mp4"
echo ""
echo "See README.md for more information."

