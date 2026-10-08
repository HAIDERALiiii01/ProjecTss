import os
import glob
import tiktoken
import numpy as np
import frontmatter
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from sklearn.manifold import TSNE
import plotly.graph_objects as go

# price is a factor for our company, so we're going to use a low cost model

MODEL = "gpt-4.1-nano"
db_name = "vector_db"
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# How many characters in all the documents?

knowledge_base_path = "knowledge-base/**/*.md"
files = glob.glob(knowledge_base_path, recursive=True)
print(f"Found {len(files)} files in the knowledge base")

entire_knowledge_base = ""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        entire_knowledge_base += f.read()
        entire_knowledge_base += "\n\n"

print(f"Total characters in knowledge base: {len(entire_knowledge_base):,}")

# How many tokens in all the documents?

encoding = tiktoken.encoding_for_model(MODEL)
tokens = encoding.encode(entire_knowledge_base)
token_count = len(tokens)
print(f"Total tokens for {MODEL}: {token_count:,}")

# Load every markdown file. The YAML front matter (between the --- lines) becomes
# metadata, and only the body text is kept as the page content.

documents = []
for file_path in files:
    post = frontmatter.load(file_path, encoding="utf-8")
    # Chroma only accepts str/int/float/bool metadata, so turn lists into "a, b, c"
    metadata = {
        key: ", ".join(value) if isinstance(value, list) else value
        for key, value in post.metadata.items()
    }
    metadata["doc_type"] = post.metadata.get("type", "general")
    metadata["source"] = file_path
    documents.append(Document(page_content=post.content, metadata=metadata))

print(f"Loaded {len(documents)} documents")

# Divide into chunks in two stages:
#   1. MarkdownHeaderTextSplitter cuts each file at its # / ## headers, so every section
#      becomes one chunk (strip_headers=False keeps the header text inside the chunk).
#   2. RecursiveCharacterTextSplitter is a safety net: it only cuts sections that are
#      longer than chunk_size, preferring paragraph breaks, then sentences.

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2")],
    strip_headers=False,
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

sections = []
for doc in documents:
    for section in header_splitter.split_text(doc.page_content):
        # keep the file's metadata and add the section's own headers (h1, h2)
        section.metadata = {**doc.metadata, **section.metadata}
        sections.append(section)

chunks = text_splitter.split_documents(sections)

# A chunk cut from the middle of a long section has lost its header (and so the topic
# name), so put the header back before embedding.
for chunk in chunks:
    if not chunk.page_content.startswith("#"):
        chunk.page_content = f"## {chunk.metadata.get('h2', '')} (continued)\n{chunk.page_content}"

print(f"Divided into {len(sections)} sections and {len(chunks)} chunks")
print(f"First chunk:\n\n{chunks[0]}")

# Pick an embedding model

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

if os.path.exists(db_name):
    Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
print(f"Vectorstore created with {vectorstore._collection.count()} documents")

# Let's investigate the vectors

collection = vectorstore._collection
count = collection.count()

sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)
print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")