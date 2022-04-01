from logging import Handler, LogRecord
import aiohttp
import asyncio

# custom logger handler
class DiscordWebHookHandler(Handler):
    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record: LogRecord):
        # send record to discord webhook
        asyncio.create_task(self.request(record))

    async def request(self, record: LogRecord):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, data={"content": self.format(record)}):
                pass