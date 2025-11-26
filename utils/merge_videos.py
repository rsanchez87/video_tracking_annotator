#!/usr/bin/env python3
"""Merge multiple video files from the same match by timestamp"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import json

def get_video_creation_time(video_path):
    """Get video creation timestamp from filename or metadata"""
    filename = Path(video_path).name

    try:
        parts = filename.split('_')
        if len(parts) >= 3 and len(parts[1]) >= 14:
            timestamp_str = parts[1][:14]
            return datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
    except:
        pass

    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', video_path],
            capture_output=True,
            text=True,
            check=True
        )
        metadata = json.loads(result.stdout)

        if 'format' in metadata and 'tags' in metadata['format']:
            creation_time = metadata['format']['tags'].get('creation_time')
            if creation_time:
                return datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
    except:
        pass

    stat = os.stat(video_path)
    return datetime.fromtimestamp(stat.st_mtime)

def get_video_duration(video_path):
    """Get video duration in seconds"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except:
        return 0


def get_video_codec_info(video_path):
    """Get basic codec information"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=codec_name,width,height',
             '-of', 'json', video_path],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        if 'streams' in data and len(data['streams']) > 0:
            return data['streams'][0]
    except:
        pass
    return {}



def merge_videos(video_paths, output_path, sort_by_timestamp=True):
    """Merge videos into a single file using copy mode (fast, no re-encoding)"""

    if not video_paths:
        print("✗ No video files provided")
        return False

    print(f"\n{'='*70}")
    print(f"VIDEO MERGER")
    print(f"{'='*70}")
    print(f"Input videos: {len(video_paths)}")

    video_info = []
    for video_path in video_paths:
        if not os.path.exists(video_path):
            print(f"✗ Video not found: {video_path}")
            return False

        timestamp = get_video_creation_time(video_path)
        duration = get_video_duration(video_path)
        codec_info = get_video_codec_info(video_path)

        video_info.append({
            'path': video_path,
            'timestamp': timestamp,
            'duration': duration,
            'codec': codec_info
        })

        print(f"\n  {Path(video_path).name}")
        print(f"    Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Duration: {duration:.1f}s ({duration/60:.1f} min)")
        if codec_info:
            print(f"    Codec: {codec_info.get('codec_name', 'unknown')} "
                  f"{codec_info.get('width', '?')}x{codec_info.get('height', '?')}")

    if sort_by_timestamp:
        video_info.sort(key=lambda x: x['timestamp'])
        print(f"\n✓ Videos sorted by timestamp")

    print(f"\nMerge order:")
    for i, info in enumerate(video_info, 1):
        print(f"  {i}. {Path(info['path']).name}")

    total_duration = sum(info['duration'] for info in video_info)
    print(f"\nTotal duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")

    concat_file = 'concat_list.txt'
    with open(concat_file, 'w') as f:
        for info in video_info:
            f.write(f"file '{os.path.abspath(info['path'])}'\n")

    try:
        print(f"\n{'='*70}")
        print(f"Merging videos (copy mode - no re-encoding)...")
        print(f"{'='*70}\n")

        ffmpeg_cmd = [
            'ffmpeg',
            '-f', 'concat', '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y', output_path
        ]

        result = subprocess.run(ffmpeg_cmd, check=False)

        os.remove(concat_file)

        if result.returncode != 0:
            print(f"\n✗ FFmpeg failed")
            return False

        output_duration = get_video_duration(output_path)

        print(f"\n{'='*70}")
        print(f"✓ Videos merged successfully!")
        print(f"{'='*70}")
        print(f"Output: {output_path}")
        print(f"Duration: {output_duration:.1f}s ({output_duration/60:.1f} min)")
        print(f"Videos merged: {len(video_info)}")

        print(f"{'='*70}\n")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        if os.path.exists(concat_file):
            os.remove(concat_file)
        return False



def main():
    if len(sys.argv) < 3:
        print("Usage: python merge_videos.py <output.mp4> <video1.mp4> <video2.mp4> [video3.mp4 ...]")
        print("\nExamples:")
        print("  python merge_videos.py merged_match.mp4 part1.mp4 part2.mp4 part3.mp4")
        print("  python merge_videos.py full_game.mp4 videos/*.mp4")
        print("\nNote: Videos will be automatically sorted by timestamp")
        print("      Requires ffmpeg installed: sudo apt install ffmpeg")
        sys.exit(1)

    output_path = sys.argv[1]
    video_paths = sys.argv[2:]

    if os.path.exists(output_path):
        response = input(f"⚠ Output file {output_path} already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("✗ Cancelled")
            sys.exit(1)

    try:
        subprocess.run(['ffmpeg', '-version'],
                      capture_output=True,
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg not found. Please install:")
        print("  sudo apt install ffmpeg")
        sys.exit(1)

    success = merge_videos(video_paths, output_path)

    if success:
        print(f"Next steps:")
        print(f"  1. Annotate merged video:")
        print(f"     python motion_detector/annotator.py {output_path}")
        print(f"  2. View annotations:")
        print(f"     python utils/view_annotations.py annotations/{Path(output_path).stem}_coco.json {output_path}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

