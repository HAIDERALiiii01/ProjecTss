# 🐍 Snake Game

<p align="center">
  <img src="https://media1.tenor.com/m/FOJj9aijZYgAAAAC/snake-nokia-3310-snake.gif" alt="Snake Game" width="800"/>
</p>

> Eat. Grow. Don't hit yourself. Classic. 🐍

---

## 🎯 What it does

A fully functional Snake game built with Python Turtle. Eat the food to grow longer and rack up points. Hit a wall or your own tail and the snake resets — but your high score is saved to a file and persists between sessions. Background music plays throughout.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the game |
| `snake.py` | Snake body, movement, extension and reset logic |
| `food.py` | Food spawning at random positions |
| `scoreboard.py` | Tracks current score and all-time high score |
| `music.py` | Background music and game over sound using pygame |
| `main_music.mp3` | Background music — plays on loop |
| `game_over.mp3` | Sound effect played on death |
| `high_score.txt` | Stores the all-time high score between sessions |

---

## ⚙️ How it works

1. **Movement** — Snake moves continuously, controlled by arrow keys
2. **Food** — Eating food grows the snake and increases the score by 1
3. **Collision** — Hitting a wall or the snake's own body resets the snake
4. **High Score** — If your score beats the record, it is saved to `high_score.txt` automatically
5. **Music** — Background music loops throughout the session

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Snake_Game"
```

### 2. Install dependencies
```bash
pip install pygame
```

### 3. Run the game
```bash
python main.py
```

---

## 🎮 Controls

| Key | Action |
| --- | --- |
| `↑` Arrow | Move up |
| `↓` Arrow | Move down |
| `←` Arrow | Move left |
| `→` Arrow | Move right |

---

## 📦 Requirements
```bash
pip install pygame
```

> `turtle` is built into Python — no install needed.

---

## 📝 Notes

- High score persists between sessions via `high_score.txt` — don't delete it
- All `.mp3` files must be in the same directory as `main.py`
- The game never truly ends — the snake resets on collision and you keep playing
- Game over sound is implemented but currently commented out in `main.py` — uncomment to enable it

---

*"One more run. Just one more."*
