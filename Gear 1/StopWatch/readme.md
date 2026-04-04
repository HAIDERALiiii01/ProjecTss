# ⏱️ Stopwatch

<p align="center">
  <img src="https://media1.tenor.com/m/5rR5t1g9P3IAAAAC/bfcr-battle-for-champions-resort.gif" alt="Stopwatch" width="800"/>
</p>

> Start. Stop. Reset. Simple as that. ⏱️

---

## 🎯 What it does

A clean GUI stopwatch built with PyQt5. Displays time in hours, minutes, seconds and milliseconds with a large digital-style display. Three buttons — Start, Stop and Reset — give you full control.

---

## 📁 Files

| File | Description |
| --- | --- |
| `WATCH_STOP.py` | 🚀 Entry point — run this to open the stopwatch |
| `DS-DIGI.TTF` | Digital display font — regular |
| `DS-DIGIB.TTF` | Digital display font — bold |
| `DS-DIGII.TTF` | Digital display font — italic |
| `DS-DIGIT.TTF` | Digital display font — alternate style |

---

## ⚙️ How it works

1. **Start** — Begins the timer, updating every 10 milliseconds
2. **Stop** — Pauses the timer at the current time
3. **Reset** — Stops and resets the display back to `00:00:00.00`
4. **Display** — Shows time in `HH:MM:SS.ms` format on a large purple label

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/StopWatch"
```

### 2. Install dependencies
```bash
pip install PyQt5
```

### 3. Run the stopwatch
```bash
python WATCH_STOP.py
```

---

## 🎮 Controls

| Button | Action |
| --- | --- |
| `START` | Begin timing |
| `STOP` | Pause the timer |
| `RESET` | Stop and reset to zero |

---

## 📦 Requirements
```bash
pip install PyQt5
```

---

## 📝 Notes

- Timer updates every **10 milliseconds** for smooth precision display
- All `.TTF` font files must be in the same directory as `WATCH_STOP.py`
- The stopwatch can be paused and resumed without resetting
- Built entirely with PyQt5 — no browser or internet required

---

*"Time waits for no one. But this stopwatch will."*
