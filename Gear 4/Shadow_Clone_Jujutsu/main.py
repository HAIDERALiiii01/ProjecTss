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
import random
import pygame


# ── Pygame audio setup ───────────────────────────────────────────────────────
pygame.mixer.init()
pop_sound = pygame.mixer.Sound("assets/audio/pop.mp3")
pygame.mixer.music.load("assets/audio/audio.mp3")

guide_img1 = cv2.imread("assets/state-1.png", cv2.IMREAD_UNCHANGED)
guide_img2 = cv2.imread("assets/state-2.png", cv2.IMREAD_UNCHANGED)

# resize both to a small size once
GUIDE_SIZE = (125, 125)  # adjust to your liking
guide_img1 = cv2.resize(guide_img1, GUIDE_SIZE)
guide_img2 = cv2.resize(guide_img2, GUIDE_SIZE)



# ── MediaPipe aliases ────────────────────────────────────────────────────────
BaseOptions        = mp.tasks.BaseOptions
VisionRunningMode  = mp.tasks.vision.RunningMode

ImageSegmenter        = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions

HandLandmarker        = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult  = mp.tasks.vision.HandLandmarkerResult

mp_drawing        = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles
mp_hands          = mp.tasks.vision.HandLandmarksConnections


# ── ML model (gesture) ───────────────────────────────────────────────────────
interpreter = tf.lite.Interpreter(model_path="gesture_model.tflite")
interpreter.allocate_tensors()
input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()
scaler        = joblib.load("scaler.pkl")
encoder       = joblib.load("encoder.pkl")
labels        = list(encoder.classes_)


# ── Segmenter state ──────────────────────────────────────────────────────────
latest_mask   = None
mask_lock     = threading.Lock()
smoothed_mask = None


# ── Hand landmarker state ────────────────────────────────────────────────────
latest_result    = None
result_lock      = threading.Lock()
prediction_buffer = deque(maxlen=6)
stable_prediction = "none"
frame_count       = 0
confidence        = 0.0


# ── Clone / burst state ──────────────────────────────────────────────────────
clones                = []
burst_triggered       = False
burst_already_triggered = False
cloning_done = False
burst_frame           = 0
FLASH_FADE_FRAMES     = 5
STAGGER               = 1
blink_state = True
blink_timer = 0
BLINK_INTERVAL = 5  # frames between each blink toggle

# ── Smoke system ─────────────────────────────────────────────────────────────
SMOKE_FOLDERS     = ["smoke_1", "smoke_2", "smoke_3"]
SMOKE_FRAME_COUNT = 5
SMOKE_DURATION    = 0.6

smoke_assets = {}
for folder in SMOKE_FOLDERS:
    frames = []
    for i in range(1, SMOKE_FRAME_COUNT + 1):
        img = cv2.imread(f"assets/{folder}/{i}.png", cv2.IMREAD_UNCHANGED)
        frames.append(img)
    smoke_assets[folder] = frames

active_smokes = []


# ── Background ───────────────────────────────────────────────────────────────
# bg = cv2.imread("assets/bg.jpg")
bg = cv2.imread("assets/BG.png")


# ── Audio function ───────────────────────────────────────────────────────────
def play_audio_then_burst():
    global burst_triggered
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.05)
    burst_triggered = True

def draw_guide(canvas, img):
    h, w = canvas.shape[:2]
    ih, iw = img.shape[:2]
    x1 = w // 2 - iw // 2
    y1 = h - ih - 2

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(x1 + iw, w)
    y2 = min(y1 + ih, h)

    # clip image to fit
    img_clipped = img[:y2 - y1, :x2 - x1]

    if img.shape[2] == 4:
        a = img_clipped[:, :, 3:4].astype(np.float32) / 255.0
        roi = canvas[y1:y2, x1:x2].astype(np.float32)
        blended = roi * (1 - a) + img_clipped[:, :, :3].astype(np.float32) * a
        canvas[y1:y2, x1:x2] = blended.astype(np.uint8)
    else:
        canvas[y1:y2, x1:x2] = img_clipped

    return canvas
