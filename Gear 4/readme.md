<p align="center">
  <img src="https://media.giphy.com/media/Q7gdXSIVy5RnEHvFTh/giphy.gif" alt="Gear 4" width="800"/>
</p>

# Gear 4 👀

[![Python](https://img.shields.io/badge/python-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-green?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![ML](https://img.shields.io/badge/machine%20learning-informational?style=flat-square)](https://github.com/HAIDERALiiii01/ProjecTss)
[![RAG](https://img.shields.io/badge/RAG-purple?style=flat-square)](https://github.com/HAIDERALiiii01/ProjecTss)
[![Stars](https://img.shields.io/github/stars/HAIDERALiiii01/ProjecTss?style=flat-square)](https://github.com/HAIDERALiiii01/ProjecTss/stargazers)

Computer vision, machine learning, and retrieval-augmented generation projects — where the machine starts to see, and starts to know.

> [!NOTE]
> Projects use a mix of OpenCV/ML libraries and RAG stacks (vector DBs, embeddings, LLM APIs). Check each project's own README/requirements before running — some need a `.env` with API keys, others just need OpenCV.

---

## About

Gear 4 is all about teaching machines to see, understand, and now — recall. Built while learning computer vision and machine learning fundamentals, it's grown to include retrieval-augmented generation projects too: assistants grounded in real knowledge bases instead of guesswork. Each project here is inspired by something fun, and gets more powerful as the gear grows.

## What's inside

| Project | Type | Description |
|---|---|---|
| 🥷 Shadow Clone Jujutsu | CV | Creates a shadow clone effect using computer vision |
| ⚽ Fifa_Box | RAG | A FIFA World Cup RAG assistant — hybrid vector + BM25 retrieval, cross-encoder reranking, wrapped in a stadium-themed desktop UI (pywebview) |

## Getting started

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 4"
```

Each project lives in its own folder with its own `requirements.txt` — install and run from inside that folder:

```bash
cd "<project folder>"
pip install -r requirements.txt
python <entry_point>.py
```

RAG projects (like Fifa_Box) additionally need a `.env` file with your API key(s) before running — see that project's own README for specifics.

## Requirements

- Python
- **CV projects:** OpenCV — `pip install opencv-python`, plus MediaPipe/TensorFlow where noted
- **RAG projects:** an LLM API key (e.g. OpenAI), plus vector store / embedding / reranking libraries (Chroma, sentence-transformers, rank_bm25, litellm)
- Any additional dependencies will be noted inside each project folder.

---

*"The eye that sees the truth is not the one that looks — it's the one that understands." 👁️*
