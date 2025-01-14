import discord
import os
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

class NylaBot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        super().__init__(
            command_prefix='!',
            intents=intents
        )

    async def setup_hook(self):
        print("Bot is starting up...")
        await self.tree.sync()
        print("Commands synced")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        print("Current Guilds:")
        for guild in self.guilds:
            print(f"- {guild.name} (ID: {guild.id})")

    async def on_guild_join(self, guild):
        print(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
    async def on_guild_available(self, guild):
        print(f"Guild became available: {guild.name} (ID: {guild.id})")

bot = NylaBot()

if __name__ == "__main__":
    bot.run(TOKEN)