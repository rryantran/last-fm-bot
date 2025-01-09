import os
import sys
import requests
from discord import Embed, Color
from discord.ext import commands
from dotenv import load_dotenv

# Add the parent directory to the sys.path for db import
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db import get_lastfm_user
from spotify import spotify_cc, spotify_uc

# Load environment variables
load_dotenv()

FLASK_URL = os.getenv("FLASK_URL")
LASTFM_KEY = os.getenv("LASTFM_KEY")


class Playlist(commands.Cog):
    """Cog for playlist commands"""

    def __init__(self, bot):
        self.bot = bot
        self.flask_url = f"{FLASK_URL}/access"
        self.lastfm_url = "https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks"

    def get_spotify_uri(self, track, artist):
        query = f"{track} {artist}"
        response = spotify_cc.search(q=query, limit=1)
        items = response["tracks"]["items"]

        if items:
            return items[0]["uri"]

    @commands.command(name="top")
    async def top(self, ctx, limit, time_range):
        """Creates a playlist of the user's top tracks for a given time range"""

        discord_user = str(ctx.author.id)
        lastfm_user = get_lastfm_user(discord_user)
        sp = spotify_uc(discord_user)
        sp_user = sp.current_user()

        # Map the time range to the Last.fm API period
        time_range_map = {
            "alltime": "overall",
            "week": "7day",
            "month": "1month",
            "quarter": "3month",
            "half": "6month",
            "year": "12month"
        }

        mapped_time_range = time_range_map.get(time_range)

        params = {
            "user": lastfm_user,
            "api_key": LASTFM_KEY,
            "format": "json",
            "limit": limit,
            "period": mapped_time_range
        }

        # Get the user's top tracks from Last.fm
        response = requests.get(self.lastfm_url, params=params)
        data = response.json()
        track_names = [track["name"] for track in data["toptracks"]["track"]]
        artist_names = [track["artist"]["name"]
                        for track in data["toptracks"]["track"]]

        # Get the Spotify URI for each track
        uris = []
        for track, artist in zip(track_names, artist_names):
            uri = self.get_spotify_uri(track, artist)

            if uri:
                uris.append(uri)
 
        # Create a playlist on Spotify with the user's top tracks
        playlist = sp.user_playlist_create(sp_user["id"], "Top Tracks", public=True)
        playlist_id = playlist["id"]
        playlist_link = playlist["external_urls"]["spotify"]

        sp.playlist_add_items(playlist_id, uris)

        embed = Embed(
            title="Top Tracks Playlist",
            description=f"[Listen on Spotify]({playlist_link})",
            color=Color.green()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Playlist(bot))