# ── Segmenter callback ───────────────────────────────────────────────────────
def result_callback(result, output_image, timestamp_ms):
    global latest_mask
    if result.category_mask is not None:
        raw = np.squeeze(result.category_mask.numpy_view()).copy()
        with mask_lock:
            latest_mask = raw


# ── Hand landmarker callback ─────────────────────────────────────────────────
def on_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    global latest_result
    with result_lock:
        latest_result = result


# ── Gesture feature extraction helpers ──────────────────────────────────────
def get_scale(hand):
    wrist     = hand[0]
    index_mcp = hand[5]
    pinky_mcp = hand[17]
    d1 = math.dist([index_mcp.x, index_mcp.y, index_mcp.z],
                   [wrist.x,     wrist.y,     wrist.z])
    d2 = math.dist([pinky_mcp.x, pinky_mcp.y, pinky_mcp.z],
                   [wrist.x,     wrist.y,     wrist.z])
    return (d1 + d2) / 2 or 1

def dist(a, b):
    return math.dist([a.x, a.y, a.z], [b.x, b.y, b.z])

def angle(a, b, c):
    ab  = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    cb  = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    dot = np.dot(ab, cb)
    mag = (np.linalg.norm(ab) * np.linalg.norm(cb)) + 1e-6
    return dot / mag

def extract_hand_features(hand):
    f     = []
    wrist = hand[0]

    dx = hand[5].x - wrist.x
    dy = hand[5].y - wrist.y
    dz = hand[5].z - wrist.z
    length = (dx**2 + dy**2 + dz**2) ** 0.5 or 1
    dx /= length
    dy /= length
    dz /= length

    scale = get_scale(hand)

    for lm in hand:
        x = (lm.x - wrist.x) / scale
        y = (lm.y - wrist.y) / scale
        z = (lm.z - wrist.z) / scale
        projection = x * dx + y * dy + z * dz
        f.extend([x, y, z, projection])

    f.extend([
        dist(hand[4],  hand[8])  / scale,
        dist(hand[8],  hand[12]) / scale,
        dist(hand[12], hand[16]) / scale,
        dist(hand[16], hand[20]) / scale,
    ])

    f.extend([
        angle(hand[0], hand[5], hand[6]),
        angle(hand[5], hand[6], hand[8]),
        angle(hand[0], hand[9], hand[10]),
    ])

    return f

def co_ordinates(lh, rh):
    features = []
    features.extend(extract_hand_features(lh) if lh else [0] * 91)
    features.extend(extract_hand_features(rh) if rh else [0] * 91)
    return features


# ── Smoke helpers ─────────────────────────────────────────────────────────────
def spawn_smoke(x, y, scale=1.0):
    scale *= 1.2
    folder = random.choice(SMOKE_FOLDERS)
    active_smokes.append({
        "x":      x,
        "y":      y,
        "scale":  scale,
        "start":  time.time(),
        "frames": smoke_assets[folder]
    })

def draw_smokes(canvas):
    now            = time.time()
    frame_duration = SMOKE_DURATION / SMOKE_FRAME_COUNT

    for i in range(len(active_smokes) - 1, -1, -1):
        s           = active_smokes[i]
        elapsed     = now - s["start"]
        frame_index = int(elapsed / frame_duration)

        if frame_index >= len(s["frames"]):
            active_smokes.pop(i)
            continue

        img = s["frames"][frame_index]
        if img is None:
            continue

        canvas = stamp_free(canvas, img, s["x"], s["y"], scale=s["scale"])

    return canvas


# ── Cutout helpers ────────────────────────────────────────────────────────────
def build_cutout_with_outline(frame, alpha):
    alpha_8u = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    r, g, b  = cv2.split(frame)
    return cv2.merge([r, g, b, alpha_8u])

