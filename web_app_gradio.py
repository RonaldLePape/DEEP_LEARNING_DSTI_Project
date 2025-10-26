# simple_top5_app.py
# Upload image → Predict (Top-5 only) → Reset

import gradio as gr
from ultralytics import YOLO
from PIL import Image
import numpy as np
import torch

# ==== CONFIG ====
MODEL_PATH = "./weights/best.pt"
IMSZ = 224  # keep same size as training

# ==== LOAD MODEL ONCE ====
device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = YOLO(MODEL_PATH)
MODEL.to(device)

def ensure_pil(x):
    if x is None:
        return None
    if isinstance(x, Image.Image):
        return x
    if isinstance(x, np.ndarray):
        return Image.fromarray(x)
    # last resort
    return Image.open(x)

def predict_top5(img):
    img = ensure_pil(img)
    if img is None:
        return {}
    # Standardize size for consistency with training
    img = img.resize((IMSZ, IMSZ), Image.BICUBIC)

    results = MODEL(img, imgsz=IMSZ, verbose=False)
    r = results[0]
    probs = r.probs.data.float().cpu().numpy()  # shape [num_classes]

    # Build top-5 dict {class_name: probability}
    top5_idx = np.argsort(-probs)[:5]
    top5 = {r.names[i]: float(probs[i]) for i in top5_idx}
    return top5

def reset_all():
    # Return values matching the outputs we want to clear
    return None, None  # clears the image and the label

with gr.Blocks(title="YOLOv8-CLS — Top-5 Classifier") as demo:
    gr.Markdown("## YOLOv8 Classifier\nUpload an image, then click **Predict** to see the **Top-5** classes.")

    with gr.Row():
        inp = gr.Image(type="pil", label="Upload image")
    with gr.Column():
        btn_predict = gr.Button("Predict", variant="primary")
        btn_reset = gr.Button("Reset")
    with gr.Row():
        out_top5 = gr.Label(num_top_classes=5, label="Top-5 predictions")

    btn_predict.click(predict_top5, inputs=inp, outputs=out_top5)
    btn_reset.click(reset_all, inputs=None, outputs=[inp, out_top5])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
