# 🎯 Aim Trainer

<p align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdwM2VqOWcwcW5kNnFnOWhoZnF6ZXkzbHJ1Mnc1ODZkbWpuNGR4aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JCD1jbu3UgBby/giphy.gif" alt="Aim Trainer" width="800"/>
</p>

> Click the targets. Don't miss. Train your aim. 🖱️

---

## 🎯 What it does

A fast-paced aim training game built with Pygame. Targets appear randomly on screen, grow to full size and shrink back — click them before they disappear. You have 50 lives. Miss too many and the game ends, showing your full performance stats.

---

## 📁 Files

| File | Description |
| --- | --- |
| `trainer.py` | 🚀 The entire game — run this to start training |

---

## ⚙️ How it works

1. **Targets** — Circular targets spawn randomly every 400ms, grow and then shrink
2. **Click** — Hit a target before it fully shrinks to score a hit
3. **Miss** — If a target disappears without being clicked, you lose a life
4. **Lives** — You start with 50 lives — run out and the game ends
5. **Stats** — End screen shows time, speed, hits and accuracy

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Aim_Trainer"
```

### 2. Install dependencies
```bash
pip install pygame
```

### 3. Run the game
```bash
python trainer.py
```

---

## 📊 Stats Tracked

| Stat | Description |
| --- | --- |
| Time | Total time elapsed |
| Speed | Targets hit per second |
| Hits | Total successful clicks |
| Accuracy | Percentage of clicks that landed |

---

## 📦 Requirements
```bash
pip install pygame
```

---

## 📝 Notes

- Targets spawn every **400ms** — adjust `TARGET_INCREMENT` in the script to change difficulty
- Lives are set to **50** — change `LIVES` at the top of the script to make it harder or easier
- Press any key on the end screen to quit
- Runs at a locked **60 FPS**

---

*"Aim. Click. Repeat. No excuses."*
