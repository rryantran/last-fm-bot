import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

# Set up MongoDB connection
client = MongoClient(MONGODB_URI)
db = client['users']
collection = db['user']


def create_user(discord_id, lastfm_user, access_token, refresh_token):
    """Creates a new user in the database"""

    user = {
        "discord_id": discord_id,
        "lastfm_user": lastfm_user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    collection.insert_one(user)


def get_lastfm_user(discord_id):
    """Gets the Last.fm username for a user"""

    try:
        user = collection.find_one({"discord_id": discord_id})

        return user.get("lastfm_user")
    except:
        return None


def get_access_token(discord_id):
    """Gets the access token for a user"""

    try:
        user = collection.find_one({"discord_id": discord_id})

        return user.get("access_token")
    except:
        return ""
