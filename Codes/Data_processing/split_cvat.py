import os
import shutil
import math

INPUT_DIR = "images_dataset"
OUTPUT_ROOT = "cvat_split"
NUM_FOLDERS = 20
EXTENSIONS = (".jpg", ".jpeg", ".png")

os.makedirs(OUTPUT_ROOT, exist_ok=True)

images = sorted([
    f for f in os.listdir(INPUT_DIR)
    if f.lower().endswith(EXTENSIONS)
])

total = len(images)
images_per_folder = math.ceil(total / NUM_FOLDERS)

print(f"Total images: {total}")
print(f"Images per folder: ~{images_per_folder}")

for i in range(NUM_FOLDERS):
    batch_dir = os.path.join(OUTPUT_ROOT, f"batch_{i+1:02d}")
    os.makedirs(batch_dir, exist_ok=True)

    start = i * images_per_folder
    end = min(start + images_per_folder, total)

    for img in images[start:end]:
        src = os.path.join(INPUT_DIR, img)
        dst = os.path.join(batch_dir, img)
        shutil.copy2(src, dst)

    print(f"batch_{i+1:02d}: {end - start} images")

print("Done splitting for CVAT!")
