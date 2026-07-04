import sys
import json
import traceback
from pathlib import Path

import webview

UI_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = UI_DIR.parent

# Make the sibling `app` package (your ingest.py / query.py) importable.
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from app.pro_implementation.answer import answer_question  # noqa: E402
except ImportError as e:
    print(
        "Could not import `answer_question` from app.pro_implementation.answer.\n"
        "Edit the import path at the top of ui/main.py to match your project's "
        "actual folder layout (wherever answer_question is defined).\n"
        f"Original error: {e}"
    )
    answer_question = None


class Api:
    """Everything the JS frontend can call is a method on this class."""

    def __init__(self):
        self.history: list[dict] = []

    # ---- static data for the two rails -----------------------------
    def get_winners(self):
        return json.loads((UI_DIR / "data" / "winners.json").read_text(encoding="utf-8"))

    def get_moments(self):
        return json.loads((UI_DIR / "data" / "moments.json").read_text(encoding="utf-8"))

    # ---- chat ---------------------------------------------------------
    def ask(self, question: str):
        if answer_question is None:
            return {
                "answer": (
                    "The RAG backend isn't wired up yet — fix the import at the top "
                    "of ui/app.py so it can find your query.py."
                ),
                "sources": [],
            }
        try:
            answer, chunks = answer_question(question, self.history)
            self.history.append({"role": "user", "content": question})
            self.history.append({"role": "assistant", "content": answer})

            # Keep the running history bounded so context doesn't grow forever.
            self.history = self.history[-16:]

            sources = []
            for chunk in chunks:
                src = chunk.metadata.get("source", "")
                if src and src not in sources:
                    sources.append(src)
            return {"answer": answer, "sources": sources[:5]}
        except Exception:
            traceback.print_exc()
            return {
                "answer": "Something went wrong looking that up. Please try again.",
                "sources": [],
            }

    def reset_chat(self):
        self.history = []
        return True


def main():
    api = Api()
    window = webview.create_window(
        "World Cup Archive",
        str(UI_DIR / "web" / "index.html"),
        js_api=api,
        width=1920,
        height=1080,
        fullscreen=True,
        min_size=(1000, 680),
        background_color="#0B1120",
    )
    # webview.start(debug=True)
    webview.start(debug=False)


if __name__ == "__main__":
    main()
