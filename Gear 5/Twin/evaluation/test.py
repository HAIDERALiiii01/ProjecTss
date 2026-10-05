import json
from pathlib import Path
from pydantic import BaseModel, Field

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestQuestion(BaseModel):
    """A test question with expected keywords and reference answer."""

    question: str = Field(description="The question to ask the twin")
    keywords: list[str] = Field(
        default_factory=list,
        description=(
            "Keywords that must appear word-for-word in the retrieved chunks. "
            "Leave empty for unanswerable / off-topic questions (they are skipped in retrieval metrics)."
        ),
    )
    reference_answer: str = Field(
        description="The reference answer. For unanswerable questions, say the information is not available."
    )
    category: str = Field(
        description=(
            "Question category, e.g. direct_fact, project_detail, spanning, follow_up, unanswerable, off_topic"
        )
    )
    history: list[dict] = Field(
        default_factory=list,
        description=(
            "Optional earlier turns for follow-up questions, as "
            '[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]'
        ),
    )


def load_tests(path: str = TEST_FILE) -> list[TestQuestion]:
    """Load test questions from a JSONL file (one JSON object per line, blank lines ignored)."""
    tests = []
    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                tests.append(TestQuestion(**json.loads(line)))
            except Exception as e:
                raise ValueError(f"Bad test on line {line_number} of {path}: {e}") from e
    return tests