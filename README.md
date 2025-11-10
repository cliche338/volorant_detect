# ⚔️ VALORANT Enemy Detector (By YOLOv5)

⭐⭐⭐Just my final project of crouse "Introduction to Imaging Processing" in college. It just can detect the enemy in pictures or videos, can't detect in real gameplay. IT ISN'T A CHEATING PROJECT⭐⭐⭐

This is a complete project for training and running a **YOLOv5** object detection model to detect enemies in VALORANT gameplay. This was developed as a solo final project for my Image Processing course.

The project can be used in two ways:
1.  **Inference:** Use the pre-trained `best.pt` model to detect enemies in new images or videos.
2.  **Training:** Re-train or fine-tune the model using a custom dataset.

---

## 📸 Demo

<img width="850" height="476" alt="image" src="https://github.com/user-attachments/assets/c4bf3e2c-1d0e-42c9-bfde-859aa39f1e8a" />


---

## 🛠️ Tech Stack 

* **Python 3.x**
* **YOLOv5** (by Ultralytics)
* **PyTorch**
* **OpenCV** (for video/image processing)
* **labelImg** (for data annotation)

---

## 🚀 1. How to Use (Inference with Pre-trained Model)

This guide assumes you have already trained a model and have a `best.pt` file.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/cliche338/](https://github.com/cliche338/)[your-repo-name].git
    cd [your-repo-name]
    ```

2.  **Install dependencies:**
    ```bash```
    # Install main YOLOv5 requirements
    pip install -r [https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt](https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt)
    pip install opencv-python
    ```

3.  **Run detection:**
    The `code_main.py` script is a wrapper that handles running `yolo predict` and organizing the output.

    ```bash
    # Detect from a single image
    python code_main.py path/to/your/image.jpg

    # Detect from a video file
    python code_main.py path/to/your/video.mp4

    # Detect from a folder of images
    python code_main.py path/to/your/folder/
    ```

4.  **Check results:**
    The detected images/videos will be saved in the `runs/detect/exp` (or the latest `expXX`) folder.

---

## 🏋️‍♂️ 2. How to Train (Replicating the Model)

This section describes the process to train the model from scratch.

### Step 1: Data Annotation

1.  **Gather images/videos:** Collect your raw training data.
2.  **Annotate:** Use **`labelImg`** to hand-draw bounding boxes around the enemies.
    * **Note:** On Windows, `labelImg.exe` must be **Run as Administrator** to avoid crashes.
3.  **Export:** Save the annotations as `.xml` files (PASCAL VOC format).

### Step 2: Convert Annotations

1.  Move all `.xml` files into one folder.
2.  Run the `code_VtoY.py` script to convert all `.xml` files into the YOLO-compatible `.txt` format.

### Step 3: Organize Dataset

Your `dataset` folder **must** follow this structure for the `data.yaml` file to work:

dataset/ ├── train/ 
       │ ├── images/ (contains img1.jpg, img2.jpg...) 
       │ └── labels/ (contains img1.txt, img2.txt...) 
       │ └── val/ 
       ├── images/ (contains img3.jpg, img4.jpg...) 
       └── labels/ (contains img3.txt, img4.txt...)

### Step 4: Create `data.yaml`

Create a `data.yaml` file in the root directory:
```yaml```
train: ./dataset/train
val: ./dataset/val

# number of classes
nc: [YOUR_NUMBER_OF_CLASSES, e.g., 1]

# class names
names: ['enemy'] # (or whatever your class name is)

### Step 5: Start Training
Download a pre-trained YOLOv5 model (e.g., yolov5s.pt).

Run the YOLO training command (this assumes code_main.py's train or train2 mode calls this):
yolo train model=yolov5s.pt data=data.yaml epochs=50 imgsz=640

Your best model (best.pt) will be saved in runs/train/[project_name]/weights/
