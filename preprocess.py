import os
import cv2
import numpy as np

# ==========================================
# SETTINGS
# ==========================================
IMG_SIZE = 64

DATASET_PATH = "dataset"

# IMPORTANT:
# 0 = Uninfected
# 1 = Parasitized
CATEGORIES = [
    "Uninfected",
    "Parasitized"
]

MAX_IMAGES_PER_CLASS = 2500

data = []
labels = []

# ==========================================
# CREATE DATASET
# ==========================================
def create_data():

    for category in CATEGORIES:

        path = os.path.join(DATASET_PATH, category)

        label = CATEGORIES.index(category)

        count = 0

        print(f"\nLoading {category} images...")

        for img_name in os.listdir(path):

            if count >= MAX_IMAGES_PER_CLASS:
                break

            try:
                img_path = os.path.join(path, img_name)

                img = cv2.imread(img_path)

                if img is None:
                    continue

                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

                img = img.astype("float32") / 255.0

                data.append(img)

                labels.append(label)

                count += 1

            except Exception as e:
                print("Error:", e)

        print(f"{category}: {count} images loaded")

    return np.array(data, dtype="float32"), np.array(labels)

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    os.makedirs("model", exist_ok=True)

    X, y = create_data()

    print("\nDataset Shape:", X.shape)
    print("Labels Shape:", y.shape)

    # VERY IMPORTANT
    print("\nUnique Labels:", np.unique(y))

    np.save("model/X.npy", X)
    np.save("model/y.npy", y)

    print("\nPreprocessing completed successfully!")