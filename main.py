# -*- coding: utf-8 -*-
import asyncio
import logging
import platform
import os

import discord
from discord.ext import commands

from config import ADMIN_ID, COMMAND_PREFIX, TOKEN, WEBHOOK_URL
from modules.db import init
from modules.logging import DiscordWebHookHandler


# add logger which is sent to discord channel
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M'))
discord_handler = DiscordWebHookHandler(WEBHOOK_URL)
discord_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M'))
logger.addHandler(discord_handler)
logger.addHandler(console_handler)

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command('help')
bot.owner_id = ADMIN_ID

# Setting up asyncio to use uvloop if possible, a faster implementation on the event loop
if platform.system() == "Linux":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass
    import uvloop


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
bot.run(TOKEN)
