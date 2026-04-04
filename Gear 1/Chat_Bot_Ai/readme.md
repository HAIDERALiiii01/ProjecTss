# 🤖 WhatsApp AI Chatbot

<p align="center">
  <img src="https://media1.tenor.com/m/a6S35wgiCOsAAAAC/deku-java.gif" alt="Chatbot" width="800"/>
</p>

> Reads your WhatsApp. Replies like you. Nobody suspects a thing. 🥷

---

## 🎯 What it does

An AI-powered WhatsApp automation bot that reads your chat history and replies on your behalf using Google Gemini. It mimics a 19-year-old from Karachi — sarcastic, funny, anime-loving, Roman Urdu typing — so naturally that no one can tell it's an AI.

---

## 📁 Files

| File | Description |
| --- | --- |
| `chat-bot-ai.py` | 🚀 The entire bot — run this to start automating |

---

## ⚙️ How it works

1. **Launch** — Opens WhatsApp via Windows search using `pyautogui`
2. **Navigate** — Searches for the target chat and opens it
3. **Read** — Copies the chat history from the screen to clipboard
4. **Generate** — Sends the chat history to Gemini AI with a custom personality prompt
5. **Reply** — Pastes and sends the AI-generated response directly into the chat

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Chatbot"
```

### 2. Install dependencies
```bash
pip install pyautogui pyperclip google-generativeai
```

### 3. Add your Gemini API key

Open `chat-bot-ai.py` and replace the placeholder:
```python
GEMINI_API_KEY = "your Gemini api key here"
```

> Get a free API key from: https://aistudio.google.com/app/apikey

### 4. Run the bot
```bash
python chat-bot-ai.py
```

Enter the WhatsApp contact name when prompted and let it do the rest.

---

## 🎭 Personality

The bot is prompted to act as a 19-year-old from Karachi who:

- Replies in short, casual **Roman Urdu**
- Is a fan of **One Piece, Marvel, and animated movies**
- Loves **football, memes, and background scores**
- Is **sarcastic and funny** without being harsh
- Is a **Taarak Mehta ka Oolta Chasma** enjoyer 😭
- Is currently **learning programming**

---

## 📦 Requirements
```
pyautogui
pyperclip
google-generativeai
```

---

## 📝 Notes

- Designed for **Windows** — uses `Win + S` to open search
- Screen coordinates for clicking are hardcoded — adjust `x` and `y` values in the script if your screen resolution differs
- WhatsApp must be installed as a desktop app
- Make sure WhatsApp is not minimized before running

---

*"Tera reply aya — but it wasn't really you. 😶‍🌫️"*
