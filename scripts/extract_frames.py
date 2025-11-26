import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=1):
    """
    Extract frames from video for AI training

    Args:
        video_path: Path to video file
        output_folder: Folder to save frames
        frame_interval: Save every Nth frame (1 = all frames, 5 = every 5th frame)
    """

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # Open video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\nVideo Info:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Total frames: {total_frames}")
    print(f"  Frame interval: {frame_interval} (saving every {frame_interval} frame(s))")

    expected_frames = total_frames // frame_interval
    print(f"  Expected output: ~{expected_frames} frames")
    print(f"\nExtracting frames to: {output_folder}\n")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Save every Nth frame
        if frame_count % frame_interval == 0:
            # Format: frame_0001.png, frame_0002.png, etc.
            filename = f"frame_{frame_count:06d}.png"
            filepath = os.path.join(output_folder, filename)

            cv2.imwrite(filepath, frame)
            saved_count += 1

            # Progress indicator
            if saved_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {saved_count} frames saved ({progress:.1f}% of video)")

    cap.release()

    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Total frames processed: {frame_count}")
    print(f"Frames saved: {saved_count}")
    print(f"Output folder: {output_folder}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Configuration
    video_path = "videos/test.mp4"
    output_folder = "training_frames"

    # Frame interval options:
    # 1 = Save ALL frames (8027 frames for your video)
    # 5 = Save every 5th frame (~1605 frames)
    # 10 = Save every 10th frame (~803 frames)
    # 24 = Save 1 frame per second (~334 frames)

    frame_interval = 5  # Change this value as needed

    print("="*60)
    print("FRAME EXTRACTOR FOR AI TRAINING")
    print("="*60)

    extract_frames(video_path, output_folder, frame_interval)

    print("Next steps for AI training:")
    print("1. Use a labeling tool (LabelImg, CVAT, Roboflow)")
    print("2. Annotate ball positions in frames")
    print("3. Export annotations in YOLO format")
    print("4. Train YOLOv8 with your labeled data")

