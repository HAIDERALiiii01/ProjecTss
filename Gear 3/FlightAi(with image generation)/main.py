import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import base64
from io import BytesIO
from PIL import Image
from IPython.display import Audio, display

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()

system_message = "You are a helpful assistant for an Airline called FlightAI."
system_message += "Give short, courteous answers, no more than one sentence."
system_message += "Always be accurate. If you don't know the answer, say so."

ticket_prices = {"tokyo": "$800", "new york": "$600", "london": "$500", "paris": "$450"}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}.")
    city = destination_city.lower()
    price = ticket_prices.get(city, "unknown")
    return price

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

def artist(city):
    image_response = openai.images.generate(
        model = "dall-e-3",
        prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
        size="1024x1024",
        n=1,
        response_format="b64_json"
    )
    image_base64 = image_response.data[0].b64_json # type: ignore
    image_data = base64.b64decode(image_base64) # type: ignore
    return Image.open(BytesIO(image_data))

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools) # type: ignore
    image = None

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        image = artist(city)
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    
    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]

    return history, image

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages")
        image_output = gr.Image(height=500)
    with gr.Row():
        entry = gr.Textbox(label="Chat with our Ai Assistant:")
    with gr.Row():
        clear = gr.Button("Clear")
    
    def do_entry(message, history):
        history += [{"role": "user", "content": message}]
        return "", history
    
    
    entry.submit(do_entry, inputs=[entry, chatbot], outputs=[entry, chatbot]).then(
    chat, inputs=[entry, chatbot], outputs=[chatbot, image_output]
)

    clear.click(lambda: None, inputs=None, outputs=chatbot, queue=False)

ui.launch(inbrowser=True)