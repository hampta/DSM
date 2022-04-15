# -*- coding: utf-8 -*-
import asyncio
import logging

import aiohttp.client_exceptions
from discord import Activity, ActivityType
from discord.errors import Forbidden, NotFound
from discord.ext import commands, tasks
from modules.db import Servers
from modules.utils import embed_generator, get_server_info, stop_server


class ServersCron(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.crontab.start()
        self.logger.info("Cron started")

    @tasks.loop(minutes=1, reconnect=True)
    async def crontab(self):
        await self.bot.wait_until_ready()
        channels = await Servers.filter(worked=True).group_by("channel").values_list("channel", flat=True)
        for channel_id in channels:
            asyncio.create_task(self.for_channels(channel_id))
        servers_count = await Servers.filter(worked=True).count()
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching,
                                                         name=f"{servers_count} game servers"))

    async def for_channels(self, channel_id, sleep=.5):
        servers_ids = await Servers.filter(channel=channel_id, worked=True).values_list("id", flat=True)
        channel = self.bot.get_channel(channel_id)
        if len(servers_ids) > 3:
            sleep = 6
        for id in servers_ids:
            await self.for_id(channel, id)
            await asyncio.sleep(sleep)

    async def for_id(self, channel, id):
        instance = await Servers.filter(id=id).first()
        server_info, players = await get_server_info(instance.ip, instance.port)
        if server_info:
            await Servers.filter(id=id).update(name=server_info.server_name, game=server_info.game)
        try:
            msg = await channel.fetch_message(instance.message)
            embed = await embed_generator(server_info, players, instance)
            await msg.edit(embed=embed)
        except (NotFound, Forbidden):
            user = await self.bot.fetch_user(instance.author)
            await user.send(f"Server {instance.ip}:{instance.port} in channel <#{instance.channel}> is off if you not delete bot message, check bot permissions")
            await stop_server(id)


def setup(bot: commands.Bot):
    bot.add_cog(ServersCron(bot))
