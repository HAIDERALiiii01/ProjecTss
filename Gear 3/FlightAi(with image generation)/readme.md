# ✈️ FlightAI — With Image Generation

<p align="center">
  <img src="https://media1.tenor.com/m/ns_8Rmp-9O4AAAAd/o9iw-mr-bean-meme.gif" width="600"/>
</p>

> Ask about flights. Get the price. See your destination come to life. 🎨

---

## 🎯 What it does

An AI-powered airline chatbot built with GPT-4o-mini and DALL-E 3. Ask about ticket prices to any supported city and the assistant responds with the price — then instantly generates a vibrant pop-art image of that destination. All inside a clean Gradio interface.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to launch the chatbot |
| `.env` | Stores your OpenAI API key — create this yourself |

---

## ⚙️ How it works

1. **Chat** — You ask the assistant about ticket prices or anything flight-related
2. **Tool Call** — When a destination is detected, GPT calls the `get_ticket_price` tool
3. **Price** — The ticket price is looked up and returned to the model
4. **Image** — DALL-E 3 generates a vibrant pop-art image of the destination city
5. **Response** — The assistant replies with the price and the image appears side by side

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 2/FlightAI"
```

### 2. Install dependencies
```bash
pip install openai gradio pillow python-dotenv
```

### 3. Set up your API key

Create a `.env` file in the same directory:
```
OPENAI_API_KEY=your_openai_key_here
```

> Get your key from: https://platform.openai.com/api-keys

### 4. Run the app
```bash
python main.py
```

The Gradio interface opens in your browser automatically.

---

## 🌍 Supported Destinations

| City | Price |
| --- | --- |
| Tokyo | $800 |
| New York | $600 |
| London | $500 |
| Paris | $450 |

> More cities can be added by updating the `ticket_prices` dictionary in `main.py`.

---

## 📦 Requirements
```bash
pip install openai gradio pillow python-dotenv
```

---

## 📝 Notes

- DALL-E 3 image generation costs credits — each image query uses your OpenAI balance
- The chatbot keeps full conversation history within a session
- Click `Clear` to reset the chat and start fresh
- Unknown destinations return `"unknown"` as the price — extend the dictionary to add more cities

---

*"Where do you want to go today?"*
