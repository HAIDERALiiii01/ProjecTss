# 🃏 Blackjack

<p align="center">
  <img src="https://media1.tenor.com/m/r_esBp32ZF0AAAAC/garth-marenghi-darkplace.gif" alt="Blackjack" width="800"/>
</p>

> Hit or stand. Beat the dealer. Don't go over 21. 🎰

---

## 🎯 What it does

A fully playable terminal-based Blackjack game against the computer. Cards are dealt randomly, scores are calculated automatically, and the computer plays by real Blackjack rules — hitting until it reaches 17 or above. Get 21 with two cards and you've got a Blackjack. Go over and you're done.

---

## 📁 Files

| File | Description |
| --- | --- |
| `blackjack.py` | 🚀 The entire game — run this to play |

---

## ⚙️ How it works

1. **Deal** — Both you and the computer receive 2 cards each
2. **Your Turn** — Choose to hit (`y`) or stand (`n`) each round
3. **Computer's Turn** — The computer keeps hitting until its score reaches 17 or more
4. **Result** — Scores are compared and the winner is declared

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Blackjack"
```

### 2. Run the game
```bash
python blackjack.py
```

No dependencies. No setup. Just Python. 🐍

---

## 🎮 Gameplay

- Type `y` to get another card
- Type `n` to stand and let the computer play
- Score of **0** means **Blackjack** (21 with exactly 2 cards)
- Going **over 21** means you bust — instant loss
- Ace (`11`) auto-converts to `1` if you'd go over 21
- Computer always hits below 17, stands at 17 or above

---

## 📝 Notes

- No external libraries required — pure Python
- The game loops — after each round it asks if you want to play again
- Card values follow standard Blackjack: face cards count as 10, Ace as 11 (or 1)

---

*"The house always wins — unless you're the one coding it. 😏"*
