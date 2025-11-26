#!/usr/bin/env python3
"""COCO annotations viewer"""

import cv2
import json
import sys
import os

def visualize_annotations(annotation_file, video_file):
    with open(annotation_file, 'r') as f:
        coco_data = json.load(f)

    print(f"\n{'='*70}")
    print(f"COCO Annotation Viewer")
    print(f"{'='*70}")
    print(f"Video: {coco_data['info']['video_id']}")
    print(f"Annotations: {len(coco_data['annotations'])}")
    print(f"{'='*70}\n")

    frame_annotations = {}
    for ann in coco_data['annotations']:
        frame_id = ann['frame_id']
        if frame_id not in frame_annotations:
            frame_annotations[frame_id] = []
        frame_annotations[frame_id].append(ann)

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"✗ Cannot open video: {video_file}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_idx = 0
    paused = False

    print("Controls: SPACE=play/pause | n=next | p=prev | q=quit\n")

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("✓ End")
                break
            frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break

        if frame_idx in frame_annotations:
            for ann in frame_annotations[frame_idx]:
                center = ann['center']
                cx, cy = int(center[0]), int(center[1])  # type: ignore

                cv2.circle(frame, (cx, cy), 8, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

                cv2.putText(frame, f"Ball", (cx + 10, cy - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        info_text = f"Frame: {frame_idx}/{total_frames}"
        if frame_idx in frame_annotations:
            info_text += f" - ANNOTATED"
            color = (0, 255, 0)
        else:
            info_text += " - No annotation"
            color = (200, 200, 200)

        cv2.putText(frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Viewer', frame)

        delay = 1 if paused else int(1000 / fps)
        key = cv2.waitKey(delay) & 0xFF

        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
        elif key == ord('n'):
            paused = True
            frame_idx = min(frame_idx + 1, total_frames - 1)
        elif key == ord('p'):
            paused = True
            frame_idx = max(frame_idx - 1, 0)

    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Closed")


def print_statistics(annotation_file):
    with open(annotation_file, 'r') as f:
        coco_data = json.load(f)

    print(f"\n{'='*70}")
    print(f"ANNOTATION STATISTICS")
    print(f"{'='*70}")

    if 'video' in coco_data:
        video = coco_data['video']
        print(f"Video: {video['name']}")
        print(f"Resolution: {video['width']}x{video['height']}")
        print(f"Frames: {video['total_frames']} | FPS: {video['fps']}")

    print(f"\nAnnotations: {len(coco_data['annotations'])}")

    if coco_data['annotations']:
        frame_ids = [ann['frame_id'] for ann in coco_data['annotations']]
        print(f"Frame range: {min(frame_ids)} - {max(frame_ids)}")

        centers = [ann['center'] for ann in coco_data['annotations']]
        avg_x = sum(c[0] for c in centers) / len(centers)  # type: ignore
        avg_y = sum(c[1] for c in centers) / len(centers)  # type: ignore

        print(f"\nAvg position: X={avg_x:.1f}, Y={avg_y:.1f}")

    print(f"{'='*70}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python view_annotations.py <annotation.json> [video.mp4]")
        print("\nExamples:")
        print("  python view_annotations.py annotations/match_coco.json")
        print("  python view_annotations.py annotations/match_coco.json videos/match.mp4")
        sys.exit(1)

    annotation_file = sys.argv[1]

    if not os.path.exists(annotation_file):
        print(f"✗ Annotation file not found: {annotation_file}")
        sys.exit(1)

    try:
        print_statistics(annotation_file)
    except Exception as e:
        print(f"✗ Error reading annotations: {e}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        video_file = sys.argv[2]
        if not os.path.exists(video_file):
            print(f"✗ Video file not found: {video_file}")
            sys.exit(1)
        try:
            visualize_annotations(annotation_file, video_file)
        except Exception as e:
            print(f"✗ Error visualizing: {e}")
    else:
        print(f"Tip: Add video path to visualize annotations")
        print(f"  python view_annotations.py {annotation_file} videos/your_video.mp4")


if __name__ == "__main__":
    main()
