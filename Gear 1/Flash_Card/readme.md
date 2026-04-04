# 🃏 Flash Card

<p align="center">
  <img src="https://media1.tenor.com/m/loEwTgRJ1Q4AAAAC/lula-nao-no.gif" alt="Flash Card" width="800"/>
</p>

> Flip the card. Know the word. Build your vocabulary. 🧠

---

## 🎯 What it does

A GUI-based flashcard app for learning Japanese (and French) vocabulary. Each card shows a Japanese word for 3 seconds, then flips to reveal the English translation. Mark it right or wrong, and your score is shown at the end.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to start the app |
| `data/japanese_words.csv` | Japanese to English word pairs |
| `data/french_words.csv` | French to English word pairs |
| `images/card_front.png` | Front face of the flashcard |
| `images/card_back.png` | Back face of the flashcard (flipped) |
| `images/right.png` | ✅ Right answer button image |
| `images/wrong.png` | ❌ Wrong answer button image |

---

## ⚙️ How it works

1. **Card Appears** — A Japanese word is shown on the front of the card
2. **Auto Flip** — After 3 seconds, the card flips to show the English translation
3. **You Decide** — Click ✅ if you knew it, ❌ if you didn't
4. **Next Card** — Moves to the next word automatically
5. **Final Score** — After all cards, your score is displayed on screen

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Flash_Card"
```

### 2. Install dependencies
```bash
pip install pandas
```

### 3. Run the app
```bash
python main.py
```

---

## 🌍 Switching Language

The app currently loads `japanese_words.csv` by default. To switch to French, update this line in `main.py`:
```python
data = pandas.read_csv(r"data\french_words.csv")
```

And update the title text from `"Japanese"` to `"French"` accordingly.

---

## 📦 Requirements
```bash
pip install pandas
```

> `tkinter` is built into Python — no install needed.

---

## 📝 Notes

- Buttons are **disabled** while the Japanese word is showing — you can only answer after the card flips
- The score is shown at the end once all cards are exhausted
- Both `data/` and `images/` folders must be in the same directory as `main.py`

---

*"Ek word roz — ek saal mein fluent. Theoretically. 📖"*
