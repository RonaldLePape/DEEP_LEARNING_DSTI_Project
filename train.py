# train.py
from ultralytics import YOLO

def main():
    model = YOLO("yolov8s-cls.pt")
    model.train(
        data=r"C:\Users\ronal\Desktop\PROJETS PERSO\1-FORMATIONS\DSTI\DeepLearning\PROJECT\DatasetYolo",
        epochs=50,
        imgsz=224,
        batch=64,
        workers=0  # or 2/4; 0 is the safest on Windows
    )

if __name__ == "__main__":
    main()
