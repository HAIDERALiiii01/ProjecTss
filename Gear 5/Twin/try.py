from dotenv import load_dotenv; load_dotenv(override=True)
from answer import fetch_context

docs = fetch_context("What was the hardest part of building DealScout?", [])
print(len(docs))
for d in docs: print("-", d.page_content[:120].replace("\n", " "))
print("integrating" in " ".join(d.page_content.lower() for d in docs))