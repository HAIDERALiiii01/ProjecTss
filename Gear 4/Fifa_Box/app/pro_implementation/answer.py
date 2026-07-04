import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from chromadb import PersistentClient
from litellm import completion
from pydantic import BaseModel, Field
from pathlib import Path
from sentence_transformers import CrossEncoder
from rank_bm25 import BM25Okapi

load_dotenv(override=True)

MODEL = "openai/gpt-4.1-nano"
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
DB_NAME = str(Path(__file__).parent.parent / "preprocessed_db")
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge-base"
SUMMARIES_PATH = Path(__file__).parent.parent / "summaries"

collection_name = "docs"
embedding_model = "text-embedding-3-large"


openai = OpenAI()

chroma = PersistentClient(path=DB_NAME)
collection = chroma.get_or_create_collection(collection_name)



RETRIEVAL_K = 20
FINAL_K = 20

SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant for a FIFA World Cup app, covering all-time stats, iconic moments, tournament winners, and records.
You are chatting with a user about FIFA World Cup history and facts.
Your answer will be evaluated for accuracy, relevance and completeness, so make sure it only answers the question and fully answers it.
If you don't know the answer, say so. If the knowledge base does not have information on a topic (for example, results that have not happened yet, such as an unfinished 2026 World Cup match), say that clearly rather than guessing.
For context, here are specific extracts from the Knowledge Base that might be directly relevant to the user's question:
{context}

With this context, please answer the user's question. Be accurate, relevant and complete.
"""

class Result(BaseModel):
    page_content: str
    metadata: dict

# Load every document from Chroma once
results = collection.get(include=["documents", "metadatas"])
all_chunks = [
    Result(page_content=doc, metadata=meta)
    for doc, meta in zip(results["documents"], results["metadatas"])
]
tokenized_docs = [chunk.page_content.lower().split() for chunk in all_chunks]
bm25 = BM25Okapi(tokenized_docs)

def rerank(question, chunks):
    pairs = [(question, c.page_content) for c in chunks]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [c for c, _ in ranked]

def make_rag_messages(question, history, chunks):
    context = "\n\n".join(
        f"Extract from {chunk.metadata['source']}:\n{chunk.page_content}" for chunk in chunks
    )
    system_prompt = SYSTEM_PROMPT.format(context=context)
    return (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": question}]
    )


def rewrite_query(question, history=[]):
    """Rewrite the user's question to be a more specific question that is more likely to surface relevant content in the Knowledge Base."""
    message = f"""
You are in a conversation with a user, answering questions about the FIFA World Cup - stats, moments, winners, and records.
You are about to look up information in a Knowledge Base to answer the user's question.

This is the history of your conversation so far with the user:
{history}

And this is the user's current question:
{question}

Respond only with a short, refined question that you will use to search the Knowledge Base.
It should be a VERY short specific question most likely to surface content. Focus on the question details.
IMPORTANT: Respond ONLY with the precise knowledgebase query, nothing else.
"""
    response = completion(model=MODEL, messages=[{"role": "system", "content": message}])
    return response.choices[0].message.content

def merge_chunks(chunks, reranked):
    merged = chunks[:]
    existing = [chunk.page_content for chunk in chunks]
    for chunk in reranked:
        if chunk.page_content not in existing:
            merged.append(chunk)
    return merged


def fetch_vector(question):
    query = openai.embeddings.create(model=embedding_model, input=[question]).data[0].embedding
    results = collection.query(query_embeddings=[query], n_results=RETRIEVAL_K)
    chunks = []
    for result in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(Result(page_content=result[0], metadata=result[1]))
    return chunks


def fetch_bm25(question):
    tokens = question.lower().split()
    scores = bm25.get_scores(tokens)
    top_indices = np.argsort(scores)[::-1][:RETRIEVAL_K]
    return [all_chunks[i] for i in top_indices]

def fetch_context(original_question):
    rewritten_question = rewrite_query(original_question)
    vector_original = fetch_vector(original_question)
    vector_rewritten = fetch_vector(rewritten_question)
    bm25_original = fetch_bm25(original_question)
    bm25_rewritten = fetch_bm25(rewritten_question)
    chunks = merge_chunks(vector_original, vector_rewritten)
    chunks = merge_chunks(chunks, bm25_original)
    chunks = merge_chunks(chunks, bm25_rewritten)
    reranked = rerank(original_question, chunks)
    return reranked[:FINAL_K]


def answer_question(question: str, history: list[dict] = []) -> tuple[str, list]:
    """
    Answer a question using RAG and return the answer and the retrieved context
    """
    chunks = fetch_context(question)
    messages = make_rag_messages(question, history, chunks)
    response = completion(model=MODEL, messages=messages)
    return response.choices[0].message.content, chunks
