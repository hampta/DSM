import logging
from logging import Handler, LogRecord

from aiohttp import client_exceptions
from config import WEBHOOK_URL
from discord import RequestsWebhookAdapter, Webhook


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


# add logger which is sent to discord channel
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M'))
discord_handler = DiscordWebHookHandler(WEBHOOK_URL)
discord_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M'))
logger.addHandler(discord_handler)
logger.addHandler(console_handler)
