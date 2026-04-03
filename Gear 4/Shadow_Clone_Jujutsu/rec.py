import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarkerResult
import time
import csv
import threading

model_path = 'hand_landmarker.task'

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles
    
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# open webcam (0 = default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not found")
    exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

left_hand = None
right_hand = None
countdown_time = 5
timer_duration = 8
datasets = []
features = []
latest_result = None
result_lock = threading.Lock()
recording = False
current_label = None
start_time = None
last_sample_time = 0
sample_interval = 0.1   # 0.1 sec = 10 samples per second
FEATURE_SIZE = 182
MIN_HAND_CONFIDENCE = 0.7

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    global latest_result
    with result_lock:
        latest_result = result

def is_stable(new_features, last_features, threshold=0.02):
    if not last_features:
        return True
    
    diff = sum(abs(a - b) for a, b in zip(new_features, last_features)) / len(new_features)
    return diff < threshold

def is_blurry(frame, threshold=300):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(laplacian_var)
    return laplacian_var < threshold

def rec_display(frame, lh, rh, current_l, elapsed):
    global recording, start_time, features, current_label, last_sample_time
    new_features = None
    if elapsed < countdown_time:
        cv2.putText(frame, f"Get Ready for {current_l}: {int(countdown_time - elapsed)}s",
                    (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    elif elapsed < timer_duration:
        cv2.putText(frame, f"Recording {current_l}: {int(timer_duration - elapsed)}s",
                    (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
        current_time = time.time()
        
        if current_time - last_sample_time > sample_interval:
            if current_l == "none":
                new_features = [0]*FEATURE_SIZE
                if lh or rh:
                    new_features = co_ordinates(lh, rh)
                    if new_features and len(new_features) != FEATURE_SIZE:
                        print("Feature size error:", len(new_features))
                else:
                    # optional: add zero vector
                    new_features = [0]*FEATURE_SIZE   # same size as your feature vector
            else:
                if lh or rh:
                    new_features = co_ordinates(lh, rh)
                    if new_features and len(new_features) != FEATURE_SIZE:
                        print("Feature size error:", len(new_features))
            

            if new_features is not None:
                # Check blur
                if not is_blurry(frame):
                    # Check hand confidence for each hand
                    lh_ok = all(cls.score >= MIN_HAND_CONFIDENCE for h in result_snapshot.handedness for cls in h if cls.category_name == "Left") if lh else True
                    rh_ok = all(cls.score >= MIN_HAND_CONFIDENCE for h in result_snapshot.handedness for cls in h if cls.category_name == "Right") if rh else True
                    
                    if lh_ok and rh_ok:
                        # Only save frame if it’s different enough
                        if not features or not is_stable(new_features, features[-1]):
                            features.append(new_features)
            
            last_sample_time = current_time

    else:
        cv2.putText(frame, f"Dataset Collected for {current_l}!", (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        # Save collected data
        if features and current_l:
            for f in features:
                datasets.append([current_l] + f)
        if datasets:
            with open("test_dataset.csv", "a", newline="") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerows(datasets)
            datasets.clear()
        # Reset recording state
        recording = False
        start_time = None
        features = []
        current_label = None
        
        
def draw(frame, result_snapshot):
    left_hand = None
    right_hand = None
    for i, hand_landmarks in enumerate(result_snapshot.hand_landmarks):
        handedness_info = result_snapshot.handedness[i] if i < len(result_snapshot.handedness) else None
        if handedness_info:
            score = handedness_info[0].score
            hand_type = handedness_info[0].category_name
            # hand_type = "Left" if hand_type == "Right" else "Right"
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
             
    return left_hand, right_hand

def get_scale(hand):
    wrist = hand[0]
    index_mcp = hand[5]
    pinky_mcp = hand[17]
    
    d1 = ((index_mcp.x - wrist.x)**2 + (index_mcp.y - wrist.y)**2 + (index_mcp.z - wrist.z)**2) ** 0.5
    d2 = ((pinky_mcp.x - wrist.x)**2 + (pinky_mcp.y - wrist.y)**2 + (pinky_mcp.z - wrist.z)**2) ** 0.5
    
    return (d1 + d2) / 2 or 1

def dist(a, b):
    return ((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)**0.5

def angle(a, b, c):
    # angle at point b
    ab = [a.x-b.x, a.y-b.y, a.z-b.z]
    cb = [c.x-b.x, c.y-b.y, c.z-b.z]
    
    dot = sum(x*y for x,y in zip(ab, cb))
    mag1 = sum(x*x for x in ab) ** 0.5
    mag2 = sum(x*x for x in cb) ** 0.5
    
    return dot / (mag1 * mag2 + 1e-6)

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
    
   
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    # min_tracking_confidence=0.6,
    result_callback=print_result
)


# Map keys to labels
key_labels = {ord('0'): "none",
        ord('1'): "jujutsu_sign",
        ord('2'): "not_jujutsu_sign",
        ord('3'): "thumbs_up",
        ord('4'): "thumbs_down",
        ord('5'): "peace_sign",
        ord('6'): "open_palm",
        ord('7'): "random"}

key_counts = {label: 0 for label in key_labels.values()} 

with HandLandmarker.create_from_options(options) as landmarker:   
    while True: 
        ret, frame = cap.read()   # read frame from camera
        key = cv2.waitKey(1) & 0xFF
        
        if ret == False:
            break
        
        
        frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        
        frame = cv2.flip(frame, 1)
        # frame_small = cv2.resize(frame, (640, 480))
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        landmarker.detect_async(mp_image, frame_timestamp_ms) 
        
        with result_lock:
            result_snapshot = latest_result      
        
        lh, rh = None, None
        
        if result_snapshot and result_snapshot.hand_landmarks:
            lh, rh = draw(frame, result_snapshot)

        if recording:
            elapsed = time.time() - start_time
            remaining = timer_duration - elapsed
            rec_display(frame, lh, rh, current_label, elapsed)            

        if not recording and key in key_labels:
            current_label = key_labels[key]
            key_counts[current_label] += 1
            recording = True
            start_time = time.time()  # Initialize the timer once
            features = []             # Reset features for new recording
            last_sample_time = 0
            print("Pressed:", current_label, "Total so far:", key_counts[current_label])
            

                            
        cv2.imshow("Webcam", frame)  # show the frame
                
        # press q to close the window
        if key == ord('q'):
            break
        
        time.sleep(0.001)
    

cap.release()
cv2.destroyAllWindows()

