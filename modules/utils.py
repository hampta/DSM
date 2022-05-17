# -*- coding: utf-8 -*-

import asyncio
import datetime
import operator
import logging
import re
from time import gmtime, strftime
from typing import Dict

import a2s
import discord

from modules.db import Servers

# open file and return content
bot_names = open("resources/botnames.txt", "r").read()
bot_names = bot_names.split("\n")
logger = logging.getLogger('discord')

# get ip and port from string
async def raw_ip(r_ip):
    r_ip = r_ip.split(":")
    ip = r_ip[0]
    if len(r_ip) == 1:
        port = 27015
    else:
        port = r_ip[1]
    return (ip, port)

# validate ip
async def is_valid_ip(address: str) -> bool:
    if re.match(r"^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}(:((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{1,5})|([0-9]{1,4})))?$|^$", address):
        return True
    else:
        return False

# get server info from ip
async def get_server_info(ip, port):
    address = (ip, port)
    try:
        info = await a2s.ainfo(address, timeout=5)
        players = await a2s.aplayers(address, timeout=5)
        if info is None:
            raise
        return (info, players)
    except (asyncio.exceptions.TimeoutError, ConnectionRefusedError, OSError):
        return (False, False)
    except a2s.exceptions.BufferExhaustedError:
        return (info, False)

# get max played time
async def max_played(players, max=0.0):
    for player in players:
        if float(player.duration) > max:
            max = float(player.duration)
        else:
            continue
    return max

# embed message generator
async def embed_generator(server_info, players, instance):
    if server_info:
        em = discord.Embed(title=server_info.server_name,
                           description=server_info.game, colour=0x10EE00)
        em.add_field(name="🔌 IP: ", value=f"`{instance.ip}:{instance.port}`", inline=True)
        em.add_field(name="🛰️ Status: ", value="✅ Server online")
        em.add_field(name="🗺️ Map: ", value=server_info.map_name, inline=True)
        if server_info.player_count - server_info.bot_count and players:
            em.add_field(name=f"😎 Players: ",
                         value=server_info.player_count - server_info.bot_count, inline=True)
        else:
            em.add_field(name=f"😎 Players: ", value="0", inline=True)
        em.add_field(name=f"🤖 Bots: ", value=server_info.bot_count, inline=True)
        em.add_field(name=f"🌍 Max Players: ",
                     value=server_info.max_players, inline=True)
        em.add_field(name="👮 VAC: ", value=(
            "✅ Enabled" if server_info.vac_enabled else "🚫 Disabled"), inline=True)
        em.add_field(name="🖥️ Running on: ", value=(
            "🐧 Linux" if server_info.platform == "l" else "🪟 Windows"), inline=True)
        em.add_field(name="🔑 Password: ", value=(
            "🔐 Yes" if server_info.password_protected else "🔓 No"), inline=True)
        if server_info.player_count - server_info.bot_count and players:
            players_ = {x.name: [x.score, x.duration] for x in players}
            players_ = dict(
                sorted(players_.items(), key=operator.itemgetter(1), reverse=True))
            player_names, player_scores, player_played = "", "", ""
            time_max = await max_played(players)
            for n, player_name in enumerate(players_):
                if player_name in bot_names and float(players_[player_name][1]) == time_max:
                    continue
                player_scores += f"{players_[player_name][0]} \n"
                player_played += strftime("%H:%M:%S",
                                          gmtime(players_[player_name][1])) + "\n"
                if len(player_name) > 22:
                    player_name = player_name[:22] + "..."
                if not player_name:
                    player_name = "⏱️ Connecting..."
                player_names += f"{n} - {player_name} \n"
            em.add_field(name="♿ Player list: ",
                         value=f"```{player_names}```", inline=True)
            em.add_field(name="⚔️ Score: ",
                         value=f"```{player_scores}```", inline=True)
            em.add_field(name="⏱️ Time played: ",
                         value=f"```{player_played}```", inline=True)
    else:
        em = discord.Embed(title=instance.name,
                           description=instance.game, colour=0xFF0000)
        em.add_field(name="🔌 IP: ", value=f"`{instance.ip}:{instance.port}`", inline=True)
        em.add_field(name="🛰️ Status: ", value=":no_entry: Server offline")
    em.set_footer(text="Last update",
                  icon_url="https://cdn.discordapp.com/attachments/836638488924782624/941072454674165780/update-icon.png")
    em.timestamp = datetime.datetime.utcnow()
    return em


async def stop_server(message_id):
    logger.info(f"Stopping server {message_id}")
    #logger.info(f"Message {instance.message} deleted in {instance.channel} author - {instance.author} | {instance.ip}:{instance.port}")
    await Servers.filter(message=message_id).update(worked=False)


async def start_server(message_id):
    logger.info(f"Starting server {message_id}")
    await Servers.filter(message=message_id).update(worked=True)