def stamp_free(canvas, cutout_rgba, x_center, y_bottom, scale=0.5, flash=0.0):
    ch, cw = canvas.shape[:2]
    ph, pw = cutout_rgba.shape[:2]

    new_w   = int(pw * scale)
    new_h   = int(ph * scale)
    resized = cv2.resize(cutout_rgba, (new_w, new_h))

    x1 = int(x_center - new_w // 2)
    y1 = int(y_bottom  - new_h)

    if x1 < 0:
        resized = resized[:, -x1:]
        x1 = 0
    if y1 < 0:
        resized = resized[-y1:, :]
        y1 = 0

    x2    = min(x1 + resized.shape[1], cw)
    y2    = min(y1 + resized.shape[0], ch)
    patch = resized[:y2 - y1, :x2 - x1]

    if flash > 0:
        white     = np.ones_like(patch[:, :, :3], dtype=np.float32) * 255
        patch_rgb = patch[:, :, :3].astype(np.float32)
        patch_rgb = patch_rgb * (1 - flash) + white * flash
        patch     = np.dstack([patch_rgb.astype(np.uint8), patch[:, :, 3]])

    a       = patch[:, :, 3:4].astype(np.float32) / 255.0
    roi     = canvas[y1:y2, x1:x2].astype(np.float32)
    blended = roi * (1 - a) + patch[:, :, :3].astype(np.float32) * a
    canvas[y1:y2, x1:x2] = blended.astype(np.uint8)

    return canvas


# ── MediaPipe options ─────────────────────────────────────────────────────────
segmenter_options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path="selfie_multiclass_256x256.tflite"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    output_category_mask=True,
    result_callback=result_callback
)

landmarker_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    result_callback=on_result
)


# ── Webcam ────────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


