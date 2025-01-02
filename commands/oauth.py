import os
from discord import Embed, Color
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FLASK_URL = os.getenv("FLASK_URL")


class OAuth(commands.Cog):
    """Cog for Spotify OAuth commands"""

    def __init__(self, bot):
        self.bot = bot
        self.flask_url = f"{FLASK_URL}/login"

    @commands.command(name="connect")
    async def connect(self, ctx):
        """Connects a user's Spotify account to the bot"""

        user_id = str(ctx.author.id)
        auth_url = f"{self.flask_url}?user_id={user_id}"

        embed = Embed(
            title="Connect your Spotify account",
            description=f"Click the following link to connect your Spotify account to the bot: [Spotify OAuth]({
                auth_url})",
            color=Color.green())

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OAuth(bot))
