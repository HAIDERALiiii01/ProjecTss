"""Shared RAG logic for the digital twin.

Both app.py (production) and evaluation/eval.py import from here, so the eval
always measures exactly the code path visitors hit.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"      # answers the visitor
REWRITE_MODEL = "gpt-4.1-nano"   # cheap model that rewrites the query before retrieval
DB_NAME = str(Path(__file__).parent / "vector_db")  # absolute path, independent of the working directory
MAX_TOOL_ROUNDS = 5              # safety net against endless tool-call loops
DEBUG = True

openai = OpenAI()

# ---------------------------------------------------------------------------
# Retrieval (LangChain + Chroma)
# ---------------------------------------------------------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # must match ingest.py
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

# MMR: fetch 20 candidates, keep the 5 that are relevant AND different from each other
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.6},
)


def as_text(content):
    # Gradio gives either a string or a list of parts like [{"type": "text", "text": "..."}]
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        ).strip()
    return str(content)


def clean_history(history):
    # Gradio may attach extra keys (metadata, options); the OpenAI API only needs role and content
    return [{"role": m["role"], "content": as_text(m["content"])} for m in history]


def rewrite_query(question, history=None):
    """Turn the visitor's question into a short, standalone query for the knowledge base."""
    history = history or []
    transcript = "\n".join(
        f"{m['role']}: {as_text(m['content'])[:500]}" for m in history[-6:]
    ) or "(no previous messages)"

    prompt = f"""
You are helping a digital twin look up information in a knowledge base about one person's
career, projects, skills, education and background.

Conversation so far:
{transcript}

The visitor's latest question:
{question}

Rewrite the latest question as a short, standalone search query for the knowledge base.
- Resolve references like "it", "that project" or "the first one" using the conversation.
- Keep project names, technologies and other specific terms exactly as written.
- If the question is already standalone, keep it close to the original.
- Do NOT answer the question.

Respond ONLY with the query, nothing else.
"""
    try:
        response = openai.chat.completions.create(
            model=REWRITE_MODEL,
            temperature=0,
            messages=[{"role": "system", "content": prompt}],
        )
        return response.choices[0].message.content.strip() or question
    except Exception as e:
        print(f"Query rewrite failed, falling back to the original question: {e}")
        return question


def fetch_context(question, history=None):
    """Rewrite the question, then return the retrieved chunks (a list of Documents)."""
    query = rewrite_query(question, history)
    docs = retriever.invoke(query)

    if DEBUG:
        print(f"\n{'=' * 60}\nORIGINAL:  {question}\nREWRITTEN: {query}\n{'=' * 60}")
        for i, doc in enumerate(docs, 1):
            source = str(doc.metadata.get("source", "?")).replace("\\", "/").split("/")[-1]
            section = doc.metadata.get("h2") or doc.metadata.get("h1") or "-"
            print(f"\n[{i}] {source} | {section} | {len(doc.page_content)} chars")
            print(doc.page_content)
        print("=" * 60, flush=True)

    return docs


def format_context(docs):
    parts = []
    for doc in docs:
        source = str(doc.metadata.get("source", "knowledge base")).replace("\\", "/").split("/")[-1]
        parts.append(f"Source: {source}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def build_system_prompt(context):
    return (
        TWIN_SYSTEM_PROMPT
        + f"""

# Retrieved knowledge

The excerpts below were retrieved from the knowledge base for the visitor's latest question.
They are your source of truth. Answer from them in the first person, as the person you represent.
Only call the record_unknown_question tool if the excerpts contain nothing relevant to the question.
If you can answer even part of it, answer that part and do not call the tool. Never guess beyond the excerpts.

{context}
"""
    )


# ---------------------------------------------------------------------------
# Answering
# ---------------------------------------------------------------------------
def dry_run_tool_calls(tool_calls):
    """Same shape as handle_tool_calls, but sends no notifications (used by the eval)."""
    results = []
    for tool_call in tool_calls:
        print(f"[dry run] tool call: {tool_call.function.name} {tool_call.function.arguments}", flush=True)
        results.append(
            {"role": "tool", "content": json.dumps("OK"), "tool_call_id": tool_call.id}
        )
    return results


def answer_question(question, history=None, notify=True):
    """Answer a visitor question. Returns (answer_text, retrieved_docs).

    notify=False keeps the tools visible to the model but stubs them, so evaluation
    runs never send real ntfy alerts.
    """
    history = history or []
    docs = fetch_context(question, history)  # once per user turn, not per tool iteration

    messages = (
        [{"role": "system", "content": build_system_prompt(format_context(docs))}]
        + clean_history(history)
        + [{"role": "user", "content": as_text(question)}]
    )
    run_tools = handle_tool_calls if notify else dry_run_tool_calls

    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    rounds = 0
    while response.choices[0].finish_reason == "tool_calls" and rounds < MAX_TOOL_ROUNDS:
        assistant_message = response.choices[0].message
        results = run_tools(assistant_message.tool_calls)
        messages.append(assistant_message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
        rounds += 1

    return response.choices[0].message.content or "", docs