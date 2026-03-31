import os
import subprocess
from pathlib import Path

VIDEO_DIR = "raw_2"
OUTPUT_DIR = "aus_frames"
FPS = 16

os.makedirs(OUTPUT_DIR, exist_ok=True)

video_exts = (".mp4", ".avi", ".mov", ".mkv")

for video_path in Path(VIDEO_DIR).glob("*"):
    if video_path.suffix.lower() not in video_exts:
        continue

    video_name = video_path.stem
    out_dir = Path(OUTPUT_DIR) / video_name
    out_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = str(out_dir / "%06d.jpg")

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",     
        "-err_detect", "ignore_err",  
        "-i", str(video_path),
        "-vf", f"fps={FPS}",
        "-q:v", "2",
        output_pattern
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] {video_name}")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed decoding {video_name}")
