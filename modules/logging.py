from logging import Handler, LogRecord
from discord import Webhook, RequestsWebhookAdapter
from aiohttp import client_exceptions


# custom logger handler
class DiscordWebHookHandler(Handler):
    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url
        self.webhook = Webhook.from_url(
            self.webhook_url, adapter=RequestsWebhookAdapter())

    def emit(self, record: LogRecord):
        # send record to discord webhook
        if record.msg.find("is rate limited") != -1:
            return
        try:
            self.webhook.send(self.format(record), username='Logs')
        except (client_exceptions.ClientOSError, ConnectionError, client_exceptions.ClientConnectorError):
            print("Discord webhook connection error")
