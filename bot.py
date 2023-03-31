import os

import discord
from discord.ext import tasks, commands
import responses
import scheduler



# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    # bot = commands.Bot(command_prefix='/', intents=intents)

    @tasks.loop(hours=24)
    async def update():
        # await send_message("update", scheduler.update_status(), is_private=True)
        channel = client.get_channel(1091281973441482814)
        status = scheduler.update_status()
        if status:
            await channel.send(status)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        update.start()

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
    # Remember to run your bot with your personal TOKEN
    
    client.run(os.getenv("BETTERLEB2_BOT_TOKEN"))