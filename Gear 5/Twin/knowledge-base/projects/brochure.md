---
type: project
name: AI Brochure Generator
topics: [llm, web-scraping, streaming, gradio, prompt-engineering]
stack: Python, GPT-4o-mini, Gemini 2.0 Flash, BeautifulSoup, Requests, Gradio
---

# AI Brochure Generator: Turn a Company Website into a Brochure

## What the AI Brochure Generator is and why I built it

The AI Brochure Generator is an application I built that takes a company's name and website URL and generates a complete company brochure in Markdown. It scrapes the company's website, uses an LLM to pick the most relevant pages, and then uses GPT-4o-mini or Gemini 2.0 Flash to write the final brochure. I built it to turn a company website into a structured, AI-generated brochure.

I built the interface with Gradio, and the brochure streams live, token by token, as the model writes it.

## How the AI Brochure Generator pipeline works

In the AI Brochure Generator, the workflow is: company URL, then web scraping, then link selection, then relevant page scraping, then LLM generation, then a Markdown brochure.

The steps are: scrape the company's landing page, find the links on it, use GPT to decide which links are useful, scrape those selected pages, combine everything collected, and have the selected LLM generate the brochure.

## Website scraping

In the AI Brochure Generator, I use a `Website` class to fetch and parse the company's landing page. It starts from the URL I enter and extracts the page content and the links. The scraping uses Requests to fetch pages and BeautifulSoup to parse them. This collected content is the source material that the language model later uses to write the brochure.

## Relevant link selection with an LLM

In the AI Brochure Generator, GPT looks at the links found on the landing page and picks the ones most relevant to a company brochure, such as the About page, Careers, and other pages with useful information about the organization. This lets the app go beyond the landing page and gather information from the most useful parts of the site.

## Content collection

In the AI Brochure Generator, once the relevant links are selected, the app visits those pages and collects their content. The model therefore receives information from both the original landing page and the selected pages, which gives it more context about the company before it writes anything.

## Brochure generation and model choice

In the AI Brochure Generator, I can choose between two models from the interface: GPT-4o-mini or Gemini 2.0 Flash. The selected model receives the collected company information and generates the brochure in Markdown, presenting the company's information in a structured and readable way.

The link-selection step always uses GPT, even when I choose Gemini for the final brochure. So an OpenAI API key is needed in both cases, plus a Google API key for Gemini.

## Streaming output

In the AI Brochure Generator, I stream the brochure into the interface instead of waiting for the full result. The text appears token by token as the model produces it, so the generation is visible while the brochure is being created.

## The Gradio interface

In the AI Brochure Generator, I built the interface with Gradio. It has a company name input, a website URL input (the full URL including `https://`), a model-selection dropdown, and a live output area where the Markdown brochure is rendered. The app runs locally in the browser.

## Limitations of the AI Brochure Generator

The AI Brochure Generator depends on the target website being accessible to the scraper. Some websites block automated scraping, so the amount and quality of the information collected, and therefore the brochure, varies from site to site.

## Technologies used in the AI Brochure Generator

- AI and LLM: GPT-4o-mini, Gemini 2.0 Flash
- Web scraping: BeautifulSoup, Requests
- Application: Python, Gradio
- Configuration: python-dotenv, environment variables for API keys

## Links to the AI Brochure Generator

- AI Brochure Generator GitHub: https://github.com/HAIDERALiiii01/ProjecTss/tree/main/Gear%203/Brochure_Generator(Ai_based)
