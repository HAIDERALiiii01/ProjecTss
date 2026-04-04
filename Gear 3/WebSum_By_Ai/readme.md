# 🌐 WebSum By AI

<p align="center">
  <img src="https://media1.tenor.com/m/r8kuogzc3wIAAAAC/chill-oh-ya.gif" alt="WebSum By AI" width="800"/>
</p>

> Paste a URL. Get a clean AI-written summary. No fluff. 📝

---

## 🎯 What it does

A two-part web summarizer. Selenium scrapes the full text content of any website — including JavaScript-rendered pages — saves it to a file, then GPT-4o-mini reads it and returns a clean, formatted summary. Works on sites that block basic `requests` scraping.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to summarize a website |
| `selenium_scrape.py` | Scrapes any URL using Selenium and saves content to `data.txt` |
| `data.txt` | Scraped page content — auto-overwritten on each run |
| `.env` | Stores your OpenAI API key — create this yourself |

---

## ⚙️ How it works

1. **Scrape** — Selenium opens the URL in a headless Chrome browser and waits for the page to fully load
2. **Save** — The page title and full body text are saved to `data.txt`
3. **Summarize** — GPT-4o-mini reads `data.txt` and generates a clean formatted summary
4. **Output** — The summary is printed directly to the terminal

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 2/WebSum_By_Ai"
```

### 2. Install dependencies
```bash
pip install openai selenium webdriver-manager python-dotenv
```

### 3. Set up your API key

Create a `.env` file in the same directory:
```
OPENAI_API_KEY=your_openai_key_here
```

> Get your key from: https://platform.openai.com/api-keys

### 4. Run the summarizer

Open `main.py` and replace the URL at the bottom:
```python
print(summarize("https://your-target-website.com"))
```

Then run:
```bash
python main.py
```

---

## 📦 Requirements
```bash
pip install openai selenium webdriver-manager python-dotenv
```

---

## 📝 Notes

- Uses Selenium instead of `requests` — works on JavaScript-heavy sites that block basic scrapers
- ChromeDriver is installed automatically via `webdriver-manager`
- `data.txt` is overwritten on every run — save it manually if you need to keep it
- Navigation-related text is ignored by the AI during summarization
- If the page includes news or announcements, those are summarized separately

---

*"Too long. Didn't read. Asked AI instead."*
