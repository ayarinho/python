from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import math
import base64
import numpy as np

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

@app.route('/detect', methods=['POST'])
def detect_hand():
    data = request.json
    encoded_image = data['image']
    decoded_image = base64.b64decode(encoded_image)
    image = cv2.imdecode(np.frombuffer(decoded_image, np.uint8), cv2.IMREAD_COLOR)

    # Traitement de l'image et détection des mains
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    hand_detected = False
    message = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            if wrist.y > index_finger_tip.y and calculate_distance(index_finger_tip, pinky_tip) > 0.15:
                is_open = True
                for i in range(4, 21, 4):
                    for j in range(i+1, 21, 4):
                        if calculate_distance(hand_landmarks.landmark[i], hand_landmarks.landmark[j]) < 0.06:
                            is_open = False
                            break
                    if not is_open:
                        break
                
                if is_open:
                    hand_detected = True
                    message = "Main levee et ouverte"
                    break

    return jsonify(hand_detected=hand_detected, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
