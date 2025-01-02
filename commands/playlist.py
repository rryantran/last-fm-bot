import os
from discord import Embed, Color
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FLASK_URL = os.getenv("FLASK_URL")


class Playlist(commands.Cog):
    """Cog for playlist commands"""

    def __init__(self, bot):
        self.bot = bot
        self.flask_url = f"{FLASK_URL}/access"


async def setup(bot):
    await bot.add_cog(Playlist(bot))
