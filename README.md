# ⚽ Soccer Ball Annotation Tool

**Main tool:** Interactive mouse-tracking annotator for creating ball position datasets.

**Optional:** YOLO detector for baseline testing (experimental, low accuracy).

## Complete Workflow

```bash
# 1. MERGE multiple video clips into one (if needed)
python utils/merge_videos.py full_match.mp4 half1.mp4 half2.mp4

# 2. ANNOTATE the merged video (⭐ main tool)
python motion_detector/annotator.py full_match.mp4

# 3. VIEW and validate annotations
python utils/view_annotations.py annotations/full_match_coco.json full_match.mp4

# 4. OPTIONAL - Test YOLO detector for baseline
python motion_detector/detector.py full_match.mp4
```

## Quick Start

```bash
# Setup
./setup.sh

# Main workflow
python utils/merge_videos.py full_match.mp4 clip1.mp4 clip2.mp4  # If needed
python motion_detector/annotator.py full_match.mp4               # Main tool
python utils/view_annotations.py annotations/full_match_coco.json full_match.mp4
```

## Project Structure

```
├── motion_detector/
│   ├── annotator.py          # ⭐ Main tool - Interactive annotator
│   └── detector.py            # ⚠️ Optional - YOLO detector (0-5% accuracy)
├── utils/
│   ├── view_annotations.py    # View/validate annotations
│   └── merge_videos.py        # Merge multiple video files by timestamp
├── models/
│   └── yolov8n.pt            # YOLO model (optional, for detector only)
├── videos/                    # Your video files
└── annotations/               # Generated JSON files
```

## Usage

### Video Merger (if you have multiple clips)
```bash
python utils/merge_videos.py <output.mp4> <video1.mp4> <video2.mp4> [video3.mp4 ...]

# Examples
python utils/merge_videos.py full_match.mp4 half1.mp4 half2.mp4
python utils/merge_videos.py game.mp4 videos/clip*.mp4
```

**Features:**
- Fast concatenation (no re-encoding)
- Automatically sorts videos by timestamp from filename
- Preserves original quality

### Annotator (Main Tool)
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

### Detector (Optional - Experimental)

**⚠️ Note:** Generic YOLO achieves only ~1-2% detection rate on small soccer balls. This is for baseline testing only.

```bash
python motion_detector/detector.py <video_path> [model_path] [sample_rate]

# Examples
python motion_detector/detector.py videos/match.mp4
python motion_detector/detector.py videos/match.mp4 models/yolov8x.pt
python motion_detector/detector.py videos/match.mp4 models/yolov8n.pt 5
```

**Why low accuracy?** Generic YOLO models aren't trained specifically on small soccer balls in match footage. For production, train a custom model using annotations from the annotator.

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
# Install Python dependencies
pip install -r requirements.txt

# Install ffmpeg (for video merging)
sudo apt install ffmpeg

# Download YOLO model (optional, only for detector)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P models/
```

## Notes

- **Main tool:** The annotator - create high-quality training data
- Display resolution scaled to 30% (configurable)
- Coordinates saved in original video resolution
- **Detector is optional:** 0-5% accuracy, use only for baseline comparison
- For production: train custom model with your annotations from the annotator
