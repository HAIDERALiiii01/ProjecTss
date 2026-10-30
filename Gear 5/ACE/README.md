# 🕵️ Ace Ventura: The Digital Detective

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDM2azVweGZwZGIwZ2V5bG91MHIyaHhiNGFneDJxY3U2MXJyZGJkNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/fSSbirL3Ew0zC/giphy.gif" alt="Ace Ventura — The Digital Detective" width="600"/>
</p>

<p align="center">
  <strong>A multi-agent AI research detective that investigates a question, gathers web evidence, writes a structured report, and emails the finished investigation.</strong>
</p>

<p align="center">
  Built with Python · Gradio · OpenAI Agents SDK · Web Search · Pydantic
</p>

---

## 🎯 What it does

Most search tools give you a list of links and leave the investigation to you. **Ace Ventura: The Digital Detective** takes a more agentic approach: it breaks a research question into smaller searches, investigates them, combines the findings into a report, and sends that report by email.

Give Ace a case, for example:

- What are the latest developments in agentic AI?
- Compare the leading open-source LLMs and their trade-offs.
- How is AI being used in healthcare?
- What changed in Python across recent releases?

The research workflow is coordinated by a main **Research Agent**, which delegates specialized tasks to other agents.

> **The detective's rule:** personality makes the investigation more enjoyable, but evidence and accuracy come first.

---

## 🧠 How it works

```text
                    User's research query
                              |
                              v
                       Gradio interface
                              |
                              v
                       Research Manager
                              |
                              v
                        Research Agent
                              |
                              v
                        Planner Agent
                    Creates search queries
                              |
                              v
                Search Agent calls (parallel)
                 Web search for each query
                              |
                              v
                         Writer Agent
                 Produces a structured report
                              |
                              v
                         Email Agent
                    Sends the full report
                              |
                              v
                  Report displayed in Gradio
```

### Investigation steps

1. **Plan the investigation** — The Planner Agent turns the original question into focused web searches. Each search is paired with a reason explaining what it should uncover.
2. **Search the web** — The Research Agent calls the Search Agent once for every planned search. Parallel tool calls are enabled, so independent searches can run concurrently.
3. **Write the report** — The Writer Agent combines the search summaries into one report. It is instructed to organize findings by topic, explain uncertainty or conflicting evidence, and avoid inventing unsupported details.
4. **Email the report** — The Email Agent prepares plain-text and HTML versions of the report and sends them through the configured email function.
5. **Show the result** — The Research Manager streams progress messages to the Gradio interface and displays the final report when the run finishes.

---

## 🤖 The agents

| Agent | Responsibility |
|---|---|
| **Research Agent** | Coordinates the investigation and calls the other agents as tools. |
| **Planner Agent** | Creates a list of focused searches for the original query. |
| **Search Agent** | Uses the OpenAI Agents SDK `WebSearchTool` to research one search term and return a concise summary in Ace's voice. |
| **Writer Agent** | Turns the collected summaries into a structured Markdown report and returns a Pydantic `ReportData` object. |
| **Email Agent** | Sends the report as both plain text and HTML using the email tool. |

### Structured report output

The Writer Agent uses Pydantic to define the shape of its result:

```python
class ReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: list[str]
```

This separates the full report from its short summary and suggested follow-up investigations.

---

## ✨ Features

- **Multi-agent orchestration** — Specialized agents handle planning, searching, writing, and emailing.
- **Parallel research** — The Research Agent is configured with `parallel_tool_calls=True` so planned searches can be dispatched concurrently.
- **Live progress updates** — The Gradio interface receives status messages as agent tools are called and completed.
- **Research reports** — The Writer Agent is instructed to produce a title, executive summary, thematic sections, and a conclusion.
- **Email delivery** — The Email Agent prepares both plain-text and HTML email bodies.
- **OpenAI tracing** — Each investigation is wrapped in an Agents SDK trace, and the UI displays a link to that trace.
- **Ace Ventura personality** — Search summaries and the final report use a playful detective voice without sacrificing factual accuracy.

---

## 📁 Project structure

```text
Ace-Ventura/
│
├── assets/
│   └── ace-ventura.png       # Optional project logo/image used in the README
│
├── app.py                    # Gradio interface and event handlers
├── research_manager.py       # Runs the investigation and streams status updates
├── research_agent.py         # Main agent and its specialist-agent tools
├── planner_agent.py          # Plans the web searches
├── search_agent.py           # Performs web searches
├── writer_agent.py           # Produces the structured research report
├── email_agent.py            # Sends the report by email
├── messenger.py              # SMTP/email delivery implementation
├── styles.py                 # Gradio CSS, JavaScript, examples, and header HTML
├── requirements.txt          # Python dependencies
├── .env                      # Local environment variables (do not commit)
└── README.md
```

