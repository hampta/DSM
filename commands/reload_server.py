# -*- coding: utf-8 -*-
from discord import RawReactionActionEvent
from discord.errors import Forbidden, NotFound
from discord.ext import commands
from modules.db import Servers
from modules.logging import logger
from modules.utils import (embed_generator, get_server_info, start_server,
                           stop_server)


class ReloadServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        logger.info(f"{payload.member} reloaded server {instance.ip}:{instance.port} in #{channel}, {msg.guild.name}")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, Forbidden):
            return await ctx.send("I don't have permission to edit messages in this channel.\n"
                            "Please give me permission to edit messages in this channel.\n"
                            "To resume the server, react with 🔄")
        elif isinstance(error, NotFound):
            return await ctx.send("Server has been deleted")
        await stop_server(ctx.message.id)
        logger.error(f"{ctx.author} error: {error}")

def setup(bot: commands.Bot):
    bot.add_cog(ReloadServer(bot))
