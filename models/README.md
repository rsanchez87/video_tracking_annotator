# Models Directory

This directory contains YOLO model weights.

## Download Models

### YOLOv8 Nano (fastest, recommended for testing)
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P models/
```

### YOLOv8 Small
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt -P models/
```

### YOLOv8 Medium
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt -P models/
```

### YOLOv8 Large
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt -P models/
```

### YOLOv8 Extra Large (most accurate, slowest)
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt -P models/
```

## Model Comparison

| Model | Size | Speed | mAP |
|-------|------|-------|-----|
| YOLOv8n | 6.2MB | Fastest | 37.3 |
| YOLOv8s | 21.5MB | Fast | 44.9 |
| YOLOv8m | 49.7MB | Medium | 50.2 |
| YOLOv8l | 83.7MB | Slow | 52.9 |
| YOLOv8x | 130.5MB | Slowest | 53.9 |

## Notes

- For soccer ball detection, generic YOLO models achieve ~1-2% detection rate
- These are pre-trained on COCO dataset (class 32 = 'sports ball')
- For production use, train a custom model with your annotated data
- Models are excluded from git (see .gitignore)

