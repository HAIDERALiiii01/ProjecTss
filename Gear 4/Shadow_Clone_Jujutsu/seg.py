import cv2
import mediapipe as mp
import numpy as np
import threading
import time
import os
import random
import pygame

# At the top, once
pygame.mixer.init()
pop_sound = pygame.mixer.Sound("assets/audio/pop.mp3")
pygame.mixer.music.load("assets/audio/audio.mp3")

def audio():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.05)
    global burst_triggered
    burst_triggered = True
    
# ── MediaPipe setup ─────────────────────────────────────────────────────────
BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
VisionRunningMode = mp.tasks.vision.RunningMode

latest_mask = None
mask_lock = threading.Lock()
clones = []
burst_triggered = False
burst_frame = 0   # increments every frame after burst triggered
FLASH_FADE_FRAMES = 5
STAGGER = 1        # frames between each individual clone pop

# ── Smoke system setup ─────────────────────────────────────────────
SMOKE_FOLDERS = ["smoke_1", "smoke_2", "smoke_3"]
SMOKE_FRAME_COUNT = 5
SMOKE_DURATION = 0.6  # seconds (was 600ms in JS)

# preload all smoke frames at startup — don't load from disk every spawn
smoke_assets = {}
for folder in SMOKE_FOLDERS:
    frames = []
    for i in range(1, SMOKE_FRAME_COUNT + 1):
        img = cv2.imread(f"assets/{folder}/{i}.png", cv2.IMREAD_UNCHANGED)
        frames.append(img)
    smoke_assets[folder] = frames

active_smokes = []  # list of currently playing smoke animations


def spawn_smoke(x, y, scale=1.0):
    scale *= 1.2  # same as JS
    folder = random.choice(SMOKE_FOLDERS)
    active_smokes.append({
        "x": x,
        "y": y,
        "scale": scale,
        "start": time.time(),   # replaces performance.now()
        "frames": smoke_assets[folder]  # reference preloaded frames
    })

def draw_smokes(canvas):
    now = time.time()
    frame_duration = SMOKE_DURATION / SMOKE_FRAME_COUNT  # 0.12s per frame

    for i in range(len(active_smokes) - 1, -1, -1):  # iterate backwards like JS
        s = active_smokes[i]
        elapsed = now - s["start"]
        frame_index = int(elapsed / frame_duration)

        # remove finished smoke
        if frame_index >= len(s["frames"]):
            active_smokes.pop(i)
            continue

        img = s["frames"][frame_index]
        if img is None:
            continue

        # stamp smoke onto canvas at position
        canvas = stamp_free(canvas, img, s["x"], s["y"], scale=s["scale"])

    return canvas

def result_callback(result, output_image, timestamp_ms):
    global latest_mask
    if result.category_mask is not None:
        raw = np.squeeze(result.category_mask.numpy_view()).copy()
        with mask_lock:
            latest_mask = raw

options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path="selfie_multiclass_256x256.tflite"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    output_category_mask=True,
    result_callback=result_callback
)

cap = cv2.VideoCapture(0)
smoothed_mask = None
bg = cv2.imread("bg.jpg")
   


# ── Helper: build cutout with outline ────────────────────────────────────────
def build_cutout_with_outline(frame, alpha):
    alpha_8u = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(alpha_8u, kernel, iterations=1)
    outline = cv2.subtract(dilated, alpha_8u)

    result = frame.copy()
    result[outline > 50] = [0, 255, 255]  # yellow outline

    r, g, b = cv2.split(result)
    combined_alpha = np.add(alpha_8u, outline)
    combined_alpha = np.clip(combined_alpha, 0, 255)
    return cv2.merge([r, g, b, combined_alpha])

