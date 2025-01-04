import os
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, redirect, request, render_template, url_for, session
from db import create_user, get_access_token

# Load environment variables
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Set up Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Set up Spotify OAuth
spotify_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read",
)


@app.route("/login")
def login():
    """Redirects user to Spotify login page"""

    # Store Discord user ID and Last.fm username in session
    session["user_id"] = request.args.get("user_id")
    session["lastfm_user"] = request.args.get("lastfm_user")

    return redirect(spotify_oauth.get_authorize_url())


@app.route("/connected")
def connected():
    """Renders the callback template"""

    return render_template("callback.html")


@app.route("/callback")
def callback():
    """Handles callback from Spotify OAuth"""

    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"

    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    })

    token_info = response.json()
    access_token = token_info.get("access_token")
    refresh_token = token_info.get("refresh_token")

    user_id = session.get("user_id")
    lastfm_user = session.get("lastfm_user")

    create_user(user_id, lastfm_user, access_token, refresh_token)

    return redirect(url_for('connected'))


@app.route("/access/<user_id>")
def access_token(user_id):
    """Returns the access token for the user or an empty string if no token is found"""

    return get_access_token(user_id)


# Run Flask app on port 3000
if __name__ == '__main__':
    app.run(port=3000)