# ── Main loop ─────────────────────────────────────────────────────────────────
with ImageSegmenter.create_from_options(segmenter_options) as segmenter:
    with HandLandmarker.create_from_options(landmarker_options) as landmarker:
        while True:

            # ── 1. Read frame ─────────────────────────────────────────────
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            run_model    = (frame_count % 2 == 0)
            frame        = cv2.flip(frame, 1)
            h, w         = frame.shape[:2]

            # ── 2. Send to both models (async) ────────────────────────────
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            )
            frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

            segmenter.segment_async(mp_image, frame_timestamp_ms)
            landmarker.detect_async(mp_image, frame_timestamp_ms)

            # ── 3. Get segmentation mask ──────────────────────────────────
            with mask_lock:
                current_mask = latest_mask.copy() if latest_mask is not None else None

            cutout = None
            if current_mask is not None:
                mask_f = (current_mask > 0).astype(np.float32)
                if smoothed_mask is None:
                    smoothed_mask = mask_f
                else:
                    smoothed_mask = 0.8 * smoothed_mask + 0.2 * mask_f

                resized_mask = cv2.resize(smoothed_mask, (w, h))
                alpha        = cv2.GaussianBlur(resized_mask, (21, 21), 0)
                alpha        = np.clip(alpha, 0, 1)
                cutout       = build_cutout_with_outline(frame, alpha)

            # ── 4. Get hand landmarks ─────────────────────────────────────
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
                
            # ── 5. Run gesture model ──────────────────────────────────────
            if run_model:
                if left_hand is None and right_hand is None:
                    prediction_buffer.append("none")
                    confidence = 1.0
                else:
                    f = co_ordinates(left_hand, right_hand)
                    if len(f) == 182:
                        input_data = scaler.transform(np.array(f).reshape(1, -1)).astype(np.float32)
                        interpreter.set_tensor(input_details[0]['index'], input_data)
                        interpreter.invoke()
                        prediction = interpreter.get_tensor(output_details[0]['index'])

                        pred_index = np.argmax(prediction[0])
                        confidence = prediction[0][pred_index]

                        if confidence < 0.8:
                            current_pred = "none"
                        else:
                            current_pred = labels[pred_index]
                            if current_pred == "jujutsu_sign" and confidence < 0.95:
                                current_pred = "none"
                            if current_pred == "jujutsu_sign":
                                if left_hand is None or right_hand is None:
                                    current_pred = "none"

                        prediction_buffer.append(current_pred)

            # ── 6. Stable prediction ──────────────────────────────────────
            if prediction_buffer:
                most_common = Counter(prediction_buffer).most_common(1)[0][0]
                if most_common != stable_prediction:
                    if prediction_buffer.count(most_common) >= 3:
                        stable_prediction = most_common

            # ── 7. Trigger burst on jujutsu_sign ─────────────────────────
            if stable_prediction == "jujutsu_sign" and not burst_already_triggered and not cloning_done:
                burst_already_triggered = True
                threading.Thread(target=play_audio_then_burst, daemon=True).start()

            if stable_prediction != "jujutsu_sign":
                burst_already_triggered = False

            # ── 8. Handle burst clones ────────────────────────────────────
            if burst_triggered:
                clones.clear()
                burst_frame = 0

                front_steps   = [-2, -1, 1, 2]
                back_steps    = [-3, -2, -1, 0, 1, 2, 3]
                far_steps     = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

                front_spacing = int(w * 0.12)
                back_spacing  = int(w * 0.12)
                far_spacing   = int(w * 0.12)

                for i, step in enumerate(front_steps):
                    clones.append({
                        "x": w // 2 + step * front_spacing,
                        "y": h,
                        "scale": 0.92,
                        "row": 1,
                        "smoke_spawned": False,
                        "appear_at_frame": i * STAGGER
                    })

                front_done_at = len(front_steps) * STAGGER
                for i, step in enumerate(back_steps):
                    clones.append({
                        "x": w // 2 + step * back_spacing,
                        "y": h - int(h * 0.30),
                        "scale": 0.78,
                        "row": 2,
                        "smoke_spawned": False,
                        "appear_at_frame": front_done_at + i * STAGGER
                    })

                # back_done_at = front_done_at + len(back_steps) * STAGGER
                # for i, step in enumerate(far_steps):
                #     clones.append({
                #         "x": w // 2 + step * far_spacing,
                #         "y": h - int(h * 0.55),
                #         "scale": 0.62,
                #         "row": 3,
                #         "smoke_spawned": False,
                #         "appear_at_frame": back_done_at + i * STAGGER
                #     })

                burst_triggered = False

            # advance burst frame counter
            if clones:
                cloning_done = True  # lock — no new cloning while clones are active
                last_frame_needed = max(c["appear_at_frame"] for c in clones)
                if burst_frame <= last_frame_needed + FLASH_FADE_FRAMES:
                    burst_frame += 1
            else:
                cloning_done = False  # unlock — clones are gone, ready for next trigger
            

            ## ── 9. Render ─────────────────────────────────────────────────
            if cutout is not None:
                # canvas = frame.copy()
                canvas = cv2.resize(bg, (w, h))

                # render clones back-to-front
                for clone in sorted(clones, key=lambda c: c["row"], reverse=True):
                    if burst_frame >= clone["appear_at_frame"]:

                        if not clone["smoke_spawned"]:
                            clone["smoke_spawned"] = True
                            cx = clone["x"]
                            cy = clone["y"] - int(60 * clone["scale"])
                            spawn_smoke(cx - 15 + random.randint(-5, 5), cy, clone["scale"])
                            spawn_smoke(cx + 15 + random.randint(-5, 5), cy, clone["scale"])
                            threading.Thread(target=pop_sound.play, daemon=True).start()

                        age   = burst_frame - clone["appear_at_frame"]
                        flash = max(0.0, 1.0 - age / 5)
                        canvas = stamp_free(canvas, cutout, clone["x"], clone["y"], clone["scale"], flash)

                # stamp main user on top
                canvas = stamp_free(canvas, cutout, w // 2, h, scale=1.0)

                # draw hand landmarks
                if result_snapshot and result_snapshot.hand_landmarks:
                    for i, hand_landmarks in enumerate(result_snapshot.hand_landmarks):
                        mp_drawing.draw_landmarks(
                            canvas,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )

                # draw smoke
                canvas = draw_smokes(canvas)

                # output is canvas now — guide draws on top of final canvas
                output = canvas

                # ── Guide image ───────────────────────────────────────────
                if not clones:
                    if burst_already_triggered:  # audio playing, show image_2 blinking
                        blink_timer += 1
                        if blink_timer >= BLINK_INTERVAL:
                            blink_state = not blink_state
                            blink_timer = 0
                        if blink_state:
                            output = draw_guide(output, guide_img2)
                    else:  # idle, show image_1
                        blink_state = True
                        blink_timer = 0
                        output = draw_guide(output, guide_img1)

            else:
                output = frame

            cv2.imshow("Shadow Clone Jutsu", output)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
