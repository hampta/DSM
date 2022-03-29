# -*- coding: utf-8 -*-
import logging

from asyncio import sleep
from aiohttp.client_exceptions import ClientOSError, ServerDisconnectedError
from discord import Activity, ActivityType
from discord.errors import DiscordServerError, Forbidden, NotFound
from discord.ext import commands, tasks
from modules.db import Servers, init
from modules.utils import embed_generator, get_server_info, stop_server


class ServersCron(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.crontab.start()

    @tasks.loop(minutes=1, reconnect=False)
    async def crontab(self, online=0):
        await self.bot.wait_until_ready()
        self.logger.info("Cron started")
        servers_id = await Servers.filter(worked=True).values_list("id", flat=True)
        for id in servers_id:
            instance = await Servers.filter(id=id).first()
            info = await get_server_info(instance.ip, instance.port)
            em = await embed_generator(info[0], info[1], instance.ip, instance.port, instance.name, instance.game)
            if info[1]:
                online += info[0].player_count - info[0].bot_count
                await Servers.filter(id=id).update(name=info[0].server_name, game=info[0].game)
            try:
                channel = self.bot.get_channel(instance.channel)
                msg = await channel.fetch_message(instance.message)
                await msg.edit(embed=em)
                await msg.add_reaction("🔄")
            except (NotFound, Forbidden):
                await stop_server(instance)
            # FUCK DISCORD
            except (DiscordServerError, ClientOSError, ServerDisconnectedError):
                self.logger.info("discord shitty")
            await sleep(.5) # temp rate limit fix
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name=f"{len(servers_id)} game servers | Online: {online}"))


def setup(bot):
    bot.add_cog(ServersCron(bot))
