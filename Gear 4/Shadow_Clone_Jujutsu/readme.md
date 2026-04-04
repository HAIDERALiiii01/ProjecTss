# 🥷 Shadow Clone Jujutsu

<p align="center">
  <img src="https://media1.tenor.com/m/W4O0eoqdaREAAAAC/naruto-naruto-shippuden.gif" alt="Clone" width="800"/>
</p>

> Perform a hand sign — and your clones appear. A real-time computer vision project inspired by Naruto.

---

## 🎯 What it does

Shadow Clone Jujutsu uses your webcam to detect hand gestures in real time. When you perform the correct hand sign, a smoke effect plays and your shadow clones appear on screen — just like in the anime. Built using a custom-trained ML model and MediaPipe for hand tracking.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the program |
| `rec.py` | Record and collect hand gesture data, saves to `datasets.csv` |
| `seg.py` | Segmentation — extracts person from webcam frame |
| `training.py` | Trains the gesture recognition model using `datasets.csv` |
| `testing.py` | Tests the trained model to verify accuracy |
| `datasets.csv` | Hand gesture dataset used to train the model |
| `encoder.pkl` | Stores the gesture class labels the model recognizes |
| `scaler.pkl` | Feature scaler saved during training, used during recognition |
| `gesture_model_tflite` | The trained TFLite model for hand sign recognition |
| `hand_landmark.task` | MediaPipe task file for detecting and drawing hand landmarks |
| `selfie_multiclass_256x256.tflite` | TFLite segmentation model for extracting person from frame |
| `assets/` | Smoke effect images and audio files |
| `requirements.txt` | All dependencies |

---

## ⚙️ How it works

1. **Hand Detection** — MediaPipe detects your hand and draws landmarks on it using `hand_landmark.task`
2. **Segmentation** — `seg.py` separates you from the background using the segmentation model
3. **Gesture Recognition** — landmark coordinates are scaled using `scaler.pkl` and passed to the TFLite model
4. **Clone Effect** — when the correct sign is detected, smoke assets play and clones are rendered on screen

---

## 🚀 Getting started

### 1. Clone the repository

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 4/shadow_clone_jujutsu"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the program

```bash
python main.py
```

Make sure your webcam is connected. Perform the correct hand sign and watch the clones appear. 🥷

---

## 🎮 Recording your own gestures (optional)

If you want to train the model on your own hand signs, use `rec.py`:

```bash
python rec.py
```

- Press a specific key to record a specific gesture
- The gesture label can be changed inside the code
- Recorded data is saved to `datasets.csv`

---

## 🏋️ Training the model (optional)

The model is already trained and ready to use. But if you want to retrain it after recording new gestures:

```bash
python training.py
```

This will use `datasets.csv` to train and update the model.

---

## ✅ Testing the model (optional)

To verify that the trained model is working correctly:

```bash
python testing.py
```

---

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Key libraries used:
- `opencv-python` — webcam feed and frame processing
- `mediapipe` — hand landmark detection
- `tensorflow` / `tflite` — gesture recognition and segmentation models
- `scikit-learn` — feature scaling
- `numpy`, `pandas` — data handling

---

## 📝 Notes

- The model is already trained — you don't need to run `training.py` unless adding new gestures
- `rec.py` and `training.py` are optional tools for extending the project
- Make sure your lighting is decent for best gesture detection results

---

*"The stronger the bond, the more powerful the clone." 🍃*
