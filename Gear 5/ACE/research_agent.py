from agents import Agent, ModelSettings
from planner_agent import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent
from email_agent import email_agent

MODEL_NAME = "gpt-4o-mini"  # use whatever you use elsewhere

INSTRUCTIONS = """You are a deep research assistant. Given a query, follow this process:
1. Call plan_searches with the query to get a list of searches.
2. Call web_search once for EACH planned search, all in parallel. Pass the input as
   'Search term: <query>\\nReason for searching: <reason>'.
3. Call write_report with the original query and all the search summaries.
4. Call send_email with the markdown report from the writer.
5. Reply with the full markdown report as your final answer.
Never skip a step, and never write the report yourself."""

research_agent = Agent(
    name="Research Agent",
    instructions=INSTRUCTIONS,
    tools=[
        planner_agent.as_tool(
            tool_name="plan_searches",
            tool_description="Plan web searches for a research query. Input: the query.",
        ),
        search_agent.as_tool(
            tool_name="web_search",
            tool_description="Run ONE web search and return a summary. Input: 'Search term: ...\\nReason for searching: ...'",
        ),
        writer_agent.as_tool(
            tool_name="write_report",
            tool_description="Write the report. Input: the original query plus all summarized search results.",
        ),
        email_agent.as_tool(
            tool_name="send_email",
            tool_description="email the markdown report. Input: the full markdown report.",
        ),
    ],
    model=MODEL_NAME,
    model_settings=ModelSettings(parallel_tool_calls=True),
)