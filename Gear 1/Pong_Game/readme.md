# 🏓 Pong Game

<p align="center">
  <img src="https://media1.tenor.com/m/uVn99ocpKFYAAAAC/grafica-graphic.gif" alt="Pong Game" width="800"/>
</p>

> Two paddles. One ball. Infinite rivalry. 🕹️

---

## 🎯 What it does

A classic two-player Pong game built with Python Turtle. Both players control paddles on opposite sides of the screen, trying to keep the ball in play. Miss the ball and your opponent scores. Background music plays throughout the match.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the game |
| `ball.py` | Ball movement, bouncing and reset logic |
| `paddle.py` | Paddle class — movement for both players |
| `scoreboard.py` | Tracks and displays scores for both sides |
| `music.py` | Background music using pygame |
| `sss.mp3` | Background music — plays on loop |

---

## ⚙️ How it works

1. **Ball** — Moves diagonally and bounces off top and bottom walls
2. **Paddles** — Each player moves their paddle to intercept the ball
3. **Bounce** — Ball reverses horizontal direction when it hits a paddle
4. **Score** — If the ball passes a paddle and hits the edge, the other player scores
5. **Reset** — Ball resets to center after each point
6. **Music** — Background music loops throughout the game

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Pong_Game"
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

| Player | Up | Down |
| --- | --- | --- |
| Right Player | `↑` Arrow | `↓` Arrow |
| Left Player | `W` | `S` |

---

## 📦 Requirements
```bash
pip install pygame
```

> `turtle` is built into Python — no install needed.

---

## 📝 Notes

- `sss.mp3` must be in the same directory as `main.py` for music to work
- The game runs indefinitely — there is no winning condition, just bragging rights 😎
- Ball speed is fixed — commented-out code in `ball.py` can enable speed increase on each bounce if you want a challenge

---

*"Sirf ek aur point. Sirf ek aur. 😤🏓"*
