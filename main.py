# -*- coding: utf-8 -*-
import asyncio
import os
import platform

import discord
from discord.ext import commands

from config import ADMIN_ID, COMMAND_PREFIX, TOKEN
from modules.db import init
from modules.logging import logger

# Setting up asyncio to use uvloop if possible, a faster implementation on the event loop
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logger.info("Linux decected, using uvloop")

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command('help')
bot.owner_id = ADMIN_ID


@bot.event
async def on_ready():
    # init db
    await init()
    logger.info("Starting bot...")
    # load commands
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[:-3]}")
            logger.info(f"Loaded {filename[:-3]}")
    logger.info('----------------------------------------')
    logger.info('Logged in as {0}'.format(bot.user.name))
    logger.info(f"Discord API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(
        f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info('----------------------------------------')
    logger.info('Bot is ready')


# start bot
if __name__ == '__main__':
    bot.run(TOKEN)
