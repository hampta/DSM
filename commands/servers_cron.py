# -*- coding: utf-8 -*-
import logging

from aiohttp.client_exceptions import ClientOSError, ServerDisconnectedError
from discord import Activity, ActivityType
from discord.errors import DiscordServerError, Forbidden, NotFound
from discord.ext import commands, tasks
from modules.db import Servers
from modules.utils import embed_generator, get_server_info, stop_server


class ServersCron(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.crontab.start()
        self.logger.info("Cron started")

    @tasks.loop(minutes=1, reconnect=False)
    async def crontab(self, online=0):
        await self.bot.wait_until_ready()
        channels = await Servers.filter(worked=True).group_by("channel").values_list("channel", flat=True)
        for channel_id in channels:
            servers_ids = await Servers.filter(channel=channel_id, worked=True).values_list("id", flat=True)
            channel = self.bot.get_channel(channel_id)
            for id in servers_ids:
                instance = await Servers.filter(id=id).first()
                server_info, players = await get_server_info(instance.ip, instance.port)
                embed = await embed_generator(server_info, players, instance.ip, instance.port, instance.name, instance.game)
                if players:
                    online += server_info.player_count - server_info.bot_count
                    await Servers.filter(id=id).update(name=server_info.server_name, game=server_info.game)
                try:
                    msg = await channel.fetch_message(instance.message)
                    await msg.edit(embed=embed)
                except (NotFound, Forbidden):
                    await stop_server(instance)
                # FUCK DISCORD
                except (DiscordServerError, ClientOSError, ServerDisconnectedError):
                    self.logger.info("discord shitty")
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name=f"{len(servers_ids)} game servers | Online: {online}"))


def setup(bot):
    bot.add_cog(ServersCron(bot))
