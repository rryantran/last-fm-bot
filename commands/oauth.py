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
    async def connect(self, ctx, lastfm_user):
        """Connects a user's Spotify and Last.fm account to the bot"""

        user_id = str(ctx.author.id)
        auth_url = f"{self.flask_url}?user_id={
            user_id}&lastfm_user={lastfm_user}"

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
                description="Please provide your Last.fm username: `!connect <lastfm_user>`",
                color=Color.red())

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OAuth(bot))
