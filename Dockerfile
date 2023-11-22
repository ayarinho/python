FROM python:3.7-buster

WORKDIR /app

# Mettre à jour les paquets et installer les dépendances sans supprimer le cache
# Utiliser --fix-missing avec les commandes apt-get pour résoudre les problèmes de dépendances manquantes
RUN apt-get update -y -o APT::Update::Post-Invoke="" \
    && apt-get install -y libgl1-mesa-glx libglib2.0-0



# Installer Flask, OpenCV et MediaPipe
RUN pip install --no-cache-dir --quiet Flask opencv-python-headless mediapipe

COPY ["import cv2.py", "./"]

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "import cv2.py"]
