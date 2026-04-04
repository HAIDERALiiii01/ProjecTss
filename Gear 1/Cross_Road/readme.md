# 🐢 Cross Road

<p align="center">
  <img src="https://media1.tenor.com/m/2Sjak6gDwUgAAAAC/flailing-fish-crossing-road.gif" alt="Cross Road" width="800"/>
</p>

> Cross the road. Dodge the cars. Don't get hit. 🚗💨

---

## 🎯 What it does

A Frogger-style arcade game built with Python Turtle. Guide your turtle across a busy road full of speeding cars. Each time you reach the other side, the level increases and the cars get faster. Get hit once and it's game over.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the game |
| `player.py` | Controls the turtle player — movement and finish line detection |
| `car_manager.py` | Spawns and moves cars, handles level speed increases |
| `scoreboard.py` | Displays current level and game over screen |
| `music.py` | Background music and sound effects using pygame |
| `main.mp3` | Background music — plays on loop |
| `game_over.mp3` | Sound effect played when you get hit |
| `level_up.mp3` | Sound effect played when you reach the finish line |

---

## ⚙️ How it works

1. **Player** — A turtle starts at the bottom of the screen, moves up with the `Up` arrow key
2. **Cars** — Randomly colored cars spawn from the right and move left at increasing speeds
3. **Collision** — If a car gets within 20 pixels of the turtle, game over
4. **Level Up** — Reaching the top sends the turtle back to start and increases car speed
5. **Score** — Current level is displayed on screen throughout the game
6. **Sound** — Background music plays on loop, with separate sounds for level up and game over

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Cross_Road"
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
| `↑` Arrow | Move turtle up |

---

## 📦 Requirements
```bash
pip install pygame
```

---

## 📝 Notes

- `turtle` is built into Python — no install needed
- All `.mp3` files must be in the same directory as `main.py`
- Cars spawn randomly — 1 in 6 chance each game tick
- Every time you cross, car speed increases by 10 units — it gets brutal fast 😅

---

*"Just one more cross. Just one more. I swear. 😤"*
