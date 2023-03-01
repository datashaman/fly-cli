import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, token):
        self.token = token

    @property
    def client(self):
        return WebClient(token=self.token)

    def send_message(self, text: str, channel: str = 'random'):
        return self.client.chat_postMessage(text=text, channel=channel)
