#!/usr/bin/python3
'''
    https://github.com/johnnyapol/discord-role-bot

    License: AGPL v3.0

    Simple role management bot for Discord, works by !add <roleName>
'''

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import logging
import os
import traceback
import json
import string

async def run(bot):
    try:
        await bot.start(os.getenv('DISCORD_BOT_TOKEN'))
    except:
        await bot.logout()
    

class RoleBot(commands.Bot):
    def __init__(self, serverDb):
        super().__init__(
        command_prefix="!",
        case_insensitive=True,
        description="Add roles using !add or list roles using !list")

        self.serverDB = serverDb

    async def on_ready(self):
        pass
    async def on_command_error(self, context, exception):
        await context.send(exception)
        return super().on_command_error(context, exception)

bot = RoleBot({})

@bot.command()
async def add(ctx, role):
    role = role.lower()
    id = ctx.message.guild.id
    if role in bot.serverDB[id]:
        r = ctx.message.guild.get_role(bot.serverDB[id][role])
        await ctx.message.author.add_roles(r)
        await ctx.send("Done!")
    pass

@bot.command()
async def list(ctx):
    '''Lists available roles to add'''
    msg = "Available roles (add using !add <name>):\n"

    table = bot.serverDB[ctx.message.guild.id]
    for role in table:
        msg = msg + ("\t" + role + "\n")
    
    await ctx.send(msg)

@bot.command()
async def reg(ctx, role : discord.Role, name):
    table = None
    id = ctx.message.guild.id
    if id in bot.serverDB:
        table = bot.serverDB[id]
    else:
        table = bot.serverDB[id] = { }

    if (table == None):
        table = bot.serverDB[ctx.message.guild.id] = { }
    
    table[name] = role.id

    await ctx.send("Registered!")

asyncio.get_event_loop().run_until_complete(run(bot))