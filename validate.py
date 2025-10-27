# eval_test.py
from ultralytics import YOLO

def main():
    model = YOLO(r"C:\Users\ronal\Desktop\PROJETS PERSO\1-FORMATIONS\DSTI\DeepLearning\PROJECT\Yolo fine tuning\runs\classify\train\weights\best.pt")

    metrics = model.val(
        data=r"C:\Users\ronal\Desktop\PROJETS PERSO\1-FORMATIONS\DSTI\DeepLearning\PROJECT\DatasetYolo",
        split="test",     # <-- use the /test set, not /val
        workers=0         # <-- Windows-friendly
        # imgsz=224, batch=64  # optional; use if you want to control them
    )
    print(metrics)  # shows top1/top5, loss, etc.

if __name__ == "__main__":
    main()
