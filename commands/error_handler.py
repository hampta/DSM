import contextlib
import socket
import sys
import traceback

import discord
from aiohttp.client_exceptions import (ClientConnectorError, ClientOSError,
                                       ServerDisconnectedError)
from discord.errors import DiscordServerError
from discord.ext import commands
from modules.logging import logger


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        if cog := ctx.cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, DiscordServerError, ClientOSError,
                   ServerDisconnectedError, ClientConnectorError, socket.gaierror, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            with contextlib.suppress(discord.HTTPException):
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, DiscordServerError):
            print(f'Discord Server Error: {error}')

        else:
            logger.error(f'Ignoring exception in command {error}:')
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
