---
type: project
name: Shadow Clone Jutsu
aliases: [Shadow_Clone_Jujutsu, Shadow_Clone_jutsu]
topics: [computer-vision, gesture-recognition, real-time, mediapipe, tflite]
stack: Python, OpenCV, MediaPipe, TensorFlow, TensorFlow Lite, Scikit-learn, NumPy, Pandas
---

# Shadow Clone Jutsu: Real-Time Hand Gesture Recognition

## What Shadow Clone Jutsu is and why I built it

Shadow Clone Jutsu is a real-time computer vision project I built, inspired by Naruto. The repository folder is named Shadow_Clone_Jujutsu. It uses a webcam to detect my hand gestures live. When I perform the correct hand sign, a smoke effect appears and shadow clones of me are rendered on screen, with audio effects triggered at the same moment.

The hand sign that triggers the effect is the Shadow Clone Jutsu hand seal from the Naruto anime, which is where the idea came from.

I built the gesture recognition with a custom-trained machine learning model together with MediaPipe for hand tracking.

## How the Shadow Clone Jutsu pipeline works

In Shadow Clone Jutsu, the application processes the live webcam feed and does three main things: it detects and tracks hand landmarks, recognizes the hand gesture, and segments the person from the background so the clone effect can be rendered.

The gesture pipeline is: webcam, then hand detection, then hand landmarks, then feature scaling, then gesture recognition, then the clone effect. A separate segmentation pipeline runs alongside it: webcam frame, then person segmentation, then person mask, then visual effect. For every frame, the app runs these steps, checks whether the correct sign was performed, and triggers the effects immediately when it was.

## Hand detection with MediaPipe

In Shadow Clone Jutsu, I use MediaPipe's hand landmark model to detect my hand and extract its landmarks. The landmark coordinates are the features that the gesture recognition model uses.

## The gesture recognition model

In Shadow Clone Jutsu, I trained a custom classifier to recognize the hand signs. It runs as a TensorFlow Lite model on MediaPipe hand landmarks. Before the landmarks reach the model, they are scaled with a saved feature scaler, and the gesture class labels are stored in a saved label encoder. The model outputs a gesture class, which decides whether the required hand sign has been performed.

## The dataset and training

In Shadow Clone Jutsu, I collected and labeled the gesture dataset myself, about 2,000 samples. I built a recording tool that captures hand landmark data for each gesture and saves it to a CSV file. I then trained the model on that data, including feature scaling, and saved the scaler so the same transformation is applied during real-time recognition. The trained model is exported as TensorFlow Lite for the live application.

The system is extensible. To add a new hand sign, I record new landmark data with the recording tool, add the label, and retrain on the updated dataset. Retraining is only needed for new gestures or an updated dataset, since the trained model is already included.

## Person segmentation

In Shadow Clone Jutsu, I use a TensorFlow Lite selfie segmentation model (`selfie_multiclass_256x256`) to separate the person from the webcam background. Isolating the person lets the app apply the visual effect to them and not to the whole frame.

## The shadow clone effect

In Shadow Clone Jutsu, when the correct hand sign is detected, the app plays smoke assets and renders the shadow clones on screen. The effect combines the live camera feed, the person segmentation mask, the smoke assets, and the clone rendering, with audio triggered at the same time.

## How the live recognition works in Shadow Clone Jutsu

In Shadow Clone Jutsu, for each hand I turn the 21 MediaPipe landmarks into 91 features: positions normalized by the size of the hand and relative to the wrist, a projection along the hand's direction so it still works when the hand is rotated, distances between fingertips, and a few finger angles. For two hands that makes 182 features, and a missing hand is filled with zeros.

The features are scaled and passed to the classifier, which runs on every second frame. To keep the result stable, I only accept a prediction when its confidence is at least 80%, and I smooth the output with a majority vote over the last 6 predictions, so the detected sign only changes when at least 3 of them agree. The Shadow Clone Jutsu sign also requires both hands to be visible before it counts. MediaPipe hand detection runs with a confidence threshold of 0.7.

I tested the system live with my webcam. While running, the model's confidence for the sign was typically around 80 to 90%.

## The hardest part of building Shadow Clone Jutsu

The hardest part of Shadow Clone Jutsu was collecting the dataset. The model itself was manageable, but there was no ready-made dataset for this hand sign, so I had to record and label all the gesture data myself with my own recording tool.

## Technologies used in Shadow Clone Jutsu

- Computer vision: OpenCV, MediaPipe, TensorFlow Lite
- Machine learning: TensorFlow, Scikit-learn, a custom gesture classifier, feature scaling
- Data processing: NumPy, Pandas
- Models: MediaPipe hand landmark model, custom TFLite gesture model, TFLite person segmentation model

## Links to Shadow Clone Jutsu

- Shadow Clone Jutsu GitHub: https://github.com/HAIDERALiiii01/ProjecTss/tree/main/Gear%204/Shadow_Clone_Jujutsu
- Shadow Clone Jutsu demo: https://lnkd.in/p/dWCsmPjB
