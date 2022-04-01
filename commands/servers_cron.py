# -*- coding: utf-8 -*-
import logging


from discord import Activity, ActivityType
from discord.errors import Forbidden, NotFound
from discord.ext import commands, tasks
from modules.db import Servers
from modules.utils import embed_generator, get_server_info, stop_server
import asyncio

class ServersCron(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.crontab.start()
        self.logger.info("Cron started")

    @tasks.loop(minutes=1, reconnect=False)
    async def crontab(self):
        await self.bot.wait_until_ready()
        channels = await Servers.filter(worked=True).group_by("channel").values_list("channel", flat=True)
        for channel_id in channels:
            await self.for_channels(channel_id)

    @crontab.before_loop
    async def before_crontab(self):
        self.online = 0

    @crontab.after_loop
    async def after_crontab(self):
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching,
                                                         name=f"{len(self.servers_ids)} game servers | Online: {self.online}"))

    async def for_channels(self, channel_id, i=0):
        self.servers_ids = await Servers.filter(channel=channel_id, worked=True).values_list("id", flat=True)
        channel = self.bot.get_channel(channel_id)
        for id in self.servers_ids:
            # Rate limit crutch
            if i == 3:
                await asyncio.sleep(15)
                i = 0
            await asyncio.create_task(self.for_id(channel, id))
            i += 1

    async def for_id(self, channel, id):
        self.instance = await Servers.filter(id=id).first()
        server_info, players = await get_server_info(self.instance.ip, self.instance.port)
        if server_info:
            await Servers.filter(id=id).update(name=server_info.server_name, game=server_info.game)
        if players:
            self.online += server_info.player_count - server_info.bot_count
        try:
            msg = await channel.fetch_message(self.instance.message)
            embed = await embed_generator(server_info, players, self.instance)
            await msg.edit(embed=embed)
        except (NotFound, Forbidden):
            await stop_server(id)

def setup(bot):
    bot.add_cog(ServersCron(bot))
