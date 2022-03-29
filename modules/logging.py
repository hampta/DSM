from logging import Handler, LogRecord
import requests

# custom logger handler
class DiscordWebHookHandler(Handler):
    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record: LogRecord):
        # send record to discord webhook
        requests.post(self.webhook_url, json={"content": self.format(record)})