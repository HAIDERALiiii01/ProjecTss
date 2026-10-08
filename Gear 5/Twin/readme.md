# 🤖 AI Resume Twin

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzdjbG10MTN1NWJ6NWg0YTRpbnFzenozdHJmcnZrcG1nY204aWlkMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l36kU80xPf0ojG0Erg/giphy.gif" alt="AI Resume Twin" width="800"/>
</p>

<p align="center">
  <strong>A conversational digital twin that lets recruiters ask about your projects, skills, education, career goals, and story, instead of just reading a PDF.</strong>
</p>

<p align="center">
  Built with Python · Gradio · LangChain · ChromaDB · LLM-powered RAG · Deployed on Render
</p>

---

## 🎯 What it does

A traditional resume tells people **what you have done**. AI Resume Twin lets them **ask about it**.

Recruiters can ask things like:

- What projects have you built?
- Tell me about your DealScout project.
- What technologies do you use?
- What are your strongest skills?
- What kind of AI/ML role are you looking for?
- What are you currently learning?
- Why should we consider you for an AI internship?

The twin uses **Retrieval-Augmented Generation (RAG)**: it retrieves the most relevant parts of your knowledge base, then has an LLM answer using only that context. When it doesn't know something, it says so, and can record the question for you.

> This repository is a **template**. Replace the knowledge base, summary, and prompts with your own information before deploying.

---

## 🧠 How it works

```text
User Question
      ↓
Query Rewriting (LLM)
      ↓
Retrieval (ChromaDB)
      ↓
System Prompt + Summary + Retrieved Context
      ↓
LLM
      ↓
Answer (Gradio UI)
```

1. **Rewrite**: the question is rewritten into a clearer, standalone search query so follow-ups like "what about the second one?" still retrieve well.
2. **Retrieve**: the rewritten query is embedded and matched against ChromaDB.
3. **Generate**: the retrieved chunks are combined with your system prompt and `summary.txt`, and the LLM writes the answer.
4. **Act**: if the question reveals a real knowledge gap or a visitor leaves contact details, the twin's tools record it.

The Markdown knowledge base is never queried directly. `ingest.py` splits it into chunks, embeds them, and stores them in a local vector database.

---

## 🛠️ Built-in tools

The twin can take actions, not just answer:

- **Record visitor email:** if a recruiter wants to get in touch, the twin saves their email address.
- **Record unanswered questions:** if a question points to a real gap in the knowledge base, it's logged (and you're notified) so you know what to add next. Off-topic or trivial questions don't trigger it.

## 📁 Project structure

```text
Twin/
│
├── knowledge-base/
│   ├── projects/
│   │   ├── brochure.md
│   │   ├── dealscout.md
│   │   ├── fifa-box.md
│   │   └── shadow_clone_jutsu.md
│   ├── career.md
│   ├── education.md
│   ├── faq.md
│   ├── skills.md
│   └── story.md
│
├── evaluation/
│   ├── eval.py
│   ├── test.py
│   └── tests.jsonl
│
├── answer.py
├── app.py
├── context.py
├── evaluator.py
├── ingest.py
├── styles.py
├── tools.py
├── summary.txt
├── requirements.txt
└── README.md
```

| File / Folder | Purpose |
|---|---|
| `knowledge-base/` | The RAG knowledge base (Markdown) |
| `knowledge-base/projects/` | One file per project |
| `career.md` | Career goals and the roles you want |
| `education.md` | Education and academic background |
| `faq.md` | Common recruiter questions and answers |
| `skills.md` | Skills, technologies, and practical experience |
| `story.md` | Your learning and career story |
| `summary.txt` | Short, fixed profile summary injected into every prompt |
| `context.py` | System prompt and context configuration |
| `answer.py` | Query rewriting, retrieval, and answer generation |
| `ingest.py` | Builds the ChromaDB vector database |
| `app.py` | Gradio app entry point |
| `tools.py` | Agent tools: record visitor contact details and unanswered questions |
| `evaluator.py` | LLM-judge evaluation logic |
| `evaluation/` | Evaluation scripts and test questions |
| `styles.py` | UI styling |

---

## ⚙️ Customize before using

### 1. Knowledge base

Replace everything in `knowledge-base/` with your own information. You can rename, add, or remove files, but the content must be **accurate**, because the twin treats it as the source of truth.

Write for retrieval, and focus on what a recruiter would actually ask:

```markdown
# Project Name

## Overview
What the project does.

## Technologies
- Python
- LangChain
- ChromaDB

## What I Built
Your specific contribution.

## What I Learned
The key concepts you picked up.

## Challenges
Problems you solved.
```

You don't need an entry for every small project. Point to your GitHub profile for the rest.

### 2. `summary.txt`

A short, high-level profile used directly in the prompt. Keep it concise; details belong in the knowledge base.

