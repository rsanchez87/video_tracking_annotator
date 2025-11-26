# ⚽ Ball Annotation & Detection Tools

OpenCV tools for soccer ball annotation, detection and tracking.

## 🎯 NEW: Ball Annotator Interactive (Recording Mode)

**Fast annotation tool** - Follow the ball with your mouse while video plays!

### Quick Start

```bash
python3 "Motion Detector/ball_annotator_interactive.py" videos/test.mp4
```

**Workflow:**
1. Press `SPACE` to play video
2. Press `r` to start recording (red crosshair appears)
3. Move mouse to follow the ball
4. Press `r` to stop recording
5. Press `q` to quit and save

**Output:** `annotations/[video_name]_coco.json` (COCO format)

### Controls

| Key       | Action               |
|-----------|----------------------|
| `r`       | Start/Stop RECORDING |
| `SPACE`   | Play/Pause           |
| `+` / `-` | Speed up/slow down   |
| `z`       | Toggle zoom          |
| `n` / `p` | Next/previous frame  |
| `s`       | Save annotations     |
| `q`       | Quit & save          |
| `g`       | Go to specific frame |

### Why Recording Mode?

- ⚡ **10-30x faster** than frame-by-frame clicking
- 🎯 **Smooth annotations** - follow ball naturally with mouse
- 💾 **Auto-save** - annotations saved every frame during recording
- 📊 **COCO format** - standard format for ML frameworks
- 🔄 **Resume anytime** - loads existing annotations automatically

---

## Tools Overview

### 1. ball_annotator_interactive.py ⭐
**Interactive annotation with mouse tracking**

```bash
python3 "Motion Detector/ball_annotator_interactive.py" videos/test.mp4
```

Features:
- Recording mode (follow ball with mouse)
- COCO format output
- Playback speed control
- Frame navigation
- Auto-save/load

### 2. ball_detector_enhanced.py
**Automated YOLO-based detection**

```bash
python3 "Motion Detector/ball_detector_enhanced.py"
```

Features:
- YOLOv8 detection
- Validation reports
- Configurable thresholds

### 3. ball_manual_tracker.py
**Semi-automated optical flow tracking**

```bash
python3 "Motion Detector/ball_manual_tracker.py"
```

Features:
- Manual ball selection
- Lucas-Kanade tracking
- Robust to occlusions

### 4. view_annotations.py
**Annotation viewer and validator**

```bash
# View statistics
python3 view_annotations.py annotations/test_coco.json

# Visualize on video
python3 view_annotations.py annotations/test_coco.json videos/test.mp4
```

---

## COCO Format Output

Standard COCO format with video support:

```json
{
  "info": {
    "description": "Ball tracking annotations",
    "video_id": "test",
    "video_path": "videos/test.mp4"
  },
  "videos": [{"id": 1, "name": "test", "width": 1920, "height": 1080, "fps": 30}],
  "categories": [{"id": 1, "name": "ball", "supercategory": "sports"}],
  "images": [{"id": 100, "video_id": 1, "frame_id": 100, "file_name": "frame_000100.jpg"}],
  "annotations": [{
    "id": 1,
    "image_id": 100,
    "video_id": 1,
    "frame_id": 100,
    "category_id": 1,
    "bbox": [950, 530, 20, 20],
    "area": 400,
    "iscrowd": 0,
    "center": [960, 540]
  }]
}
```

**Key fields:**
- `video_id`: Video identifier
- `frame_id`: Frame number
- `bbox`: [x, y, width, height] in pixels
- `center`: [x, y] ball center coordinates

---

## Installation

