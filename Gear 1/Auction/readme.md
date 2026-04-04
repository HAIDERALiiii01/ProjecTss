# 🔨 Auction House

<p align="center">
  <img src="https://media1.tenor.com/m/9xBOcrRY8X8AAAAC/sold-auction.gif" alt="Auction" width="800"/>
</p>

> Place your bids. Clear the screen. May the highest offer win. 💰

---

## 🎯 What it does

A terminal-based blind auction program. Each bidder enters their name and bid privately — the screen clears between turns so no one sees anyone else's offer. Once all bids are in, the highest bidder is revealed.

---

## 📁 Files

| File | Description |
| --- | --- |
| `auction.py` | 🚀 The entire auction — run this to start bidding |

---

## ⚙️ How it works

1. **Bidding Round** — Each player enters their name and bid amount
2. **Screen Clear** — 100 blank lines flush the terminal so the next bidder sees nothing
3. **Repeat** — Continues until no more bidders remain
4. **Winner** — The highest bid is calculated and the winner is announced

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Auction"
```

### 2. Run the program
```bash
python auction.py
```

No dependencies. No setup. Just Python. 🐍

---

## 🎮 How to play

- Each player enters their name and bid one at a time
- After each bid, type `y` if more people want to bid — the screen will clear
- Type `n` when everyone has placed their bid
- The winner with the highest bid is announced at the end

---

## 📝 Notes

- No external libraries required — pure Python
- Bids are kept secret — the screen clears between each player's turn
- All bids are stored in memory and compared at the end
- Bid amounts must be whole numbers

---

*"Going once. Going twice. Sold. 🔨"*
