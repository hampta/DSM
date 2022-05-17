# -*- coding: utf-8 -*-
import logging

from discord import Message
from discord.ext import commands
from modules.utils import raw_ip, is_valid_ip
from modules.db import Servers

# Remove server command
class RemoveServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

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



def setup(bot: commands.Bot):
    bot.add_cog(RemoveServer(bot))