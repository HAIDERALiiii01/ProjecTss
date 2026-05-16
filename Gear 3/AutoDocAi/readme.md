# 🤖 AutoDoc AI — AI Based Code Commenter

<p align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXlkb2Z2dTMyZzJnMjJkc3RwMHFqcWd3ZHpvaWNwdXozd254OThvNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/sSmxfWnEVxtWU/giphy.gif" width="600"/>
</p>

> Paste your code. Pick a style. Get it commented. Powered by GPT and Gemini. 🤖

---

## 🎯 What it does

An AI-powered code documentation tool with a Gradio web interface. Paste any code, select the language, choose a comment style (short, detailed, beginner-friendly, etc.), and the model adds meaningful comments throughout — instantly.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.ipynb` | 📓 Main notebook — run all cells to launch the Gradio interface |
| `styles.py` | 🎨 Custom CSS for the Gradio UI |
| `requirements.txt` | 📦 All dependencies listed — install with one command |
| `.env` | Stores your API keys — create this yourself |

---

## ⚙️ How it works

1. **Input** — Paste your code and select the programming language
2. **Style** — Choose your preferred comment style from the dropdown
3. **Model** — Select GPT or Gemini from the model dropdown
4. **Generate** — The model reads your code and adds comments throughout
5. **Output** — Commented code appears in the right panel, ready to copy

---

## 🚀 Getting started

### 1. Clone the repository

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 3/AutoDocAi"
```

### 2. Install dependencies

Using `requirements.txt` (recommended):
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install openai gradio python-dotenv
```

### 3. Set up API keys

Create a `.env` file in the same directory:
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here

> Get your OpenAI key from: https://platform.openai.com/api-keys  
> Get your Gemini key from: https://aistudio.google.com/app/apikey

---

## 📓 How to run the notebook

You have two options:

### Option A — VS Code (recommended)
1. Install [VS Code](https://code.visualstudio.com/)
2. Install the **Jupyter** extension from the Extensions panel
3. Open `main.ipynb` directly in VS Code
4. Click **Run All** or run cells one by one with `Shift+Enter`

### Option B — JupyterLab in browser
1. Make sure Jupyter is installed:
```bash
pip install jupyterlab
```
2. Launch it from your terminal inside the project folder:
```bash
jupyter lab
```
3. Your browser will open automatically — navigate to `main.ipynb` and run all cells

---

## 🎮 How to use

- Select the **programming language** from the dropdown
- Paste your **code** in the left panel
- Choose a **comment style**:
  - `Short inline` — brief one-liners
  - `Detailed` — thorough explanations per block
  - `Beginner-friendly` — simple language, great for learning
  - `Docstrings only` — only function/class-level docs
  - `Senior engineer style` — concise, professional, assumes knowledge
- Select a **model** from the dropdown
- Click **Add Comments** and get your documented code in the right panel

---

## 🌐 Want to use open-source models?

You can swap GPT/Gemini for free open-source models using **Ollama** — no API key needed.

### 1. Install Ollama
Download from: https://ollama.com

### 2. Pull a model
```bash
ollama pull llama3
# or
ollama pull codellama   # better for code tasks
ollama pull deepseek-coder
```

### 3. Point the client to Ollama's local server
Ollama runs an OpenAI-compatible server locally, so add this to the notebook:
```python
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

Then add your Ollama models to the `models` list and handle them in `get_client()` just like GPT and Gemini.

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

---

## 📝 Notes

- Google API key is optional if you only use GPT models
- Some very large code files may hit token limits — split them into smaller chunks
- The language dropdown controls syntax highlighting and tells the model what language it's reading
- Output can be copied directly from the right panel

---

*"Saving developers from: 'I'll document it later.😉"*
