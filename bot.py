import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

# Create a bot instance with all intents enabled
intents = discord.Intents.all()  # Enable all intents to match Developer Portal
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('Guilds the bot is in:')
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')
        print('  Channels:')
        for channel in guild.channels:
            print(f'  - {channel.name} (id: {channel.id})')

@bot.event
async def on_guild_join(guild):
    print(f'Bot joined guild: {guild.name} (id: {guild.id})')

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Run the bot
    bot.run(TOKEN) 