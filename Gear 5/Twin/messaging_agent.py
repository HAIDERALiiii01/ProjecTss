import os
from agents.deals import Opportunity
from agents.agent import Agent
from litellm import completion
import requests


class MessagingAgent(Agent):
    name = "Messaging Agent"
    color = Agent.WHITE
    MODEL = "gpt-5-mini"

    def __init__(self):
        """
        Set up this object to either do push notifications via ntfy,
        or SMS via Twilio,
        whichever is specified in the constants
        """
        self.log("Messaging Agent is initializing")
        self.ntfy_topic = os.getenv("NTFY_TOPIC", "your-ntfy-topic-if-not-using-env")
        self.ntfy_url = f"https://ntfy.sh/{self.ntfy_topic}"
        self.log("Messaging Agent has initialized ntfy and GPT-5-mini")

    def push(self, text):
        """
        Send a Push Notification using the ntfy API
        """
        self.log("Messaging Agent is sending a push notification")
        requests.post(
            self.ntfy_url,
            data=text.encode("utf-8"),
            headers={
                "Title": "Deal Alert",
                "Priority": "high",
                "Tags": "moneybag",
            },
        )

    def alert(self, opportunity: Opportunity):
        """
        Make an alert about the specified Opportunity
        """
        text = f"Deal Alert! Price=${opportunity.deal.price:.2f}, "
        text += f"Estimate=${opportunity.estimate:.2f}, "
        text += f"Discount=${opportunity.discount:.2f} :"
        text += opportunity.deal.product_description[:10] + "... "
        text += opportunity.deal.url
        self.push(text)
        self.log("Messaging Agent has completed")

    def craft_message(
        self, description: str, deal_price: float, estimated_true_value: float
    ) -> str:
        user_prompt = "Please summarize this great deal in 2-3 sentences to be sent as an exciting push notification alerting the user about this deal.\n"
        user_prompt += f"Item Description: {description}\nOffered Price: {deal_price}\nEstimated true value: {estimated_true_value}"
        user_prompt += "\n\nRespond only with the 2-3 sentence message which will be used to alert & excite the user about this deal"
        response = completion(
            model=self.MODEL,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    def notify(self, description: str, deal_price: float, estimated_true_value: float, url: str):
        """
        Make an alert about the specified details
        """
        self.log("Messaging Agent is using GPT-5-mini to craft the message")
        text = self.craft_message(description, deal_price, estimated_true_value)
        self.push(text[:200] + "... " + url)
        self.log("Messaging Agent has completed")