#!/usr/bin/env python3
"""YOLO ball detector"""

import cv2
from ultralytics import YOLO
import time
import sys
import os

DEFAULT_MODEL_PATH = "models/yolov8n.pt"
DEFAULT_SAMPLE_RATE = 10
DEFAULT_SCALE = 0.4
DEFAULT_CONFIDENCE = 0.03

def validate_ball_presence(video_path, model_path=DEFAULT_MODEL_PATH, sample_rate=DEFAULT_SAMPLE_RATE,
                          scale=DEFAULT_SCALE, conf=DEFAULT_CONFIDENCE):
    if not os.path.exists(model_path):
        print(f"✗ Model not found: {model_path}")
        print(f"  Download from: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt")
        return {'error': 'Model not found'}

    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {'error': 'Cannot open video'}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    results = {
        'total_frames': total_frames,
        'frames_analyzed': 0,
        'frames_with_ball': 0,
        'detections': [],
        'detection_rate': 0,
        'processing_time': 0,
        'avg_confidence': 0,
        'low_conf_detections': 0
    }

    start_time = time.time()
    frame_idx = 0
    confidence_sum = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        if frame_idx % sample_rate != 0:
            continue

        results['frames_analyzed'] += 1

        h, w = frame.shape[:2]
        frame_small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        crop_h = frame_small.shape[0]
        frame_crop = frame_small[int(crop_h * 0.25):int(crop_h * 0.92), :]
        frame_enhanced = cv2.GaussianBlur(frame_crop, (3, 3), 0)

        preds = model(frame_enhanced, conf=conf, verbose=False, classes=[32], iou=0.4)

        best_detection = None
        max_conf = 0

        for pred in preds:
            for box in pred.boxes:
                if model.names[int(box.cls[0])] == 'sports ball':
                    current_conf = float(box.conf[0])

                    if current_conf > max_conf:
                        max_conf = current_conf
                        best_detection = {
                            'frame': frame_idx,
                            'time': frame_idx / fps,
                            'confidence': current_conf,
                            'bbox': box.xyxy[0].cpu().numpy().tolist()
                        }

        if best_detection:
            results['frames_with_ball'] += 1
            results['detections'].append(best_detection)
            confidence_sum += max_conf

            if max_conf < 0.1:
                results['low_conf_detections'] += 1

        if results['frames_analyzed'] % 100 == 0:
            print(f"\rProgress: {frame_idx}/{total_frames} | Detections: {results['frames_with_ball']}", end='')

    cap.release()

    results['processing_time'] = time.time() - start_time  # type: ignore
    results['detection_rate'] = (results['frames_with_ball'] / results['frames_analyzed'] * 100  # type: ignore
                                 if results['frames_analyzed'] > 0 else 0)
    results['avg_confidence'] = (confidence_sum / results['frames_with_ball']  # type: ignore
                                if results['frames_with_ball'] > 0 else 0)

    return results


def print_report(results):
    if 'error' in results:
        print(f"\n✗ Error: {results['error']}")
        return

    print("\n" + "=" * 50)
    print("VALIDATION REPORT")
    print("=" * 50)
    print(f"Frames analyzed:   {results['frames_analyzed']}")
    print(f"Frames with ball:  {results['frames_with_ball']}")
    print(f"Detection rate:    {results['detection_rate']:.1f}%")
    print(f"Processing time:   {results['processing_time']:.1f}s")
    print(f"Speed:             {results['frames_analyzed'] / results['processing_time']:.1f} fps")
    print("=" * 50)


def main():
    if len(sys.argv) < 2:
        print("Usage: python detector.py <video_path> [model_path] [sample_rate]")
        print("\nExamples:")
        print("  python detector.py videos/match.mp4")
        print("  python detector.py videos/match.mp4 models/yolov8x.pt")
        print("  python detector.py videos/match.mp4 models/yolov8n.pt 5")
        sys.exit(1)

    video_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL_PATH
    sample_rate = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_SAMPLE_RATE

    if not os.path.exists(video_path):
        print(f"✗ Video not found: {video_path}")
        sys.exit(1)

    print(f"\nRunning detection on: {video_path}")
    print(f"Model: {model_path}")
    print(f"Sample rate: {sample_rate}\n")

    results = validate_ball_presence(video_path, model_path=model_path, sample_rate=sample_rate)
    print_report(results)


if __name__ == "__main__":
    main()
