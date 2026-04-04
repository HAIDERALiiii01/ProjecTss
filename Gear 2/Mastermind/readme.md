# 🧠 Mastermind

<p align="center">
  <img src="https://media1.tenor.com/m/oJKQsEPQrYIAAAAC/spongebob-spongebob-squarepants.gif" alt="Mastermind" width="800"/>
</p>

> Crack the color code before your attempts run out. 🎨

---

## 🎯 What it does

A terminal-based Mastermind code-breaking game. The computer generates a secret sequence of 5 colors and you have 10 attempts to guess it correctly. After each guess, it tells you how many positions are correct — use that info to crack the code.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 The entire game — run this to play |
| `rough.py` | Scratch file used for testing — not required to run the game |

---

## ⚙️ How it works

1. **Secret Code** — The computer randomly generates a sequence of 5 colors
2. **Your Guess** — Enter 5 color codes separated by spaces
3. **Feedback** — The number of correctly positioned colors is revealed
4. **Win** — Match all 5 positions exactly to win
5. **Lose** — Run out of 10 attempts and the correct answer is revealed

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Mastermind"
```

### 2. Run the game
```bash
python main.py
```

No dependencies. No setup. Just Python. 🐍

---

## 🎮 How to play

- Colors available: `R` (Red), `Y` (Yellow), `G` (Green)
- Enter exactly 5 colors separated by spaces like this:
```
R Y G G Y
```

- The game tells you how many positions are correct after each guess
- Figure out the full sequence within 10 attempts to win

---

## 📝 Notes

- No external libraries required — pure Python
- Input is space-separated — entering without spaces will be rejected
- Colors can repeat in the secret code

---

*"Logic over luck. Every time."*
