# PyPlus 🐍➕

<p align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmI3c2Fndmk0Y3VnOXpyM3M1aGQyZmdzZnd6dnUzb2VyMHpnNmN1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/d4blalI6x2oc4xAA/giphy.gif" width="600"/>
</p>

> Convert Python to blazing-fast C++ — powered by open and closed source AI models.

---

## 🎯 What it does

PyPlus is an AI-powered Python-to-C++ code converter with a Gradio web interface. Write or paste any Python code, pick your model, and watch it get ported to high-performance C++ — compiled and run right from the UI so you can compare execution times side by side.

---

## 📁 Project Files

| File | Description |
| --- | --- |
| `open_source.ipynb` | 🦙 Uses local Ollama models (Llama, Qwen) — free, runs offline |
| `closed_source.ipynb` | 🔑 Uses GPT and Gemini APIs — more powerful, requires API keys |
| `system_info.py` | Collects system details (OS, CPU, memory, Python version) used to tailor compiler commands |
| `styles.py` | Custom CSS for the Gradio UI |
| `requirements.txt` | All Python dependencies |

---

## ⚙️ How it works

1. **System scan** — `system_info.py` profiles your machine (OS, architecture, installed compilers)
2. **Compiler setup** — An AI call analyzes your system and tells you the optimal `compile_command` and `run_command` for your environment
3. **Port** — The selected model receives your Python code and rewrites it as optimized C++
4. **Compile & run** — The generated C++ is saved as `main.cpp`, compiled with g++, and executed via `subprocess`
5. **Compare** — Python and C++ outputs (and runtimes) are shown side by side in the UI

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>
cd PyPlus
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API keys (closed source notebook only)

Create a `.env` file in the project directory:

```
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

> **OpenAI key** — Paid. Get yours at: https://platform.openai.com/api-keys  
> **Google/Gemini key** — Free tier available. Get yours at: https://aistudio.google.com/app/apikey  
>
> If you only want to use Gemini, you can remove the OpenAI client from the code — and vice versa.

For `open_source.ipynb`, no API keys are needed. Just have [Ollama](https://ollama.com/) installed with your chosen models pulled:

```bash
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:3b
```

---

## 📓 Running the Notebooks

You have two options for running Jupyter notebooks:

### Option A — VS Code (recommended)

1. Install the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) in VS Code
2. Open `open_source.ipynb` or `closed_source.ipynb`
3. Select your Python interpreter (top right of the notebook)
4. Run cells one by one with **Shift + Enter**, or click **Run All**

### Option B — Browser (JupyterLab)

```bash
pip install jupyterlab
jupyter lab
```

This opens JupyterLab in your browser automatically. Navigate to the notebook file and open it. You can also use the classic Jupyter Notebook interface:

```bash
jupyter notebook
```

---

## 🔧 Compiler Setup (Important Step)

Before you can compile C++, you need to run the **compiler detection cell** in the notebook. It sends your system info to GPT and asks it to figure out the right compile and run commands for your machine.

**Here's how to do it:**

1. Run the `system_info` cell to collect your machine details
2. Run the next cell — it sends that info to the AI and prints instructions
3. Read the output — it will tell you either:
   - ✅ You're already set up — and give you the exact `compile_command` and `run_command` to use
   - ⚠️ You need to install a compiler — with step-by-step instructions for your OS
4. Copy the suggested commands and paste them into the cell that defines `compile_command` and `run_command`, like this:

```python
compile_command = ["g++", "-std=c++17", "-O3", "-march=native", "main.cpp", "-o", "main.exe"]
run_command = ["main.exe"]
```

The flags `-O3 -march=native` enable maximum optimization for your specific CPU — this is what makes C++ dramatically faster than Python for compute-heavy tasks.

---

## 🤖 Choosing Models

### Open Source (`open_source.ipynb`)

Models are defined in a list at the top of the notebook:

```python
models = ["llama3.2:3b", "qwen2.5-coder:3b"]
```

Add or swap any model you have pulled in Ollama. Larger models (7b, 13b) generally produce better C++ but are slower.

### Closed Source (`closed_source.ipynb`)

```python
models = ["gpt-5-nano", "gpt-5-mini", "gpt-4o-mini", "gpt-4o", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
```

Feel free to add or remove models from this list. The code automatically routes GPT models to the OpenAI client and Gemini models to the Google client. Reasoning models like `gpt-4o` will use `reasoning_effort="high"` automatically.

---

## 🎮 Using the Interface

Once you run the final cell in either notebook, a Gradio interface launches in your browser:

- **Left panel** — Python code editor (pre-loaded with a pi calculation benchmark)
- **Right panel** — Generated C++ output
- **Run Python** — Executes the Python code and shows the result + time
- **Port to C++** — Sends the code to the selected model for conversion
- **Run C++** — Compiles and runs the generated C++
- **Bottom panels** — Side-by-side output comparison

You can edit the Python code directly in the UI before converting.

---

## 📦 Requirements

Install everything at once:

```bash
pip install -r requirements.txt
```

Key packages: `openai`, `gradio`, `python-dotenv`, `IPython`

---

## 📝 Notes

- The default benchmark computes π using 200 million iterations — a good stress test to see the speed difference between Python and C++
- Some systems (especially Windows) may use `main.exe`; Linux/macOS typically use `./main` — the AI's compiler cell will handle this for you
- If compilation fails, the error from `g++` is shown directly in the C++ output panel
- The open source notebook always uses Ollama locally — no internet needed after setup

---

*"For when Python says: 'I'm trying my best.'"*
