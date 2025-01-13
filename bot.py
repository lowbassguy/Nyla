import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a bot instance with all intents enabled
intents = discord.Intents.all()  # Enable all intents to match Developer Portal
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

# Load cogs
initial_extensions = [
    # Add other cogs here as needed
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', e)

# Run the bot
bot.run(TOKEN) 