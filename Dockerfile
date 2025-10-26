# Image légère Python
FROM python:3.11-slim

# Déps système utiles à ultralytics/opencv/PIL
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential ffmpeg libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Répertoire app
WORKDIR /app

# Déps Python (torch CPU + gradio + ultralytics + pillow + numpy)
# NB: torch CPU via l’index officiel CPU
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
      "torch==2.*" "torchvision==0.*" "torchaudio==2.*" \
      --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir gradio ultralytics pillow numpy

# Copier le code + poids
COPY Web_app_gradio.py /app/
# Place ton best.pt à côté du Dockerfile puis copie-le :
COPY weights/best.pt /app/weights/best.pt

# Variables d’env pour Gradio (optionnel, ton code fixe déjà host/port)
#ENV GRADIO_SERVER_NAME=0.0.0.0
#ENV GRADIO_SERVER_PORT=7860

EXPOSE 7860

# Démarrage
CMD ["python", "Web_app_gradio.py"]
