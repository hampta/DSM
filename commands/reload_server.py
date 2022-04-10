# -*- coding: utf-8 -*-
import logging

from discord import RawReactionActionEvent
from discord.ext import commands
from discord.errors import NotFound, Forbidden

from modules.utils import get_server_info, embed_generator, stop_server
from modules.db import Servers

class ReloadServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.member != self.bot.user and str(payload.emoji) == "🔄":
            instance = await Servers.filter(message=payload.message_id, worked=True).first()
            if instance is not None:
                channel = self.bot.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction(payload.emoji, payload.member)
                try:
                    instance = await Servers.filter(message=payload.message_id).first()
                    info = await get_server_info(instance.ip, instance.port)
                    em = await embed_generator(info[0], info[1], instance)
                    await msg.edit(embed=em)
                except (NotFound, Forbidden):
                    await stop_server(instance)
                self.logger.info(f"{payload.member} reloaded server {instance.ip}:{instance.port} in #{channel}, {msg.guild.name}")

def setup(bot):
    bot.add_cog(ReloadServer(bot))
