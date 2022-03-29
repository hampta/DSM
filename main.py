# -*- coding: utf-8 -*-
import logging
from os import listdir

from discord.ext import commands

from modules.logging import DiscordWebHookHandler
from modules.db import init
from config import TOKEN, WEBHOOK_URL, COMMAND_PREFIX, ADMIN_ID

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command('help')
bot.owner_id = ADMIN_ID


# add logger which is sent to discord channel
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] | %(message)s', datefmt='%d-%m-%Y %H:%M'))
discord_handler = DiscordWebHookHandler(WEBHOOK_URL)
discord_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] | %(message)s', datefmt='%d-%m-%Y %H:%M'))
logger.addHandler(discord_handler)
logger.addHandler(console_handler)

@bot.event
async def on_ready():
    # init db
    await init()
    logger.info("Starting bot...")
    # load commands
    for filename in listdir("./commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[:-3]}")
            logger.info(f"Loaded {filename[:-3]}")
    logger.info('Logged in as {0}'.format(bot.user.name))
    logger.info('Bot is ready')
    logger.info('----------------------------------------')


# start bot
bot.run(TOKEN)
