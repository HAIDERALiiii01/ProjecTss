# 🔑 Password Manager

<p align="center">
  <img src="https://media1.tenor.com/m/bBJcK7rU8FwAAAAC/spider-man-whats-your-password.gif" alt="Password Manager" width="800"/>
</p>

> Generate it. Save it. Find it. Never forget a password again. 🛡️

---

## 🎯 What it does

A GUI-based password manager built with Tkinter. Generate strong random passwords, save them against a website and email, and search them up later — all stored locally in a JSON file. Generated passwords are auto-copied to your clipboard.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to open the app |
| `logo.png` | App logo displayed in the UI |
| `data.json` | Auto-created file where all passwords are stored |
| `Data.txt` | Manual backup or notes file |

---

## ⚙️ How it works

1. **Generate** — Click `Generate Password` to create a strong random password — it's auto-copied to clipboard
2. **Save** — Fill in website, email, and password then click `Add` — confirms before saving
3. **Search** — Enter a website name and click `Search` to retrieve saved credentials
4. **Storage** — All data is stored locally in `data.json` — nothing leaves your machine

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Password_Manager"
```

### 2. Install dependencies
```bash
pip install pyperclip
```

### 3. Run the app
```bash
python main.py
```

---

## 🎮 Features

| Button | Action |
| --- | --- |
| `Generate Password` | Creates a random strong password and copies it to clipboard |
| `Add` | Saves website, email and password to `data.json` |
| `Search` | Looks up saved credentials for a website |

---

## 📦 Requirements
```bash
pip install pyperclip
```

> `tkinter` and `json` are built into Python — no install needed.

---

## 📝 Notes

- Passwords are stored **locally** in `data.json` — keep this file safe
- Default email is pre-filled as `zoro@gmail.com` — change it in `main.py` to your own
- `logo.png` must be in the same directory as `main.py`
- Generated passwords mix letters, numbers and symbols for maximum strength

---

*"Tera password 'password123' hai na? Shame. 😔🔐"*
