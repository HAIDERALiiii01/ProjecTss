# World Cup Archive — UI

A desktop shell (pywebview) around your existing RAG pipeline. Two card rails
— **Winners** and **Moments** — hover to preview, click for a short
documentary-style writeup, plus a slide-in chat drawer wired straight to
`answer_question()`.

## Setup

```bash
pip install -r ui/requirements.txt
```

(this is on top of whatever your RAG pipeline already needs — openai,
chromadb, litellm, sentence-transformers, rank_bm25, python-dotenv, etc.)

## Before running: fix one import path

`ui/main.py` assumes your project looks like:

```
fifa/
  app/
    evaluation/
    pro_implementation/
      ingest.py
      answer.py        <- exposes answer_question(question, history)
    preprocessed_db/
    knowledge-base/
  ui/           <- this folder
```

and does `from app.pro_implementation.answer import answer_question`. If
`answer_question` lives somewhere else, edit that one import line near the
top of `ui/main.py`.

If `app/` or `app/pro_implementation/` don't have `__init__.py` files, add
empty ones — makes them proper packages instead of namespace packages,
which is more robust for imports in general.

## Run

```bash
python ui/main.py
```

(the entry script is named `main.py`, not `app.py`, on purpose — a
sibling script literally named `app.py` can shadow a namespace-package
`app/` folder and break its internal imports)

This opens a native window. No separate server, no browser tab — pywebview
renders `ui/web/index.html` directly and your Python `Api` class is
reachable from JS as `window.pywebview.api`.

## What's wired up already

- `Api.get_winners()` / `Api.get_moments()` → serve `ui/data/*.json`
- `Api.ask(question)` → calls your `answer_question(question, history)`,
  keeps a rolling chat history, and returns `{answer, sources}`
- The JS frontend renders both, handles hover-gif swapping with graceful
  placeholder fallback, the detail overlay, and the chat drawer.

## What you'll want to add

- **Media** — see `assets/README.md`. Everything renders fine without it;
  it just looks better with real posters/gifs.
- **More winners/moments entries** — edit `data/winners.json` /
  `data/moments.json`. Each entry just needs an `id`, `year`, and a
  `timeline` array of 3–5 short sentences; the UI handles the rest.
- **"Ask about this" deep-linking** — right now clicking that button on a
  detail page opens the chat pre-filled with a question about that
  entry. If you want it to also inject extra system context (e.g. force
  retrieval to prioritize that specific source document), that's a small
  change to `Api.ask()` to accept an optional `context_hint` param.

## Design notes

Palette and type are deliberately not the generic "dark + neon" AI-UI
default — it's built around a stadium-at-night feel (deep navy, floodlight
gold, chalk white) with a flip-scoreboard treatment for years as the one
signature visual element. `Anton` for display type (poster/scoreboard
signage feel), `Inter` for body copy, `IBM Plex Mono` for stats and data.
All in `web/css/style.css` if you want to retheme.
