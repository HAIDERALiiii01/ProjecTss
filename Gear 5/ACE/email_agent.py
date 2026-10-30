from agents import Agent, function_tool, ModelSettings
from messenger import send_email
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

settings = ModelSettings(tool_choice="required")

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Send out an email with the given subject and body
    
    Args:
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email
    """

    send_email(subject, text_body, html_body)
    return "Email sent successfully"


INSTRUCTIONS = """
You are provided with a detailed report. Use your tool to send it as an email.

- Write a concise, descriptive subject line.
- Provide both a plain-text version (text_body) and an HTML version (html_body) of the full report.
- Do not shorten, summarize, or omit any part of the report.
- Keep the HTML clean and simple: use inline styles only (email clients strip <style> blocks),
  clear headings, readable paragraphs, and working links.
"""

email_agent = Agent(name="Email Agent", instructions=INSTRUCTIONS, tools=[send_email_tool], model=MODEL_NAME, model_settings=settings)