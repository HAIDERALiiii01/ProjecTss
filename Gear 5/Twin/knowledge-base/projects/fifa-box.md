---
type: project
name: Fifa_Box
topics: [rag, hybrid-retrieval, bm25, reranking, evaluation, desktop-app]
stack: Python, ChromaDB, BM25, OpenAI, LiteLLM, cross-encoder, pywebview, HTML/CSS/JavaScript
---

# Fifa_Box: Hybrid RAG Assistant for FIFA World Cup History

## What Fifa_Box is and why I built it

Fifa_Box is a Retrieval-Augmented Generation (RAG) assistant for FIFA World Cup history that I built. It answers questions about winners, records, statistics, and iconic moments using a real knowledge base covering 93 years of World Cup history, from 1930 to 2022, instead of relying only on the language model's own knowledge.

I built it to give grounded answers: the system first retrieves relevant information from the knowledge base, then generates the answer from that retrieved context. I also built a desktop app around it, so the RAG system became a browsable World Cup archive with a built-in chat.

## How the Fifa_Box pipeline works

In Fifa_Box, the complete pipeline is: ingestion, then query rewriting, then hybrid retrieval, then reranking, then generation, then the UI. The retrieval system combines dense vector search, BM25 keyword search, query rewriting, and cross-encoder reranking. Each stage has a specific role in producing a grounded answer.

## Knowledge base ingestion

In Fifa_Box, I built an ingestion pipeline (`app/pro_implementation/ingest.py`) that loads the documents from the knowledge-base folder and prepares them for retrieval.

An LLM splits the documents into overlapping chunks, and each chunk contains a headline, a summary, and the original text. The chunks are embedded with OpenAI's `text-embedding-3-large` model and stored in a persistent ChromaDB collection. The ingestion has to be run again whenever documents are added or changed.

## Query rewriting

In Fifa_Box, every question first goes through a query-rewriting step. The system rewrites my question into a shorter, search-optimized query, and the rewritten query is used alongside the original question during retrieval. The purpose is to improve the quality of the search before anything is retrieved.

## Hybrid retrieval: dense vectors and BM25

In Fifa_Box, I use hybrid retrieval instead of relying on vector similarity alone. It combines dense vector search with BM25 keyword search. Both the original question and the rewritten query are searched, and the results are merged into one candidate set.

Dense search converts the question into an embedding and compares it with the embedded chunks in ChromaDB to find semantically similar information. BM25 (via `rank_bm25`) complements it by matching important exact terms from the question. I combined the two so the system benefits from both semantic matching and direct keyword matching.

## Cross-encoder reranking

In Fifa_Box, after the hybrid results are merged, I rerank the candidate chunks with a cross-encoder, `ms-marco-MiniLM-L-6-v2`. The cross-encoder scores each candidate against the original question and produces a more relevant ordering. The top-ranked chunks are then passed to the generation stage.

## Answer generation

In Fifa_Box, the top reranked chunks are placed into the model's context, and the LLM generates the final answer from that retrieved information. This keeps the answers grounded in the World Cup knowledge base. LiteLLM handles the LLM calls for query rewriting, document chunking, and answer generation.

## Evaluation of Fifa_Box

I built a custom evaluation suite for Fifa_Box with 179 test cases. It scores retrieval quality with MRR, nDCG, and Precision@5, which came out at about 0.80. It scores answer quality with an LLM-as-judge on four criteria: accuracy, completeness, relevance, and faithfulness. The evaluation scripts and test set are in the `app/evaluation/` folder.

## The Fifa_Box desktop app

In Fifa_Box, I built the interface as a desktop application with `pywebview` and a hand-built HTML, CSS, and JavaScript frontend. It is designed like a browser-style archive with three parts: World Cup Winners, Iconic Moments, and the Press Box, which is the chat interface connected directly to the RAG pipeline. The Winners and Moments sections are browsable and clickable, and the winners data covers champions from 1930 to 2022. The app can run without external image assets by generating placeholder artwork, and real photos and GIFs can be added optionally.

## Fifa_Box architecture: no backend server

In Fifa_Box, there is no separate backend server. The pywebview desktop shell calls the `answer_question()` function directly, so the retrieval and generation pipeline runs in the same Python process as the desktop app. The whole application is the Python logic, the web frontend, the pywebview shell, the ChromaDB vector store, and the RAG pipeline in one process.

## Fifa_Box project structure

- `ui/main.py`: entry point that launches the desktop app.
- `ui/web/`: the frontend (`index.html`, `css/style.css`, `js/main.js`).
- `ui/data/`: `winners.json` and `moments.json` with the champions and curated moments.
- `ui/assets/`: posters, GIFs, and galleries.
- `app/pro_implementation/ingest.py`: ingestion, LLM chunking, embeddings, and ChromaDB construction.
- `app/pro_implementation/answer.py`: query rewriting, hybrid retrieval, reranking, and answer generation.
- `app/knowledge-base/`: the source documents.
- `app/preprocessed_db/`: the persistent ChromaDB store generated during ingestion.
- `app/evaluation/`: the evaluation scripts and test set.

## Technologies used in Fifa_Box

- Retrieval: ChromaDB, OpenAI `text-embedding-3-large`, BM25 (`rank_bm25`), cross-encoder reranking (`ms-marco-MiniLM-L-6-v2`)
- LLM: OpenAI models, LiteLLM
- Application: Python, pywebview, HTML, CSS, JavaScript
- Supporting libraries: Pydantic, python-dotenv

## Links

GitHub and demo: see the links on my resume.