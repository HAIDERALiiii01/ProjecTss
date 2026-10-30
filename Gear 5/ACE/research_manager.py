import json
from agents import Runner, trace, gen_trace_id
from research_agent import research_agent

class ResearchManager:

    async def run(self, query: str):
        """Run the research agent, yielding status updates and finally the report."""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"Starting research. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            result = Runner.run_streamed(research_agent, f"Query: {query}", max_turns=20)
            call_names = {}  # call_id -> tool name

            async for event in result.stream_events():
                if event.type != "run_item_stream_event":
                    continue

                raw = event.item.raw_item

                if event.name == "tool_called":
                    call_names[raw.call_id] = raw.name
                    yield self._called_email(raw.name, raw.arguments)

                elif event.name == "tool_output":
                    call_id = raw["call_id"] if isinstance(raw, dict) else raw.call_id
                    yield self._done_email(call_names.get(call_id, "tool"))

            yield result.final_output

    def _called_email(self, name: str, arguments: str) -> str:
        if name == "plan_searches":
            return "Planning searches..."
        if name == "web_search":
            try:
                term = json.loads(arguments).get("input", "")
                term = term.split("\n")[0]  # "Search term: ..." line only
            except Exception:
                term = ""
            return f"Searching... {term}"
        if name == "write_report":
            return "Writing report..."
        if name == "send_email":
            return "Sending email..."
        return f"Calling {name}..."

    def _done_email(self, name: str) -> str:
        return {
            "plan_searches": "Searches planned",
            "web_search": "A search finished",
            "write_report": "Report written",
            "send_email": "email sent, research complete",
        }.get(name, f"{name} finished")