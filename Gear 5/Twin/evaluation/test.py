import json
from pathlib import Path

from pydantic import BaseModel, Field

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestQuestion(BaseModel):
    """A single evaluation test case for the digital twin."""

    question: str = Field(description="The question a visitor would ask the twin")
    keywords: list[str] = Field(
        default_factory=list,
        description="Diagnostic keywords that should appear in retrieved chunks (empty = unanswerable / off-topic)",
    )
    reference_answer: str = Field(description="Reference answer (first person, as the twin would say it)")
    category: str = Field(description="Question category")
    history: list[dict] = Field(default_factory=list, description="Optional prior chat turns")
    gold_sections: list[list[str]] = Field(
        default_factory=list,
        description='Gold chunks as groups of alternatives, e.g. [["faq.md::Who are you?", "story.md::Who I am"]]. '
        "Each inner list is one information need; retrieving ANY section in it satisfies the need.",
    )


def load_tests(path: str = TEST_FILE) -> list[TestQuestion]:
    """Load test questions from a JSONL file."""
    tests = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tests.append(TestQuestion(**json.loads(line)))
    return tests
