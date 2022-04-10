# -*- coding: utf-8 -*-
import logging

from discord import Embed
from discord.ext import commands
from config import ADMIN_ID


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    # help command
    @commands.command(pass_context=True, aliases=['h'], ignore_extra=True)
    async def help(self, ctx):
        """Show help"""
        await ctx.message.delete()
        user = await self.bot.fetch_user(ctx.author.id)
        emb = Embed(title="Help", description="", colour=0xFFFF00)
        emb.add_field(name="!add <ip:port>",
                      value="Add server to database", inline=False)
        emb.add_field(name="!remove <ip:port>",
                      value="Remove server from database", inline=False)
        emb.add_field(
            name="!list", value="List all servers in database", inline=False)
        emb.add_field(name="!help", value="Show this message", inline=False)
        emb.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        emb.set_footer(text=f"Owner <@{ADMIN_ID}>")
        await user.send(embed=emb)
        self.logger.info(f"{ctx.author.name}#{ctx.author.discriminator} asked for help in #{ctx.channel.name}, {ctx.guild.name}")

def setup(bot):
    bot.add_cog(Help(bot))
