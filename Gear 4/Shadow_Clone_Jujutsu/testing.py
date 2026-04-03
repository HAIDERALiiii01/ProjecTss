import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarkerResult
import numpy as np
import tensorflow as tf
import joblib
import time
import threading
import math
from collections import deque, Counter


# Load model, scaler, encoder
model = tf.keras.models.load_model("gesture_model.keras")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")
labels = list(encoder.classes_)  # Maps index → label

# MediaPipe hand landmarker
model_path = 'hand_landmarker.task'
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles
mp_hands = mp.tasks.vision.HandLandmarksConnections

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

latest_result = None
result_lock = threading.Lock()
prediction_buffer = deque(maxlen=6)   # last 5 frames
stable_prediction = "none"
frame_count = 0
# run_model = True
confidence = 0.0

# Callback for hand landmark results
def on_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):  # type: ignore
    global latest_result
    with result_lock:
        latest_result = result

# Helper functions for feature extraction
def get_scale(hand):
    wrist = hand[0]
    index_mcp = hand[5]
    pinky_mcp = hand[17]
    d1 = math.dist([index_mcp.x,index_mcp.y,index_mcp.z],[wrist.x,wrist.y,wrist.z])
    d2 = math.dist([pinky_mcp.x,pinky_mcp.y,pinky_mcp.z],[wrist.x,wrist.y,wrist.z])
    return (d1+d2)/2 or 1

def dist(a,b):
    return math.dist([a.x,a.y,a.z],[b.x,b.y,b.z])

def angle(a,b,c):
    ab = np.array([a.x-b.x, a.y-b.y, a.z-b.z])
    cb = np.array([c.x-b.x, c.y-b.y, c.z-b.z])
    dot = np.dot(ab, cb)
    mag = (np.linalg.norm(ab) * np.linalg.norm(cb)) + 1e-6
    return dot/mag

def hands(hand):
    f = []
    wrist = hand[0]

    # Direction vector (wrist → index MCP)
    dx = hand[5].x - wrist.x
    dy = hand[5].y - wrist.y
    dz = hand[5].z - wrist.z

    length = (dx**2 + dy**2 + dz**2) ** 0.5 or 1

    # Normalize direction
    dx /= length
    dy /= length
    dz /= length

    scale = get_scale(hand)

    for lm in hand:
        x = (lm.x - wrist.x) / scale
        y = (lm.y - wrist.y) / scale
        z = (lm.z - wrist.z) / scale

        # project onto direction (rotation robustness)
        projection = x*dx + y*dy + z*dz

        f.extend([x, y, z, projection])
    # important distances
    f.extend([
    dist(hand[4], hand[8]) / scale,
    dist(hand[8], hand[12]) / scale,
    dist(hand[12], hand[16]) / scale,
    dist(hand[16], hand[20]) / scale
    ])
        
    f.extend([
    angle(hand[0], hand[5], hand[6]),  # index base
    angle(hand[5], hand[6], hand[8]),  # index finger
    angle(hand[0], hand[9], hand[10]), # middle base
    ])
        
    return f


def co_ordinates(lh, rh):
    features = []

    if lh:
        features.extend(hands(lh))   # ✅ flatten
    else:
        features.extend([0]*91)      # left hand missing

    if rh:
        features.extend(hands(rh))   # ✅ flatten
    else:
        features.extend([0]*91)      # right hand missing

    return features

# Create hand landmarker
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    result_callback=on_result
)

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        run_model = (frame_count % 2 == 0)
        frame = cv2.flip(frame, 1)
        frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        left_hand, right_hand = None, None
        with result_lock:
            result_snapshot = latest_result

        if result_snapshot and result_snapshot.hand_landmarks:
            for i, hand_landmarks in enumerate(result_snapshot.hand_landmarks):
                handedness_info = result_snapshot.handedness[i] if i < len(result_snapshot.handedness) else None
                if handedness_info:
                    hand_type = handedness_info[0].category_name
                    if hand_type == "Left":
                        left_hand = hand_landmarks
                    elif hand_type == "Right":
                        right_hand = hand_landmarks

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        if run_model:
            if left_hand is None and right_hand is None:
                prediction_buffer.append("none")
                confidence = 1.0
            else:
                f = co_ordinates(left_hand, right_hand)

                if len(f) == 182:
                    input_data = scaler.transform(np.array(f).reshape(1,-1))
                    prediction = model.predict(input_data, verbose=0)

                    pred_index = np.argmax(prediction[0])
                    confidence = prediction[0][pred_index]

                    if confidence < 0.8:
                        current_pred = "none"
                    else:
                        current_pred = labels[pred_index]

                        # stricter jujutsu control
                        if current_pred == "jujutsu_sign":
                            if left_hand is None or right_hand is None:
                                current_pred = "none"

                    prediction_buffer.append(current_pred)

        # Always compute final result (even if model not run)
        if prediction_buffer:
            most_common = Counter(prediction_buffer).most_common(1)[0][0]

            if most_common != stable_prediction:
                if prediction_buffer.count(most_common) >= 3:
                    stable_prediction = most_common

        result_text = stable_prediction

        # Draw EVERY frame (not just when model runs)
        color = (0,255,0) if result_text != "none" else (0,0,255)
        cv2.putText(frame, f"{result_text}", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Conf: {confidence:.2f}", (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()