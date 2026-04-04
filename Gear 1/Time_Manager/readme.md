# 🍅 Time Manager — Pomodoro Timer

<p align="center">
  <img src="https://media1.tenor.com/m/5rR5t1g9P3IAAAAC/bfcr-battle-for-champions-resort.gif" alt="Pomodoro Timer" width="800"/>
</p>

> Work. Break. Repeat. Stay productive the smart way. 🧠

---

## 🎯 What it does

A GUI-based Pomodoro timer built with Tkinter. It alternates between work sessions and breaks automatically, plays an alarm when each session ends, and tracks your completed work sessions with checkmarks. The window pops itself to the front when it's time to switch — so you never miss a break.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the timer |
| `tomato.png` | Tomato image displayed on the timer canvas |
| `alarm.mp3` | Alarm sound played at the end of each session |

---

## ⚙️ How it works

1. **Work Session** — Timer counts down for the set work duration
2. **Short Break** — After every work session, a short break begins automatically
3. **Long Break** — After every 4 work sessions (8 reps), a long break is given
4. **Alarm** — An alarm plays and the window comes to the front when a session ends
5. **Checkmarks** — Each completed work session adds a ✔ to the display
6. **Reset** — Cancels the current timer and resets everything to zero

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Time_Manager"
```

### 2. Install dependencies
```bash
pip install pygame
```

### 3. Run the timer
```bash
python main.py
```

---

## ⏱️ Default Session Lengths

| Session | Duration |
| --- | --- |
| Work | 1 minute (set to 25 for real use) |
| Short Break | 5 minutes |
| Long Break | 20 minutes |

> To adjust, change `WORK_MIN`, `SHORT_BREAK_MIN`, and `LONG_BREAK_MIN` at the top of `main.py`.

---

## 🎮 Controls

| Button | Action |
| --- | --- |
| `Start` | Begin the Pomodoro cycle |
| `Reset` | Cancel and reset the timer |

---

## 📦 Requirements
```bash
pip install pygame
```

> `tkinter` and `math` are built into Python — no install needed.

---

## 📝 Notes

- `tomato.png` and `alarm.mp3` must be in the same directory as `main.py`
- `WORK_MIN` is set to `1` for testing — change it to `25` for actual Pomodoro sessions
- The window automatically restores and jumps to the front when a session ends
- Checkmarks accumulate across the session until you hit Reset

---

*"25 minutes of focus. You can do it."*
