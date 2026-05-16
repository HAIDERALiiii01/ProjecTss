# 📄 Brochure Generator — AI Based

<p align="center">
  <img src="https://media1.tenor.com/m/Xehj8EoUtxoAAAAC/kermit-the-frog-kermit-typing.gif" width="600"/>
</p>

> Give it a company name and URL. Get a full brochure. Powered by GPT and Gemini. 🤖

---

## 🎯 What it does

An AI-powered brochure generator with a Gradio web interface. Paste any company's website URL, choose between GPT-4o-mini or Gemini 2.0 Flash, and it scrapes the landing page, finds relevant links, reads them all, and generates a polished markdown brochure — streamed live as it writes.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to launch the Gradio interface |
| `.env` | Stores your API keys — create this yourself |

---

## ⚙️ How it works

1. **Scrape** — The `Website` class fetches and parses the company's landing page
2. **Links** — GPT scans all page links and identifies the most relevant ones (About, Careers etc.)
3. **Collect** — Content from the landing page and all relevant links is gathered
4. **Generate** — The selected model (GPT or Gemini) writes a brochure in markdown
5. **Stream** — Output is streamed live token by token into the Gradio interface

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 2/Brochure_Generator"
```

### 2. Install dependencies
```bash
pip install openai google-generativeai gradio beautifulsoup4 requests python-dotenv
```

### 3. Set up API keys

Create a `.env` file in the same directory:
```
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

> Get your OpenAI key from: https://platform.openai.com/api-keys
> Get your Gemini key from: https://aistudio.google.com/app/apikey

### 4. Run the app
```bash
python main.py
```

A local Gradio interface will open in your browser automatically.

---

## 🎮 How to use

- Enter the **company name** in the first field
- Paste the **full URL** including `https://`
- Select **GPT** or **GEMINI** from the dropdown
- Watch the brochure generate live in the output panel

---

## 📦 Requirements
```bash
pip install openai google-generativeai gradio beautifulsoup4 requests python-dotenv
```

---

## 📝 Notes

- Both API keys are required even if you only use one model — remove the unused one from the code if needed
- Some websites block scraping — results may vary depending on the target site
- GPT handles link filtering for both models — an OpenAI key is always needed
- Output is rendered as formatted Markdown in the Gradio interface

---

*"From a URL to a full brochure. In seconds."*
