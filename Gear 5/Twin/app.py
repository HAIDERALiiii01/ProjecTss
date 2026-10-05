import gradio as gr
from pro_implementation.answer import answer_question
from styles import CSS, JS, EXAMPLES


def chat(message, history):
    answer, _ = answer_question(message, history)  # notify=True: real ntfy alerts in production
    return answer


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())