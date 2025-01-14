import discord
import aiosqlite
import os
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
from openai_translator import OpenAITranslator
from functools import wraps
from discord.ext import tasks
from constants import LANGUAGES

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

class TranslatorBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.members = True
        super().__init__(
            command_prefix='!',
            intents=intents
        )
        self.db = None
        self.cursor = None
        self.translator = None
        self.LANGUAGES = LANGUAGES

    async def setup_hook(self):
        await self.setup_database()
        await self.setup_translator()
        
        # Load cogs
        cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: {filename}")

        # Start the cleanup task
        self.cleanup_messages.start()
        print("Auto-deletion task has been started.")

        # Sync application commands
        await self.tree.sync()
        print("Slash commands have been synced.")

    async def setup_database(self):
        self.db = await aiosqlite.connect('translator.db')
        self.cursor = await self.db.cursor()
        
        # Create tables
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings(
                guild_id INTEGER PRIMARY KEY,
                default_language TEXT NOT NULL DEFAULT 'english',
                auto_delete_hours INTEGER NOT NULL DEFAULT 24
            )
        """)
        
        # Add auto_delete_hours column if it doesn't exist
        await self.cursor.execute("""
            SELECT COUNT(*) FROM pragma_table_info('guild_settings') WHERE name='auto_delete_hours'
        """)
        if (await self.cursor.fetchone())[0] == 0:
            await self.cursor.execute("""
                ALTER TABLE guild_settings ADD COLUMN auto_delete_hours INTEGER NOT NULL DEFAULT 24
            """)
            await self.db.commit()
        
        # Add new table for role permissions
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS authorized_roles(
                guild_id INTEGER,
                role_id INTEGER,
                PRIMARY KEY (guild_id, role_id)
            )
        """)
        
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS translation_messages(
                message_id INTEGER PRIMARY KEY,
                original_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                delete_at TIMESTAMP NOT NULL
            )
        """)
        
        await self.db.commit()

    async def setup_translator(self):
        self.translator = OpenAITranslator(os.getenv('OPENAI_API_KEY'))

    @tasks.loop(minutes=1)
    async def cleanup_messages(self):
        now = datetime.utcnow()
        try:
            await self.cursor.execute(
                "SELECT message_id, channel_id FROM translation_messages WHERE delete_at <= datetime(?)",
                (now.isoformat(),)
            )
            rows = await self.cursor.fetchall()
            
            for message_id, channel_id in rows:
                try:
                    channel = self.get_channel(channel_id)
                    if channel is None:
                        # Channel doesn't exist anymore, just remove from database
                        print(f"Channel {channel_id} no longer exists, removing associated messages from database")
                        continue
                        
                    try:
                        message = await channel.fetch_message(message_id)
                        await message.delete()
                    except discord.NotFound:
                        # Message already deleted, just continue
                        pass
                    except Exception as e:
                        print(f"Failed to delete message {message_id}: {str(e)}")
                    
                except Exception as e:
                    print(f"Error processing message {message_id}: {str(e)}")

            # Remove all processed messages from database regardless of deletion success
            await self.cursor.execute(
                "DELETE FROM translation_messages WHERE delete_at <= ?",
                (now,)
            )
            await self.db.commit()
            
        except Exception as e:
            print(f"Error in cleanup task: {e}")

    @cleanup_messages.before_loop
    async def before_cleanup_messages(self):
        await self.wait_until_ready()

    async def get_auto_delete_hours(self, guild_id: int) -> int:
        """Get guild's auto-delete duration in hours"""
        await self.cursor.execute(
            "SELECT auto_delete_hours FROM guild_settings WHERE guild_id = ?",
            (guild_id,)
        )
        result = await self.cursor.fetchone()
        return result[0] if result else 24  # Default to 24 hours if not set

bot = TranslatorBot()

if __name__ == "__main__":
    bot.run(TOKEN)
