import json
import os
from typing import Optional

import discord
import fire
from discord.ext import commands

from utils import constants


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("/"), intents=discord.Intents().default())

    async def setup_hook(self):
        """
        Loads all cogs and syncs slash commands
        """
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        synced = await self.tree.sync()
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("Slash CMDs Synced", len(synced), "commands")

    def start_locally(self, TOKEN: Optional[str] = None):
        """
        Starts the bot
        """
        if TOKEN is None and os.getenv(constants.TOKEN_NAME) is None:
            # If no token is provided, and no token is found in the environment variables.
            # We will use the token from the config.json file.
            with open(constants.TOKEN_PATH) as f:
                TOKEN = json.load(f)[constants.TOKEN_NAME]

        elif TOKEN is None and os.getenv(constants.TOKEN_NAME) is not None:
            # If no token is provided, but a token is found in the environment variables.
            # We will use the token from the environment variables.
            TOKEN = os.getenv(constants.TOKEN_NAME)

        assert len(
            TOKEN
        ), f"No token provided. Please provide a token in the config.json file or in the environment variable named {constants.TOKEN_NAME}."
        self.run(TOKEN)


if __name__ == "__main__":
    fire.Fire(Client)
