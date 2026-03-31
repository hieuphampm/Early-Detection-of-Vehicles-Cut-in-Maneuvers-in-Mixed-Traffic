import os
import shutil

INPUT_ROOT = "data_1"          
OUTPUT_DIR = "images_dataset"
EXTENSIONS = (".jpg", ".jpeg", ".png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

counter = 0

for folder in sorted(os.listdir(INPUT_ROOT)):
    folder_path = os.path.join(INPUT_ROOT, folder)
    if not os.path.isdir(folder_path):
        continue

    images = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(EXTENSIONS)
    ])

    print(f"Processing {folder} ({len(images)} images)")

    for img in images:
        src = os.path.join(folder_path, img)
        dst_name = f"image_{counter:05d}.jpg"
        dst = os.path.join(OUTPUT_DIR, dst_name)

        shutil.copy2(src, dst)
        counter += 1

print(f"Done! Total images: {counter}")
