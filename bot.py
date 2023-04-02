import os
from enum import Enum

import discord
from discord import app_commands
from discord.ext import commands, tasks

from utils import *


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is Up and Ready to Go! {bot.user}")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {synced} commands")
        except Exception as e:
            print(e)

    @bot.hybrid_group(fallback="list")
    async def classes(ctx):
        classes = read_class_info()
        header = "Available Classes: \n"
        texts = header
        for index, row in classes.iterrows():
            texts += f"`{row['id']}` - {row['name']} by {row['lecturer']}\n"
        if texts == header:
            texts = "No classes available"
        await ctx.send(texts, ephemeral=True)

    @classes.command()
    async def add(ctx, id: str, name: str, lecturer: str):
        return_message = add_class_info(id, name, lecturer)
        await ctx.send(return_message)

    @classes.command()
    async def remove(ctx, id: str):
        return_message = remove_class_info(id)
        await ctx.send(return_message)

    bot.run(os.getenv("BETTERLEB2_BOT_TOKEN"))
