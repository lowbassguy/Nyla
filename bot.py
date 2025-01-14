import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# Load environment variables from .env file
load_dotenv()  # This loads environment variables from a .env file into the environment
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieves the Discord bot token from the environment variables

# Create Flask app
app = Flask(__name__)  # Initializes a Flask web application

@app.route('/')  # Defines a route for the root URL
def home():
    return 'Bot is running!'  # Returns a simple message when the root URL is accessed

# Create a bot instance with all intents enabled
intents = discord.Intents.all()  # Enables all Discord intents for the bot
bot = commands.Bot(command_prefix='!', intents=intents)  # Creates a bot instance with a command prefix and intents

# Event: on_ready
@bot.event
async def on_ready():
    # Prints bot's login information and the guilds it is part of
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('Guilds the bot is in:')
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')
        print('  Channels:')
        for channel in guild.channels:
            print(f'  - {channel.name} (id: {channel.id})')

@bot.event
async def on_guild_join(guild):
    # Prints a message when the bot joins a new guild
    print(f'Bot joined guild: {guild.name} (id: {guild.id})')

def run_flask():
    # Runs the Flask app on all available IP addresses on port 5000
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)  # Creates a new thread to run the Flask app
    flask_thread.start()  # Starts the Flask thread
    
    # Run the bot
    bot.run(TOKEN)  # Starts the Discord bot using the token