# ── Helper: stamp cutout onto canvas ───────────────────────────────────────
def stamp_free(canvas, cutout_rgba, x_center, y_bottom, scale=0.5, flash=0.0):
    ch, cw = canvas.shape[:2]
    ph, pw = cutout_rgba.shape[:2]

    new_w = int(pw * scale)
    new_h = int(ph * scale)
    resized = cv2.resize(cutout_rgba, (new_w, new_h))

    x1 = int(x_center - new_w // 2)
    y1 = int(y_bottom - new_h)

    if x1 < 0:
        resized = resized[:, -x1:]
        x1 = 0
    if y1 < 0:
        resized = resized[-y1:, :]
        y1 = 0

    x2 = min(x1 + resized.shape[1], cw)
    y2 = min(y1 + resized.shape[0], ch)
    patch = resized[:y2 - y1, :x2 - x1]

    # ── flash must happen BEFORE blending ──
    if flash > 0:
        white = np.ones_like(patch[:, :, :3], dtype=np.float32) * 255
        patch_rgb = patch[:, :, :3].astype(np.float32)
        patch_rgb = patch_rgb * (1 - flash) + white * flash
        patch = np.dstack([patch_rgb.astype(np.uint8), patch[:, :, 3]])

    # ── now blend the (possibly flashed) patch onto canvas ──
    a = patch[:, :, 3:4].astype(np.float32) / 255.0
    roi = canvas[y1:y2, x1:x2].astype(np.float32)
    blended = roi * (1 - a) + patch[:, :, :3].astype(np.float32) * a
    canvas[y1:y2, x1:x2] = blended.astype(np.uint8)

    return canvas

# ── Main loop ─────────────────────────────────────────────────────────────
with ImageSegmenter.create_from_options(options) as segmenter:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # at the very start of the while True loop
        # global current_wave, wave_timer  # ← won't hurt now, saves you later

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # send frame to segmenter
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        segmenter.segment_async(mp_image, timestamp_ms)

        # get latest mask
        with mask_lock:
            current_mask = latest_mask.copy() if latest_mask is not None else None

        if current_mask is not None:
            # ── mask processing ─────────
            mask_f = (current_mask > 0).astype(np.float32)
            if smoothed_mask is None:
                smoothed_mask = mask_f
            else:
                smoothed_mask = 0.8 * smoothed_mask + 0.2 * mask_f

            resized_mask = cv2.resize(smoothed_mask, (w, h))
            alpha = cv2.GaussianBlur(resized_mask, (21, 21), 0)
            alpha = np.clip(alpha, 0, 1)

            # ── build cutout ───────────
            cutout = build_cutout_with_outline(frame, alpha)

            # ── handle burst clones ────
            if burst_triggered:
                clones.clear()
                burst_frame = 0    # reset counter on each burst


                front_steps = [-2, -1, 1, 2]
                back_steps  = [-3, -2, -1, 0, 1, 2, 3]
                far_steps   = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

                front_spacing = int(w * 0.12)
                back_spacing  = int(w * 0.12)
                far_spacing   = int(w * 0.12)

                # front row — pops first
                for i, step in enumerate(front_steps):
                    clones.append({
                        "x": w//2 + step * front_spacing,
                        "y": h,
                        "scale": 0.92,
                        "row": 1,
                         "smoke_spawned": False,
                        "appear_at_frame": i * STAGGER
                    })

                # back row — starts after front row finishes
                front_done_at = len(front_steps) * STAGGER
                for i, step in enumerate(back_steps):
                    clones.append({
                        "x": w//2 + step * back_spacing,
                        "y": h - int(h * 0.30),
                        "scale": 0.78,
                        "row": 2,
                         "smoke_spawned": False,
                        "appear_at_frame": front_done_at + i * STAGGER
                    })

                # far row — starts after back row finishes
                back_done_at = front_done_at + len(back_steps) * STAGGER
                for i, step in enumerate(far_steps):
                    clones.append({
                        "x": w//2 + step * far_spacing,
                        "y": h - int(h * 0.55),
                        "scale": 0.62,
                        "row": 3,
                         "smoke_spawned": False,
                        "appear_at_frame": back_done_at + i * STAGGER
                    })

                burst_triggered = False
                
            # advance waves over time
            if clones:
                last_frame_needed = max(c["appear_at_frame"] for c in clones)
                if burst_frame <= last_frame_needed + FLASH_FADE_FRAMES:
                    burst_frame += 1    

            # ── render clones ──────────
            # ── render clones ──────────
            canvas = cv2.resize(bg, (w, h))

            # render back-to-front — highest row number first
            for clone in sorted(clones, key=lambda c: c["row"], reverse=True):
                if burst_frame >= clone["appear_at_frame"]:

                    # 💨 spawn smoke ONLY ONCE
                    if not clone["smoke_spawned"]:
                        clone["smoke_spawned"] = True
                        threading.Thread(target=pop_sound.play, daemon=True).start()

                        cx = clone["x"]
                        cy = clone["y"] - int(60 * clone["scale"])

                        # left & right puff (same as JS)
                        spawn_smoke(cx - 15 + random.randint(-5, 5), cy, clone["scale"])
                        spawn_smoke(cx + 15 + random.randint(-5, 5), cy, clone["scale"])

                    # normal rendering
                    age = burst_frame - clone["appear_at_frame"]
                    flash = max(0.0, 1.0 - age / 5)

                    canvas = stamp_free(
                        canvas,
                        cutout,
                        clone["x"],
                        clone["y"],
                        clone["scale"],
                        flash
                    )

            canvas = stamp_free(canvas, cutout, w // 2, h, scale=1.0)

            # 💨 DRAW SMOKE HERE
            canvas = draw_smokes(canvas)

            output = canvas

        else:
            output = frame

        cv2.imshow("Shadow Clone Jutsu", output)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('b'):
            threading.Thread(target=audio, daemon=True).start()
        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()