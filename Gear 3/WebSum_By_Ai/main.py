import os
from openai import OpenAI
from dotenv import load_dotenv
from selenium_scrape import Swebsite

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()
        
system_prompt = "You are an assistant that analyzes the contents of a website" \
"and provides short summary, ignoring text that might be navigation related."

def user_prompt_for(url):
    Swebsite(url)
    user_prompt = """
The title and contents of this website are as follows;
please provide a short summary of this website.
The output should be nicely formatted, so that it can be printed.
If it includes news or announcements, then summarize it too\n\n
"""
    with open("data.txt", "r", encoding="utf-8") as f:
        user_prompt += "\n" + f.read()
    return user_prompt


def messages_for(url):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(url)}
    ]

def summarize(url):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages_for(url) # type: ignore
        )
    return response.choices[0].message.content

print(summarize("https://store.epicgames.com/en-US"))


