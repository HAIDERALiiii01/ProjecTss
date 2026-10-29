from pydantic import BaseModel, Field
from agents import Agent
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query and research summaries gathered from web searches.

Write a comprehensive, well-organized report that answers the query.

Requirements:
- Format: markdown, 1,500-3,000 words.
- Structure: a title, a short executive summary, body sections organized by theme (not by search result),
  and a conclusion.
- Use only information from the provided research. Do not pad with unsupported claims. If the research
  does not cover something important, say so briefly instead of guessing.
- Preserve source links from the research and cite them inline next to the claims they support.
  Never invent or alter URLs.
- Where sources conflict, note the disagreement rather than picking one silently.

Also provide:
- short_summary: a 2-3 sentence summary of the key findings.
- follow_up_questions: suggested topics worth researching further.
"""

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(name="Writer Agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=ReportData)
