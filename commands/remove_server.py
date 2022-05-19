# -*- coding: utf-8 -*-
from discord import Message
from discord.ext import commands
from modules.db import Servers
from modules.logging import logger
from modules.utils import is_valid_ip, raw_ip


# Remove server command
class RemoveServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, aliases=['r'], ignore_extra=True)
    async def remove(self, ctx: Message, addr_raw: str):
        """Remove server from database"""
        await ctx.message.delete()
        if not await is_valid_ip(addr_raw):
            return ctx.send(":warning: You’ve provided malformed IP address.")
        ip, port = await raw_ip(addr_raw)
        instance = await Servers.filter(ip=ip, port=port, channel=ctx.channel.id, worked=True).first()
        if instance is None:
            return await ctx.send(":warning: Server is not in database.")
        else:
            await Servers.filter(id=instance.id).update(worked=False)
            message = await ctx.channel.fetch_message(instance.message)
            await message.delete()
            await ctx.send(":white_check_mark: Server removed.")
            logger.info(f"{ctx.author.name}#{ctx.author.discriminator} removed server {addr_raw} in #{ctx.channel.name}, {ctx.guild.name}")

def setup(bot: commands.Bot):
    bot.add_cog(RemoveServer(bot))
