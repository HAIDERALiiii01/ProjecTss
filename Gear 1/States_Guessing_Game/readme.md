# 🗺️ States Guessing Game

<p align="center">
  <img src="https://media1.tenor.com/m/274XvFrQJV8AAAAC/kermit-map.gif" alt="States Guessing Game" width="800"/>
</p>

> Name all 50 states. Place them on the map. No cheating. 🧠

---

## 🎯 What it does

An educational geography game built with Python Turtle. A blank map of the USA is displayed and you type in state names one by one. Each correct guess places the state name exactly where it belongs on the map. Exit early and the states you missed are saved to a CSV file for review.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the game |
| `50_states.csv` | Dataset containing all 50 state names and their map coordinates |
| `blank_states_img.gif` | Blank USA map used as the game background |
| `missing_states.csv` | Auto-generated file listing states you failed to guess |

---

## ⚙️ How it works

1. **Map** — A blank USA map loads as the game screen
2. **Input** — A dialog box prompts you to type a state name each round
3. **Correct Guess** — The state name appears at its correct location on the map
4. **Score** — Tracks how many states you have correctly guessed out of 50
5. **Exit** — Type `Exit` to quit early — all missed states are saved to `missing_states.csv`

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/States_Guessing_Game"
```

### 2. Install dependencies
```bash
pip install pandas
```

### 3. Run the game
```bash
python main.py
```

---

## 🎮 How to play

- Type a US state name in the dialog box and press Enter
- Correct guesses are placed on the map at their real location
- The title bar shows your current progress (e.g. `Guess the state (12/50)`)
- Type `Exit` at any time to quit — your missed states will be saved to `missing_states.csv`
- Goal is to name all 50 states

---

## 📦 Requirements
```bash
pip install pandas
```

> `turtle` is built into Python — no install needed.

---

## 📝 Notes

- State names are case-insensitive — input is auto-formatted to title case
- `missing_states.csv` is overwritten every time you exit — use it to study and improve
- All files must be in the same directory as `main.py`
- The game ends automatically once all 50 states are correctly guessed

---

*"How many can you name without looking? Be honest."*
