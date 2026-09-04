from litellm import completion
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import re

load_dotenv(override=True)

DEFAULT_MODEL_NAME = os.getenv("PRICER_PREPROCESSOR_MODEL", "ollama_chat/llama3.2")

SYSTEM_PROMPT = """You rewrite raw product text into a clean listing.
Do not include part numbers.

Example:
Input: "Sony WH-1000XM5 wireless noise cancelling headphones, bluetooth, 30hr battery"
Output:
{"title": "Sony WH-1000XM5 Wireless Headphones", "category": "Electronics", "brand": "Sony", "description": "Premium wireless headphones offering industry-leading noise cancellation and all-day comfort.", "details": "Features Bluetooth connectivity and up to 30 hours of battery life on a single charge."}"""


class ProductListing(BaseModel):
    title: str
    category: str
    brand: str
    description: str
    details: str


class Preprocessor:
    def __init__(
        self,
        model_name=DEFAULT_MODEL_NAME,
        base_url=None,
    ):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0
        self.model_name = model_name
        self.base_url = base_url
        if "ollama" in model_name and not base_url:
            self.base_url = "http://localhost:11434"

    def messages_for(self, text: str) -> list[dict]:
        return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]

    def preprocess(self, text: str) -> str:
        messages = self.messages_for(text)
        response = completion(
            messages=messages,
            model=self.model_name,
            api_base=self.base_url,
            response_format=ProductListing,
        )
        self.total_input_tokens += response.usage.prompt_tokens
        self.total_output_tokens += response.usage.completion_tokens
        self.total_cost += response._hidden_params["response_cost"]

        raw = response.choices[0].message.content

        # Strip any leading role marker like "### System:", "System:", etc.
        raw = re.sub(r"^\s*#{0,3}\s*(System|Assistant|User)\s*:?\s*", "", raw, flags=re.IGNORECASE)

        try:
            parsed = ProductListing.model_validate_json(raw)
            return (
                f"Title: {parsed.title}\n"
                f"Category: {parsed.category}\n"
                f"Brand: {parsed.brand}\n"
                f"Description: {parsed.description}\n"
                f"Details: {parsed.details}"
            )
        except Exception:
            # Not valid JSON (structured output isn't actually being enforced) — return cleaned raw text
            return raw