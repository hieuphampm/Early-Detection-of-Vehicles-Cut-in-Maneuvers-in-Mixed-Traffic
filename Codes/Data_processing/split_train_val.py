import os
import random
import shutil

# ================= CONFIG =================
IMAGE_DIR = "batch_36"
LABEL_DIR = "train_batch_36"

VAL_RATIO = 0.2   # 0.2 = 20%, 0.3 = 30%
SEED = 42
MOVE_FILES = True  # True = move, False = copy
# ==========================================

random.seed(SEED)

IMG_EXTS = (".jpg", ".jpeg", ".png")

# output dirs
img_train_dir = "Data/train_batch_36_images"
img_val_dir   = "Data/val_batch_36_images"
lbl_train_dir = "Data/train_batch_36_labels"
lbl_val_dir   = "Data/val_batch_36_labels"

for d in [img_train_dir, img_val_dir, lbl_train_dir, lbl_val_dir]:
    os.makedirs(d, exist_ok=True)

pairs = []
skipped_no_label = 0
skipped_empty_label = 0

for fname in os.listdir(IMAGE_DIR):
    if not fname.lower().endswith(IMG_EXTS):
        continue

    stem = os.path.splitext(fname)[0]
    img_path = os.path.join(IMAGE_DIR, fname)
    lbl_path = os.path.join(LABEL_DIR, stem + ".txt")

    if not os.path.exists(lbl_path):
        skipped_no_label += 1
        continue

    if os.path.getsize(lbl_path) == 0:
        skipped_empty_label += 1
        continue

    pairs.append((img_path, lbl_path))

print(f"Valid image-label pairs: {len(pairs)}")
print(f"Skipped (no label):      {skipped_no_label}")
print(f"Skipped (empty label):   {skipped_empty_label}")

random.shuffle(pairs)
val_count = int(len(pairs) * VAL_RATIO)
val_pairs = pairs[:val_count]
train_pairs = pairs[val_count:]

def transfer(src, dst):
    if MOVE_FILES:
        shutil.move(src, dst)
    else:
        shutil.copy2(src, dst)

# move/copy validation
for img_path, lbl_path in val_pairs:
    transfer(img_path, os.path.join(img_val_dir, os.path.basename(img_path)))
    transfer(lbl_path, os.path.join(lbl_val_dir, os.path.basename(lbl_path)))

# move/copy train
for img_path, lbl_path in train_pairs:
    transfer(img_path, os.path.join(img_train_dir, os.path.basename(img_path)))
    transfer(lbl_path, os.path.join(lbl_train_dir, os.path.basename(lbl_path)))

print(f"Train samples: {len(train_pairs)}")
print(f"Val samples:   {len(val_pairs)}")
