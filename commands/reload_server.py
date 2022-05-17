# -*- coding: utf-8 -*-
import logging

from discord import RawReactionActionEvent
from discord.ext import commands
from discord.errors import NotFound, Forbidden

from modules.utils import get_server_info, embed_generator, stop_server, start_server
from modules.db import Servers

class ReloadServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if not (payload.member != self.bot.user and str(payload.emoji) == "🔄"):
            return
        instance = await Servers.filter(message=payload.message_id).first()

        if not instance.worked:
            await start_server(instance.id)
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        await msg.remove_reaction(payload.emoji, payload.member)
        instance = await Servers.filter(message=payload.message_id).first()
        info = await get_server_info(instance.ip, instance.port)
        em = await embed_generator(info[0], info[1], instance)
        await msg.edit(embed=em)
        self.logger.info(f"{payload.member} reloaded server {instance.ip}:{instance.port} in #{channel}, {msg.guild.name}")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, Forbidden):
            return await ctx.send("I don't have permission to edit messages in this channel.\n"
                            "Please give me permission to edit messages in this channel.\n"
                            "To resume the server, react with 🔄")
        elif isinstance(error, NotFound):
            return await ctx.send("Server has been deleted")
        await stop_server(ctx.message.id)
        self.logger.error(f"{ctx.author} error: {error}")

def setup(bot: commands.Bot):
    bot.add_cog(ReloadServer(bot))
