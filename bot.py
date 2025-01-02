import os
import asyncio
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = Intents.default()
intents.message_content = True

# Set up commands
bot = commands.Bot(command_prefix='!', intents=intents)


async def load_cogs():
    """Loads all cogs"""

    await bot.load_extension("commands.oauth")


@bot.event
async def on_ready():
    """Prints a message when the bot is ready"""

    print(f'{bot.user.name} has connected to Discord')

if __name__ == '__main__':
    asyncio.run(load_cogs())
    bot.run(TOKEN)
