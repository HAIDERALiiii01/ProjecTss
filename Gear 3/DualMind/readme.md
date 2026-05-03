
# 🧠 DualMind
<p align="center">
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXo0MG12a21jdTBlemZvYmJrNzB0a2xxc2NkeXV4cnYwYmR3d2dzcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/j9pKCnYLbN1nqYcuHc/giphy.gif" width="600"/>
</p>

> Give it a prompt — get an image. Give it an image — get a caption. Powered by SDXL and BLIP-2. 🤖

---

## 🎯 What it does

An AI-powered dual-mode vision studio running inside Google Colab. Choose between **Text-To-Image** generation or **Image Captioning** from a clean Gradio interface. It intelligently swaps models in and out of GPU memory as needed — so you never run out of VRAM.

---

## 📁 Files

| File | Description |
| --- | --- |
| `DualMind.ipynb` | 🚀 The entire project — open and run this in Google Colab |

---

## 🤖 Models Used

| Model | Source | Purpose |
| --- | --- | --- |
| `stabilityai/stable-diffusion-xl-base-1.0` | [Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | Generates high-quality images from text prompts |
| `madebyollin/sdxl-vae-fp16-fix` | [Hugging Face](https://huggingface.co/madebyollin/sdxl-vae-fp16-fix) | Improved VAE for SDXL — reduces color artifacts |
| `Salesforce/blip2-opt-2.7b` | [Hugging Face](https://huggingface.co/Salesforce/blip2-opt-2.7b) | Generates detailed captions from uploaded images |

---

## ⚙️ How it works

1. **Select** — Choose a mode: Text-To-Image or Image Captioning from the dropdown
2. **Load** — The app loads the correct model into GPU memory (and unloads the other to save VRAM)
3. **Input** — Either type a prompt (for image generation) or upload a photo (for captioning)
4. **Run** — Hit the Run button and watch the result appear in the output panel
5. **Swap** — Switch modes anytime — the app handles model swapping automatically

---

## 🚀 Getting Started on Google Colab

> **New to Colab?** No worries — follow these steps carefully and you'll be running the project in minutes.

### 1. Open Google Colab

Go to [colab.research.google.com](https://colab.research.google.com) and sign in with your Google account.

### 2. Upload the notebook

- Click **File → Upload notebook**
- Select `DualMind.ipynb` from your computer
- The notebook will open in your browser

### 3. Enable GPU (Important!)

The models require a GPU to run. Enable it before running anything:

- Click **Runtime → Change runtime type**
- Set **Hardware accelerator** to **T4 GPU**
- Click **Save**

### 4. Set up your Hugging Face token

This project downloads models from Hugging Face, which requires a free API token.

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Go to **Settings → Access Tokens** and create a token (read access is enough)
3. In Colab, click the **🔑 key icon** in the left sidebar
4. Add a new secret named `HF_TOKEN` and paste your token as the value
5. Make sure the toggle next to `HF_TOKEN` is **enabled**

### 5. Run all cells

- Click **Runtime → Run all**  
  *(or press `Ctrl+F9`)*
- Wait for each cell to finish — the first run downloads the models which takes a few minutes
- When you see the Gradio interface with a public link, you're ready!

---

## 🎮 How to use

- Select **Text-To-Image** or **Image Captioning** from the dropdown
- For **Text-To-Image**: type a descriptive prompt and click **Run**
- For **Image Captioning**: upload any image and click **Run**
- Switch between modes freely — the app manages memory automatically

---

## 📝 Notes

- A **Hugging Face token** is required — the notebook logs in to download SDXL and BLIP-2
- A **T4 GPU** (or better) is required — CPU mode is not supported
- Model loading takes 1–3 minutes the first time each model is used
- Switching between modes triggers a model swap — expect a short delay
- Some websites may throttle Hugging Face downloads — if it stalls, try re-running the cell
- Generated images are 768×768 by default

---

*"Power of the sun, in the palm of my hand😁."*