```bash
pip install opencv-python ultralytics numpy
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## Tips for Best Results

### Recording Tips
✅ Adjust speed with `+/-` (try 0.5x for precise annotation)  
✅ Press `z` for 100% zoom if needed  
✅ Save frequently with `s`  
✅ Move mouse smoothly following ball trajectory  
✅ Practice on a short section first  

### What to Annotate
✅ Clear ball positions (visible and in focus)  
✅ Different positions (ground, air, near/far)  
✅ Different situations (passes, shots, dribbles)  
❌ Skip when ball is occluded or too blurry  

### For Training Models
- Annotate 500-1000 frames minimum
- Include diverse ball positions and lighting
- Use COCO format directly with most ML frameworks
- Validate annotations with `view_annotations.py`

---

## Common Questions

**Q: How many frames should I annotate?**  
A: 500-1000 frames is good for training. Quality > quantity!

**Q: Can I pause and continue later?**  
A: Yes! Annotations auto-load when you restart.

**Q: Video plays too fast?**  
A: Press `-` multiple times (can go to 0.25x speed).

**Q: How do I know it's recording?**  
A: Look for red crosshair and "RECORDING" status.

**Q: Can I annotate specific sections only?**  
A: Yes! Use `g` to jump to frame, then record that section.

---

## Project Structure

```
openCV/
├── Motion Detector/
│   ├── ball_annotator_interactive.py  # Mouse tracking annotator ⭐
│   ├── ball_detector_enhanced.py      # YOLO detection
│   └── ball_manual_tracker.py         # Optical flow tracking
├── videos/
│   └── test.mp4                       # Test video
├── annotations/                        # Created by annotator
│   └── test_coco.json                 # COCO annotations
├── training_frames/                    # Extracted frames
├── view_annotations.py                 # Annotation viewer
├── extract_frames.py                   # Frame extraction
├── requirements.txt                    # Dependencies
├── yolov8n.pt                         # YOLO nano model
└── yolov8x.pt                         # YOLO large model
```

---

## Example Workflow

### Create Training Dataset
```bash
# 1. Annotate video
python3 "Motion Detector/ball_annotator_interactive.py" videos/test.mp4
# Press SPACE → Press 'r' → Follow ball → Press 'q'

# 2. View annotations
python3 view_annotations.py annotations/test_coco.json videos/test.mp4

# 3. Train your model with COCO format annotations
```

### Validate Detection
```bash
# Test YOLO detection
python3 "Motion Detector/ball_detector_enhanced.py"
```

---

## Notes

- Bounding box size: 20x20 pixels (configurable)
- Ball category ID: 1
- Supports standard video formats (mp4, avi, mov)
- Compatible with COCO training pipelines
- All coordinates in pixels (not normalized)
- ✅ Color detection: Too many false positives
- ✅ Motion filtering: Blocks real detections
- ✅ Tracking: Loses ball quickly

**Why it fails:** Ball is too small (<50 pixels) for YOLO's training data.

**For production:** Use your AI Detection API or train custom model.

---

## Available Tools

### 1. YOLO Detector
```bash
python3 "Motion Detector/ball_detector_enhanced.py"
```
- YOLOv8x detection
- 1-2% detection rate (only when ball is close)
- Fast and simple
- **Use for:** Baseline testing only

### 2. Manual Tracker
```bash
python3 "Motion Detector/ball_tracker_fixed.py"
```
- Manual selection with optical flow tracking
- Press 'c' to select ball, ENTER to confirm
- **Use for:** Manual verification of specific frames

### 3. YOLO Basic
```bash
python3 "Motion Detector/ball_detector_yolo.py"
```
- Basic YOLO with yolov8n (smaller model)
- Similar results to enhanced version
- **Use for:** Quick testing

### 4. Extract Frames
```bash
python3 extract_frames.py
```
- Extracts frames to PNG for training
- Configure interval in file
- **Use for:** Creating training dataset

---

## Installation

```bash
# System dependencies (required for GUI)
sudo apt-get update
sudo apt-get install -y libgtk2.0-dev pkg-config

# Python packages
pip install -r requirements.txt
```

---

## Real Results Summary

| Method         | Detection Rate | Speed  | Recommended      |
|----------------|----------------|--------|------------------|
| YOLOv8x        | 1-2%           | Fast   | Testing only     |
| YOLOv8n        | 1-2%           | Faster | Testing only     |
| Manual tracker | 80-90%*        | Slow   | Validation       |
| Your AI API    | ?              | ?      | ✅ **Production** |

*Requires manual selection every few seconds

---

## For Production Use

**Don't use these OpenCV tools for production.**

These are **testing/validation tools only**.

For actual ball detection in production:
1. **Your AI Detection API** (best if trained on similar data)
2. **TrackNet** (specialized for sports ball tracking)
3. **Custom YOLOv8 trained on your footage** (requires annotation)

---

## What We Learned

After extensive testing:
- Generic YOLO models don't detect small balls (1-2%)
- Upscaling doesn't help (same 1-2%)
- Color detection has too many false positives
- Manual tracking works but requires constant intervention

**Bottom line:** Small soccer balls in match footage require deep learning models specifically trained for this task.

---

## File Structure

```
Motion Detector/
├── ball_detector_enhanced.py  - YOLO detection (final, simple)
├── ball_detector_yolo.py      - YOLO basic
└── ball_tracker_fixed.py      - Manual tracking

extract_frames.py               - Frame extraction for training
README.md                       - This file
```

---

## Summary

These tools are for **testing and validation**, not production.

- ✅ Test if ball is visible in video
- ✅ Verify video quality
- ✅ Compare with AI results
- ✅ Extract frames for training
- ❌ NOT for automated detection in production

**For production:** Use your AI Detection API 🎯⚽

