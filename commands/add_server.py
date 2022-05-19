# -*- coding: utf-8 -*-
from discord import Embed, Message, errors
from discord.ext import commands
from modules.db import Servers
from modules.utils import is_valid_ip, get_ip_port
from modules.logging import logger

# Add server command
class AddServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, aliases=['a'], ignore_extra=True)
    async def add(self, ctx: Message, addr_raw: str):
        """Add server to database"""
        await ctx.message.delete()
        if not await is_valid_ip(addr_raw):
            return ctx.send(":warning: You’ve provided malformed IP address.")
        ip, port = await get_ip_port(addr_raw)
        emb = Embed(title="Please wait...",
                            description="About 1 minute", colour=0xFFFF00)
        mes = await ctx.send(embed=emb)
        await Servers.create(channel=ctx.channel.id, message=mes.id, author=ctx.author.id, ip=ip, port=port)
        await mes.add_reaction("🔄")
        logger.info(f"{ctx.author.name}#{ctx.author.discriminator} added server {addr_raw} in #{ctx.channel.name}, {ctx.guild.name}")

    async def cog_command_error(self, ctx: Message, error):
        if isinstance(error, errors.Forbidden):
            user = await self.bot.fetch_user(ctx.author.id)
            await user.send(":warning: I don’t have permission to send/delete messages in this channel.")


def setup(bot: commands.Bot):
    bot.add_cog(AddServer(bot))
