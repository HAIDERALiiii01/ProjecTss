import os 
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import gradio as gr

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GOOGLE_API_KEY')


MODEL = 'gpt-4o-mini'
openai = OpenAI()
genai.configure(api_key=gemini_api_key) # type: ignore

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):

        self.url = url
        response = requests.get(url=url, headers=headers)
        self.body = response.content

        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator='\n', strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')] # type: ignore
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage-title:\n{self.title}\nWebpage-contents:\n{self.text}"

# ed = Website("https://edwarddonner.com")
# print(ed.get_content())
# print(ed.links)

link_system_prompt = "You are provided with a list of links found on a webpage." \
"You are able to decide which of the links would be most relevant to inlcude in a brochure about the company," \
"such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should response in json as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://full.url/goes/here/careers"}

    ]
}
"""

# print(link_system_prompt)

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. "
    user_prompt += "Do not include Terms of service, Privacy, email links.\n"
    user_prompt += "Links (some might be relevant links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

# print(get_links_user_prompt(ed))

def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format= {"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result) # type: ignore

# huggingface = Website("https://huggingface.co")
# print(huggingface.links)
# print(get_links("https://huggingface.co"))

def get_all_details(url):
    result = "Landing page.\n"
    result += Website(url).get_contents()
    links = get_links(url)
    # print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link['url']).get_contents()
    return result

# print(get_all_details("https://huggingface.co"))

system_prompt = (
"You are an assistant that analyzes the contents of a company website landing page \
and creates a short brochure about the company for prospective customers, \
investors and recruits. Respond in markdown."
)


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at the company name called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company. Respond in Markdown.\n"
    user_prompt += get_all_details(url)
    # user_prompt = user_prompt[:5000]
    return user_prompt

# get_brochure_user_prompt("HuggingFace", "https://huggingface.co")

def gpt_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def gemini_brochure(company_name, url):
    model = genai.GenerativeModel( # type: ignore
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt
    )
    stream = model.generate_content(get_brochure_user_prompt(company_name, url), stream=True)
    result = ""
    for chunk in stream:
        result += chunk.text or ""
        yield result

def stream_model(company_name, url, model):
    if model == "GPT":
        result = gpt_brochure(company_name, url)
    elif model == "GEMINI":
        result = gemini_brochure(company_name, url)
    else:
        raise ValueError("Unknown model!")
    yield from result

view = gr.Interface(
    fn=stream_model,
    inputs=[
        gr.Textbox(label="Company_name here:"),
        gr.Textbox(label="Landing page URL including http:// or https://"),
        gr.Dropdown(["GPT", "GEMINI"], label="Select model"),
    ],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)
view.launch()

