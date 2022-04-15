# -*- coding: utf-8 -*-
import logging

from discord import Embed, Message, errors
from discord.ext import commands
from modules.db import Servers
from modules.utils import is_valid_ip, raw_ip


# Add server command
class AddServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, aliases=['a'], ignore_extra=True)
    async def add(self, ctx: Message, addr_raw: str):
        """Add server to database"""
        try:
            await ctx.message.delete()
            if await is_valid_ip(addr_raw):
                addr = await raw_ip(addr_raw)
                emb = Embed(title="Please wait...",
                                    description="About 1 minute", colour=0xFFFF00)
                mes = await ctx.send(embed=emb)
                await Servers.create(channel=ctx.channel.id, message=mes.id, author=ctx.author.id, ip=addr[0], port=addr[1])
                await mes.add_reaction("🔄")
                self.logger.info(f"{ctx.author.name}#{ctx.author.discriminator} added server {addr_raw} in #{ctx.channel.name}, {ctx.guild.name}")
            else:
                await ctx.send(":warning: You’ve provided malformed IP address.")
        # Cringy exception handling, rewrite later
        except errors.Forbidden:
            user = await self.bot.fetch_user(ctx.author.id)
            await user.send(":warning: I don’t have permission to send/delete messages in this channel.")

def setup(bot: commands.Bot):
    bot.add_cog(AddServer(bot))