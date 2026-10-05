import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ntfy_topic = os.getenv("NTFY_RESUME_KEY")
ntfy_url = f"https://ntfy.sh/{ntfy_topic}" if ntfy_topic else None


def push(text, notification_type):
    if not ntfy_url:
        print("NTFY_RESUME_KEY not set, skipping notification", flush=True)
        return False

    titles = {
        "email": "Resume Agent - New Contact",
        "question": "Resume Agent - Unanswered Question",
    }
    tags = {"email": "email", "question": "question"}

    try:
        response = requests.post(
            ntfy_url,
            data=text[:1000].encode("utf-8"),
            headers={
                "Title": titles[notification_type],
                "Priority": "high",
                "Tags": tags[notification_type],
            },
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"ntfy push failed: {e}", flush=True)
        return False

def record_user_details(email, name="Name not provided", notes="Not provided"):
    ok = push(f"New contact: {name} | {email} | Notes: {notes}", "email")
    return "OK" if ok else "Could not send the notification"


def record_unknown_question(question):
    ok = push(f"Unanswered question: {question}", "question")
    return "OK" if ok else "Could not send the notification"


record_user_details_json = {
    "name": "record_user_details",
    "description": "Record that a visitor wants to get in touch. Only call this after the visitor has actually typed an email address.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Record a visitor's question ONLY when the retrieved knowledge base excerpts contain nothing relevant to it. Do not call this if you can answer the question, even partially.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        print(f"Tool called: {tool_name}", flush=True)
        try:
            arguments = json.loads(tool_call.function.arguments)
            tool = tool_map.get(tool_name)
            result = tool(**arguments) if tool else f"Unknown tool: {tool_name}"
        except Exception as e:
            print(f"Tool {tool_name} failed: {e}", flush=True)
            result = f"Tool error: {e}"
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
