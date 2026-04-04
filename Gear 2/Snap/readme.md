# 🫰 Snap — The Infinity Gauntlet

<p align="center">
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDZqMmtiYjZxaHQwZm15endna3czb3R5cmVpcjY1M3JicjBuN3pzbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT0xejJnePNcOWoHOo/giphy.gif" alt="Snap" width="800"/>
</p>

> Select a folder. Press SNAP. Half of everything is gone. Just like that. 🫰

---

## 🎯 What it does

A Thanos-inspired desktop app built with PySide6. Select any folder on your machine, hit the SNAP button, and exactly half of its contents are randomly deleted — files and folders alike — with a full cinematic snap animation, dust particle effect, and sound. This is not a joke. It actually deletes files. 

> ⚠️ **WARNING: This permanently deletes real files. Do NOT use on important folders. There is no undo.**

---

## 📁 Files

| File | Description |
| --- | --- |
| `code/main.py` | 🚀 Entry point — run this to launch the app |
| `code/algo.txt` | The 4-line algorithm behind the snap logic |
| `stuff/bg.png` | Background image for the app |
| `stuff/picture.png` | Main character image displayed in the UI |
| `stuff/snap.gif` | Snap animation played when the button is pressed |
| `stuff/sound.mp3` | Audio played during the snap |
| `stuff/1-4.png` | Random images that float around the screen |
| `stuff/font/font/font.ttf` | Custom font used for the buttons |

---

## ⚙️ How it works

1. **Select Universe** — Click `SELECT UNIVERSE` to choose a folder
2. **Images Appear** — Random images float onto the screen one by one
3. **SNAP** — Click the `SNAP!` button to trigger the event
4. **Animation** — The snap GIF plays, the sound fires, and particle dust effects scatter across screen
5. **Deletion** — Exactly half the contents of the selected folder are randomly deleted permanently
6. **Aftermath** — Half the floating images also disintegrate into dust particles

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Snap"
```

### 2. Install dependencies
```bash
pip install PySide6
```

### 3. Run the app
```bash
python code/main.py
```

---

## 📦 Requirements
```bash
pip install PySide6
```

---

## 📝 Notes

- The app launches in **fullscreen** — press `Escape` to close
- All assets inside the `stuff/` folder must stay in place relative to `main.py`
- **Do not point this at anything you care about** — deleted files do not go to Recycle Bin
- Great for cleaning up junk test folders or just living dangerously 😈

---

*"Perfectly balanced. As all things should be."*