| File | Purpose |
|---|---|
| `app.py` | Builds the Gradio interface, accepts a query, and displays streamed updates and the final report. |
| `research_manager.py` | Runs the main agent inside a trace and translates tool-call events into readable progress messages. |
| `research_agent.py` | Defines the orchestrator and exposes the specialist agents as tools. |
| `planner_agent.py` | Defines the agent that creates the investigation's search plan. |
| `search_agent.py` | Uses `WebSearchTool` to research an individual search term. |
| `writer_agent.py` | Defines the Pydantic report schema and generates the final report. |
| `email_agent.py` | Uses the email-sending tool to deliver the report. |
| `messenger.py` | Implements the actual email delivery. Its configuration must match the environment variables you use. |
| `styles.py` | Supplies `CSS`, `JS`, `EXAMPLES`, and `HEADER_HTML` to the Gradio app. |

---

## ⚙️ Requirements

- Python 3.10 or newer (use the version supported by your installed OpenAI Agents SDK and dependencies).
- An OpenAI API key with access to the models you configure.
- SMTP credentials for the mailbox used to send reports.
- The Python packages used by the project, including:
  - `openai-agents`
  - `gradio`
  - `python-dotenv`
  - `pydantic`

Your `requirements.txt` should include these packages and any additional dependencies imported by `messenger.py` and `styles.py`.

---

## 🚀 Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the URL and folder name with your repository details.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. At minimum, configure the OpenAI API key and the model name used by agents that read `DEFAULT_MODEL_NAME`.

```env
OPENAI_API_KEY=your_openai_api_key
DEFAULT_MODEL_NAME=gpt-5.4-mini

# Email settings — use the exact names expected by messenger.py
EMAIL_ADDRESS=your_email@example.com
EMAIL_SMTP_SERVER=your_smtp_server
EMAIL_APP_PASSWORD=your_email_app_password
```

The email variable names above must match the implementation in `messenger.py`. For Gmail SMTP, use an app password where required; do not put your normal account password in the project.

> **Keep secrets private.** Never commit `.env`, API keys, SMTP passwords, or other credentials.

### 5. Start the application

```bash
python app.py
```

Open the local Gradio URL printed in the terminal, enter a research question, and select **Investigate!**

---

## 🔍 Tracing and progress updates

The `ResearchManager` wraps each run in an OpenAI Agents SDK trace:

```python
trace_id = gen_trace_id()

with trace("Research trace", trace_id=trace_id):
    ...
```

The app first displays a trace link, then listens to streamed run events. It uses `tool_called` and `tool_output` events to show progress such as:

- Planning searches...
- Searching... *[search term]*
- A search finished
- Writing report...
- Sending email...
- Email sent, research complete

The trace link is useful for inspecting the agent run and understanding which tools were called. Keep in mind that the trace is an observability view; it is not itself the research report.

---

## 🎨 Customize Ace

### 1. Change the detective's personality

Edit the instructions in `search_agent.py` and `writer_agent.py`.

- Keep the Search Agent concise: its job is to report relevant findings, not write the final report.
- Keep the Writer Agent evidence-led: it should use the supplied research summaries, acknowledge gaps, and explain disagreements.
- Use humor selectively. The final output should remain useful as a research document.

### 2. Change the models

The specialist agents read `DEFAULT_MODEL_NAME` from the environment, with a fallback in their Python files. The main Research Agent currently specifies its model directly in `research_agent.py`.

If you want to change models consistently, update the main agent and specialist agents deliberately. Make sure each selected model supports the features used by its agent, including tool calling and structured output where applicable.

### 3. Customize the interface

Edit `styles.py` to change:

- `HEADER_HTML` — the app's header and branding
- `CSS` — layout, colors, spacing, and responsive styling
- `JS` — any client-side behavior
- `EXAMPLES` — suggested investigation prompts

The Gradio layout and event wiring live in `app.py`.

### 4. Customize the report

Edit the Writer Agent's instructions in `writer_agent.py` to adjust the report structure, tone, length, and follow-up questions. The current instructions request a 1,500–3,000-word Markdown report.

---

## 🧭 Possible next improvements

- Add a dedicated Planner Agent with a structured Pydantic output for planned searches and their reasons.
- Display each planned search and its individual status in the Gradio interface.
- Add retry handling for failed web searches and email delivery.
- Add a user-configurable email recipient, with confirmation before sending.
- Preserve investigation history so previous reports can be revisited.
- Add report export options such as Markdown or PDF.
- Add source URLs and citations to the final report, if the search workflow is updated to preserve and pass source references through to the Writer Agent.

---

<p align="center">
  <strong>Case closed. 🕵️</strong>
</p>