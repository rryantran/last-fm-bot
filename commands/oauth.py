import os
import sys
from discord import Embed, Color
from discord.ext import commands
from dotenv import load_dotenv

# Add the parent directory to the sys.path for db import
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db import get_lastfm_user

# Load environment variables
load_dotenv()

FLASK_URL = os.getenv("FLASK_URL")


class OAuth(commands.Cog):
    """Cog for Spotify OAuth commands"""

    def __init__(self, bot):
        self.bot = bot
        self.flask_url = f"{FLASK_URL}/login"

    @commands.command(name="connect")
    async def connect(self, ctx, lastfm_user):
        """Connects a user's Spotify and Last.fm account to the bot"""

        discord_user = str(ctx.author.id)
        lastfm_user = get_lastfm_user(discord_user)
        auth_url = f"{self.flask_url}?user_id={
            discord_user}&lastfm_user={lastfm_user}"

        # Check if user is already connected
        if lastfm_user:
            embed = Embed(
                title="Error: Already Connected",
                description="You have already connected your Last.fm account",
                color=Color.red())

            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="Connect your Spotify account",
            description=f"Click the following link to connect your Spotify account to the bot: [Spotify OAuth]({
                auth_url})",
            color=Color.green())

        await ctx.send(embed=embed)

    @connect.error
    async def connect_error(self, ctx, error):
        """Handles errors for the connect command"""

        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(
                title="Error: Missing argument",
                description="Please provide your Last.fm username: `!connect <username>`",
                color=Color.red())

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OAuth(bot))
