# ☕ Coffee Machine (OOPs)

<p align="center">
  <img src="https://media1.tenor.com/m/K2k9DhGwfzUAAAAd/chai-piyo-biscuit-khao-i-want-to-eat-biscuits.gif" alt="Coffee Machine" width="800"/>
</p>

> Insert notes. Pick your poison. Enjoy your brew. ☕

---

## 🎯 What it does

A fully functional terminal-based coffee machine simulator built with Object-Oriented Programming. Choose your drink, insert cash in Pakistani rupees, get your change, and the machine even plays a sound when serving. Tracks ingredients and earnings — shuts down when stock runs out.

---

## 📁 Files

| File | Description |
| --- | --- |
| `CoFfEe_MaChInE(OOPs).py` | 🚀 Entry point — run this to start the machine |
| `art.py` | ASCII art for the coffee machine display and coffee cup |
| `chai.mpeg` | Sound effect played when serving or exiting |

---

## ⚙️ How it works

1. **Menu** — Choose from espresso, latte, or cappuccino
2. **Payment** — Insert rupee notes (1000, 500, 100, 50) until the cost is covered
3. **Change** — Excess amount is returned as change
4. **Serve** — Coffee art is displayed, sound plays, drink is served
5. **Stock Tracking** — Ingredients are deducted after every order
6. **Report** — Press 4 to see remaining ingredients and total earnings
7. **Shutdown** — Machine stops automatically when any ingredient runs too low

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Coffee_Maker"
```

### 2. Install dependencies
```bash
pip install pygame
```

### 3. Run the machine
```bash
python "CoFfEe_MaChInE(OOPs).py"
```

---

## 🎮 Menu

| Option | Drink | Cost |
| --- | --- | --- |
| 1️⃣ | Espresso | 400 PKR |
| 2️⃣ | Latte | 800 PKR |
| 3️⃣ | Cappuccino | 1000 PKR |
| 4️⃣ | Report | — |
| 5️⃣ | Exit | — |

---

## 📦 Requirements
```bash
pip install pygame
```

---

## 📝 Notes

- Payment is done by inserting individual notes — enter `0` for a denomination you don't want to use
- The machine shuts down automatically when water, milk, or coffee stock drops below minimum levels
- `art.py` must be in the same directory as the main file
- `chai.mpeg` must be in the same directory for sound to work

---

*"Chai peeoo or biscuit khao. ☕"*
