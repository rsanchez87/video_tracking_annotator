#!/usr/bin/env python3
"""Interactive Ball Annotator - Mouse tracking recording mode"""

import cv2
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_OUTPUT_DIR = "annotations"
DEFAULT_BBOX_SIZE = 20
DEFAULT_SCALE = 30
DEFAULT_MODEL_PATH = "models/yolov8n.pt"

class BallAnnotator:
    def __init__(self, video_path, output_dir=DEFAULT_OUTPUT_DIR, bbox_size=DEFAULT_BBOX_SIZE, scale=DEFAULT_SCALE):
        self.video_path = video_path
        self.output_dir = output_dir
        self.video_name = Path(video_path).stem
        self.bbox_size = bbox_size

        os.makedirs(output_dir, exist_ok=True)

        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.coco_data = {
            "info": {
                "description": f"Ball tracking annotations for {self.video_name}",
                "date_created": datetime.now().isoformat(),
                "video_id": self.video_name,
                "video_path": video_path
            },
            "video": {
                "id": 1,
                "name": self.video_name,
                "width": self.width,
                "height": self.height,
                "total_frames": self.total_frames,
                "fps": self.fps
            },
            "annotations": []
        }

        self.current_frame_idx = 0
        self.current_frame = None
        self.is_recording = False
        self.is_playing = False
        self.playback_speed = 1

        self.mouse_x = 0
        self.mouse_y = 0

        self.scale_percent = scale
        self.display_frame = None
        self.window_name = f"Ball Annotator - {self.video_name}"
        self.annotation_id = 1

        print(f"\n{'='*70}")
        print(f"BALL ANNOTATOR - Mouse Tracking Recording Mode")
        print(f"{'='*70}")
        print(f"Video: {self.video_name}")
        print(f"Frames: {self.total_frames} | FPS: {self.fps}")
        print(f"Resolution: {self.width}x{self.height}")
        print(f"\nCONTROLS:")
        print(f"  'r': Start/Stop RECORDING (follow ball with mouse)")
        print(f"  SPACE: Play/Pause")
        print(f"  'n'/'p': Next/Previous frame")
        print(f"  'g': Go to frame")
        print(f"  's': Save")
        print(f"  'q': Quit and save")
        print(f"  '+/-': Speed")
        print(f"  'z': Zoom (30%/50%/70%)")
        print(f"{'='*70}\n")

    def mouse_callback(self, event, x, y, flags, param):
        scale_factor = self.scale_percent / 100
        self.mouse_x = int(x / scale_factor)
        self.mouse_y = int(y / scale_factor)

    def add_annotation(self, frame_idx, x, y):
        x = max(0, min(x, self.width))
        y = max(0, min(y, self.height))

        annotation = {
            "id": self.annotation_id,
            "video_id": 1,
            "frame_id": frame_idx,
            "center": [x, y]
        }

        self.coco_data["annotations"] = [
            ann for ann in self.coco_data["annotations"]
            if ann["frame_id"] != frame_idx
        ]

        self.coco_data["annotations"].append(annotation)
        self.annotation_id += 1
        return annotation

    def draw_display(self):
        if self.current_frame is None:
            return

        scale_factor = self.scale_percent / 100
        width = int(self.current_frame.shape[1] * scale_factor)
        height = int(self.current_frame.shape[0] * scale_factor)
        display = cv2.resize(self.current_frame, (width, height))

        for ann in self.coco_data["annotations"]:
            if ann["frame_id"] == self.current_frame_idx:
                cx, cy = ann["center"]
                x = int(cx * scale_factor)
                y = int(cy * scale_factor)
                cv2.circle(display, (x, y), 8, (0, 255, 0), 2)
                cv2.circle(display, (x, y), 2, (0, 255, 0), -1)

        if self.is_recording:
            mouse_x_scaled = int(self.mouse_x * scale_factor)
            mouse_y_scaled = int(self.mouse_y * scale_factor)
            cv2.drawMarker(display, (mouse_x_scaled, mouse_y_scaled),
                          (0, 0, 255), cv2.MARKER_CROSS, 20, 2)
            cv2.circle(display, (mouse_x_scaled, mouse_y_scaled),
                      int(self.bbox_size * scale_factor / 2), (0, 0, 255), 2)

        info_y = 30
        overlay = display.copy()
        cv2.rectangle(overlay, (0, 0), (500, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, display, 0.4, 0, display)

        cv2.putText(display, f"Frame: {self.current_frame_idx}/{self.total_frames}",
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        info_y += 30

        if self.is_recording:
            status, color = "RECORDING", (0, 0, 255)
        elif self.is_playing:
            status, color = "PLAYING", (0, 255, 255)
        else:
            status, color = "PAUSED", (200, 200, 200)

        cv2.putText(display, f"Status: {status}", (10, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        info_y += 30

        cv2.putText(display, f"Annotations: {len(self.coco_data['annotations'])}",
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        info_y += 30

        cv2.putText(display, f"Speed: {self.playback_speed}x",
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        info_y += 30

        if not self.is_recording:
            cv2.putText(display, "Press 'r' to record | SPACE=play",
                       (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        else:
            cv2.putText(display, "Move mouse to follow ball",
                       (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow(self.window_name, display)

    def save_to_file(self):
        output_file = os.path.join(self.output_dir, f"{self.video_name}_coco.json")
        self.coco_data["annotations"].sort(key=lambda x: x["frame_id"])
        self.coco_data["info"]["last_modified"] = datetime.now().isoformat()
        self.coco_data["info"]["total_annotations"] = len(self.coco_data["annotations"])

        with open(output_file, 'w') as f:
            json.dump(self.coco_data, f, indent=2)

        print(f"\n{'='*70}")
        print(f"✓ Saved: {output_file}")
        print(f"  Annotations: {len(self.coco_data['annotations'])}")
        print(f"  Resolution: {self.width}x{self.height}")
        print(f"{'='*70}\n")
        return output_file

    def load_existing_annotations(self):
        annotation_file = os.path.join(self.output_dir, f"{self.video_name}_coco.json")

        if os.path.exists(annotation_file):
            try:
                with open(annotation_file, 'r') as f:
                    loaded = json.load(f)
                    self.coco_data["annotations"] = loaded.get("annotations", [])
                    if self.coco_data["annotations"]:
                        self.annotation_id = max(ann["id"] for ann in self.coco_data["annotations"]) + 1
                print(f"✓ Loaded {len(self.coco_data['annotations'])} annotations")
                return True
            except Exception as e:
                print(f"⚠ Load error: {e}")
        return False

    def go_to_frame(self, frame_idx):
        if 0 <= frame_idx < self.total_frames:
            self.current_frame_idx = frame_idx
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, self.current_frame = self.cap.read()
            if ret:
                print(f"→ Frame {frame_idx}")
                return True
        return False

    def next_frame(self):
        if self.current_frame_idx < self.total_frames - 1:
            self.current_frame_idx += 1
            ret, self.current_frame = self.cap.read()
            return ret
        return False

    def prev_frame(self):
        if self.current_frame_idx > 0:
            return self.go_to_frame(self.current_frame_idx - 1)
        return False

    def run(self):
        self.load_existing_annotations()

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        ret, self.current_frame = self.cap.read()
        if not ret:
            print("✗ Cannot read first frame")
            return

        base_delay = int(1000 / self.fps)

        try:
            while True:
                self.draw_display()
                delay = max(1, int(base_delay / self.playback_speed))
                key = cv2.waitKey(delay) & 0xFF

                if self.is_playing:
                    if self.next_frame():
                        if self.is_recording:
                            self.add_annotation(self.current_frame_idx, self.mouse_x, self.mouse_y)
                            if self.current_frame_idx % 30 == 0:
                                print(f"Recording... Frame {self.current_frame_idx} | Total: {len(self.coco_data['annotations'])}")
                    else:
                        self.is_playing = False
                        print("✓ End of video")

                if key == ord('q'):
                    self.save_to_file()
                    break
                elif key == ord(' '):
                    self.is_playing = not self.is_playing
                    print(f"→ {'PLAYING' if self.is_playing else 'PAUSED'}")
                elif key == ord('r'):
                    self.is_recording = not self.is_recording
                    if self.is_recording:
                        print(f"🔴 RECORDING - Move mouse to follow ball")
                    else:
                        print(f"⏹ STOPPED - {len(self.coco_data['annotations'])} annotations")
                elif key == ord('n'):
                    self.is_playing = False
                    self.next_frame()
                elif key == ord('p'):
                    self.is_playing = False
                    self.prev_frame()
                elif key == ord('s'):
                    self.save_to_file()
                elif key == ord('g'):
                    self.is_playing = False
                    print("\nFrame number: ", end='', flush=True)
                    try:
                        self.go_to_frame(int(input()))
                    except ValueError:
                        print("Invalid")
                elif key == ord('+') or key == ord('='):
                    self.playback_speed = min(4, self.playback_speed + 0.5)
                    print(f"Speed: {self.playback_speed}x")
                elif key == ord('-'):
                    self.playback_speed = max(0.25, self.playback_speed - 0.5)
                    print(f"Speed: {self.playback_speed}x")
                elif key == ord('z'):
                    if self.scale_percent == 30:
                        self.scale_percent = 50
                    elif self.scale_percent == 50:
                        self.scale_percent = 70
                    else:
                        self.scale_percent = 30
                    print(f"Zoom: {self.scale_percent}%")

        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            print("\n✓ Session ended")


def main():
    if len(sys.argv) < 2:
        print("Usage: python annotator.py <video_path> [output_dir]")
        print("\nExamples:")
        print("  python annotator.py videos/match.mp4")
        print("  python annotator.py videos/match.mp4 my_annotations/")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR

    if not os.path.exists(video_path):
        print(f"✗ Video not found: {video_path}")
        sys.exit(1)

    try:
        annotator = BallAnnotator(video_path, output_dir=output_dir)
        annotator.run()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