```text
Name: Your Name

Education:
BS Computer Science student at XYZ University.

Focus:
Machine Learning, AI, LLMs, and Agentic AI.

Career Goal:
AI/ML internships and junior AI/ML roles.

Location:
Your City, Country.

GitHub:
Your GitHub profile.

LinkedIn:
Your LinkedIn profile.
```

### 3. Prompts

Review `context.py` and `answer.py`. The prompts control your twin's identity, tone, and boundaries. Useful rules to include:

- Never invent experience or technologies.
- Say clearly when information is unavailable.
- Keep recruiter-facing answers concise, in readable Markdown.
- Decline unrelated questions politely.

---

## 🏗️ Build the vector database

```bash
python ingest.py
```

Rebuild it whenever you change the knowledge base: new or edited projects, skills, education, career goals, or FAQ entries. UI or application-logic changes don't require a rebuild.

The generated `vector_db/` should **not** be committed. Add this to `.gitignore`:

```gitignore
vector_db/
.venv/
__pycache__/
.env
```

---

## 🚀 Run locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

# 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 3. Dependencies
pip install -r requirements.txt

# 4. Build the vector database
python ingest.py

# 5. Start the app
python app.py
```

Create a `.env` file with your keys:

```dotenv
OPENAI_API_KEY=your_api_key
```

Add any other keys your setup needs (for example, notification credentials for `tools.py`). **Never commit `.env` or API keys.**

---

## 🌐 Deploy to Render

```text
GitHub → Render → install dependencies → run ingest.py → start app.py
```

**1. Push to GitHub.** Include `app.py`, `answer.py`, `context.py`, `ingest.py`, `evaluator.py`, `tools.py`, `styles.py`, `summary.txt`, `requirements.txt`, and `knowledge-base/`. Exclude `.env`, `.venv/`, `__pycache__/`, and `vector_db/`.

**2. Create a Web Service** on Render and connect your repository.

**3. Build command:**

```bash
pip install -r requirements.txt && python ingest.py
```

This builds a fresh vector database on every deploy, so the knowledge base stays the single source of truth and you never upload `vector_db/` yourself.

**4. Start command:**

```bash
python app.py
```

Your Gradio launch must work on a cloud server:

- Listen on `0.0.0.0` and use Render's `PORT` environment variable.
- Do **not** use `inbrowser=True`. It only makes sense locally.

**5. Environment variables.** Add `OPENAI_API_KEY` (and any tool credentials) in Render's **Environment** settings, not in `context.py`, `answer.py`, or `tools.py`. Because `ingest.py` runs at build time, keys needed for embeddings must be set before the first deploy.

### Updating the deployed twin

```text
Edit knowledge-base/ → commit → push → Render rebuilds → ingest.py → updated twin
```

---

## 🧪 Evaluation

```text
evaluation/
├── eval.py
├── test.py
└── tests.jsonl
```

The evaluation suite checks both **retrieval quality** and **answer quality** (via an LLM judge). Write test questions in `tests.jsonl` that cover:

- Projects, skills, education, career, and personal story
- Unanswerable questions (the twin should admit it doesn't know)
- Off-topic questions (the twin should stay in scope)

The goal is to confirm that your twin retrieves the right context, answers from it, doesn't invent information, and handles unknowns gracefully. Re-run it after every significant change to the knowledge base, retrieval settings, or prompts.

---

## 🛠️ Ideas to extend it

- **Knowledge:** certifications, experience, achievements, publications, contact info
- **RAG:** different embedding models, chunk sizes and overlap, metadata filtering, reranking, hybrid search
- **LLM:** swap in any compatible model or provider
- **UI:** Gradio theme, layout, colors, profile image, project cards, social links
- **Tools:** interview scheduling, feedback collection, other notification channels

---

## 📦 Tech stack

| Technology | Role |
|---|---|
| **Python** | Application code |
| **Gradio** | Web interface |
| **LangChain** | Retrieval framework |
| **ChromaDB** | Vector database |
| **Embeddings** | Semantic representation of the knowledge base |
| **LLMs** | Query rewriting, answer generation, evaluation |
| **Markdown** | Knowledge-base format |
| **Render** | Cloud deployment |

---

## 📌 Recommended workflow

```text
1. Edit knowledge-base/
2. Update summary.txt, context.py, or answer.py if needed
3. python ingest.py
4. python app.py and test the twin
5. Run the evaluation suite
6. Commit and push
7. Render rebuilds and deploys
```

---

## ⚠️ Important notes

- **Your knowledge base is the source of truth.** The twin should only claim what's in it, so keep it accurate.
- **Rebuild after knowledge changes**, locally or via Render's build command.
- **Never commit secrets** (`.env`, API keys, tokens) **or `vector_db/`.**

> Don't treat this repository as a finished product. Make it yours: customize the knowledge, prompts, models, retrieval pipeline, UI, and tools.
