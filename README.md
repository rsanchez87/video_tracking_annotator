# ⚽ Soccer Ball Annotation & Detection

Tools for annotating and detecting soccer balls in match videos.

## Quick Start

```bash
# Setup
./setup.sh

# Annotate video
python motion_detector/annotator.py videos/match.mp4

# View annotations
python utils/view_annotations.py annotations/match_coco.json videos/match.mp4

# Test detection
python motion_detector/detector.py videos/match.mp4
```

## Project Structure

```
├── motion_detector/
│   ├── annotator.py          # Interactive mouse-tracking annotator
│   └── detector.py            # YOLO ball detector
├── utils/
│   └── view_annotations.py    # View/validate annotations
├── models/
│   └── yolov8n.pt            # YOLO model (download via setup.sh)
├── videos/                    # Your video files
└── annotations/               # Generated JSON files
```

## Usage

### Annotator
```bash
python motion_detector/annotator.py <video_path> [output_dir]
```

**Controls:**
- `r` - Start/Stop recording
- `SPACE` - Play/Pause
- `+/-` - Speed
- `z` - Zoom (30%/50%/70%)
- `q` - Quit & save

**Workflow:**
1. Press SPACE to play
2. Press 'r' to record
3. Move mouse to follow ball
4. Press 'q' to save

### Detector
```bash
python motion_detector/detector.py <video_path> [model_path] [sample_rate]

# Examples
python motion_detector/detector.py videos/match.mp4
python motion_detector/detector.py videos/match.mp4 models/yolov8x.pt
python motion_detector/detector.py videos/match.mp4 models/yolov8n.pt 5
```

### Viewer
```bash
python utils/view_annotations.py <annotation_file> [video_file]

# Examples
python utils/view_annotations.py annotations/match_coco.json
python utils/view_annotations.py annotations/match_coco.json videos/match.mp4
```

## Output Format

```json
{
  "info": {
    "video_id": "match",
    "total_annotations": 150
  },
  "video": {
    "id": 1,
    "name": "match",
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "total_frames": 8027
  },
  "annotations": [
    {
      "id": 1,
      "video_id": 1,
      "frame_id": 100,
      "center": [960, 540]
    }
  ]
}
```

## Installation

```bash
pip install -r requirements.txt

# Download model
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P models/
```

## Notes

- Display resolution scaled to 30% (configurable)
- Coordinates saved in original video resolution
- Generic YOLO: ~1-2% detection rate on small balls
- For production: train custom model with annotations

