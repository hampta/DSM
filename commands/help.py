# -*- coding: utf-8 -*-
from discord import Embed, User
from discord.ext import commands
from modules.logging import logger


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # help command
    @commands.command(pass_context=True, aliases=['h'], ignore_extra=True)
    async def help(self, ctx):
        """Show help"""
        await ctx.message.delete()
        user: User = await self.bot.fetch_user(ctx.author.id)
        emb = Embed(title="Help", description="", colour=0xFFFF00)
        emb.add_field(name="!add <ip:port>",
                      value="Add server to database", inline=False)
        emb.add_field(name="!remove <ip:port>",
                      value="Remove server from database", inline=False)
        emb.add_field(
            name="!list", value="List all servers in database", inline=False)
        emb.add_field(name="!help", value="Show this message", inline=False)
        emb.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        admin: User = await self.bot.fetch_user(self.bot.owner_id)
        emb.set_footer(text=f"Owner {admin.name}#{admin.discriminator}")
        await user.send(embed=emb)
        logger.info(f"{ctx.author.name}#{ctx.author.discriminator} asked for help in #{ctx.channel.name}, {ctx.guild.name}")

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
