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

# Check ffmpeg
echo "Checking ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg found"
else
    echo "⚠ ffmpeg not found (needed for video merging)"
    echo "  Install with: sudo apt install ffmpeg"
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt || { echo "✗ Failed to install dependencies"; exit 1; }
echo "✓ Dependencies installed"
echo ""

# Download YOLOv8n model (optional)
echo "Download YOLO model (optional - only for detector)?"
echo ""

if [ ! -f "models/yolov8n.pt" ]; then
    read -p "Download YOLOv8n model? [y/N]: " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P models/ || {
            echo "✗ Failed to download model"
            echo "  You can download it manually from:"
            echo "  https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        }
        echo "✓ Model downloaded"
    else
        echo "⊘ Skipped model download"
    fi
else
    echo "✓ YOLO model already exists"
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
echo "  1. If you have multiple video clips:"
echo "     python utils/merge_videos.py full_match.mp4 clip1.mp4 clip2.mp4"
echo ""
echo "  2. Annotate your video:"
echo "     python motion_detector/annotator.py videos/full_match.mp4"
echo ""
echo "  3. View annotations:"
echo "     python utils/view_annotations.py annotations/full_match_coco.json videos/full_match.mp4"
echo ""
echo "See README.md for more information."

