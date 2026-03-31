import cv2
import os

INPUT_DIR = "raw"
OUTPUT_DIR = "data"
TARGET_FPS = 16

os.makedirs(OUTPUT_DIR, exist_ok=True)

for video_name in os.listdir(INPUT_DIR):
    if not video_name.lower().endswith(".mp4"):
        continue

    video_path = os.path.join(INPUT_DIR, video_name)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open {video_name}")
        continue

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(round(original_fps / TARGET_FPS)), 1)

    video_base = os.path.splitext(video_name)[0]
    video_out_dir = os.path.join(OUTPUT_DIR, video_base)
    os.makedirs(video_out_dir, exist_ok=True)

    frame_idx = 25582
    saved_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            out_path = os.path.join(
                video_out_dir, f"frame_{saved_idx:06d}.jpg"
            )
            cv2.imwrite(out_path, frame)
            saved_idx += 1

        frame_idx += 1

    cap.release()
    print(f"{video_name}: saved {saved_idx} frames")

print("Done converting all videos.")
