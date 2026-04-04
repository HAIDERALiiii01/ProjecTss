# 🔢 Guess The Number

<p align="center">
  <img src="https://media1.tenor.com/m/X9SGirjkxxEAAAAC/tenor.gif" alt="Guess The Number" width="800"/>
</p>

> Pick a number. The computer yells at you until you get it right. 🗣️

---

## 🎯 What it does

A terminal-based number guessing game — with a voice. The computer picks a random number between 1 and 100, and you have to guess it. Too high or too low, and it tells you (out loud). Get it right and it announces how many attempts it took.

---

## 📁 Files

| File | Description |
| --- | --- |
| `guess_the_number.py` | 🚀 The entire game — run this to play |

---

## ⚙️ How it works

1. **Introduction** — The game explains itself out loud using text-to-speech
2. **Random Number** — The computer picks a number between 1 and 100
3. **Your Guess** — You enter a number each round
4. **Feedback** — It tells you (and yells at you) whether to go higher or lower
5. **Win** — Match the number and it announces your total attempts

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Guess_The_Number"
```

### 2. Install dependencies
```bash
pip install pyttsx3
```

### 3. Run the game
```bash
python guess_the_number.py
```

---

## 🎮 Gameplay

- Guess a number between **1 and 100**
- The game tells you if you need to go **higher** or **lower**
- It also says it out loud — with attitude 😤
- Keep guessing until you match the number
- Your total attempt count is revealed at the end

---

## 📦 Requirements
```bash
pip install pyttsx3
```

---

## 📝 Notes

- Uses `pyttsx3` for offline text-to-speech — no internet required
- Voice feedback is randomized — it won't say the same thing every time
- `random` and `time` are built into Python — no install needed

---

*"Bhai higher bola tha — HIGHER. 😤"*
