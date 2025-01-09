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


def create_user(discord_id, lastfm_user, token_info):
    """Creates a new user in the database"""

    existing_user = collection.find_one({"discord_id": discord_id})

    if existing_user:
        return

    user = {
        "discord_id": discord_id,
        "lastfm_user": lastfm_user,
        "token_info": token_info,
    }

    collection.insert_one(user)


def get_lastfm_user(discord_id):
    """Gets the Last.fm username for a user if it exists"""

    try:
        user = collection.find_one({"discord_id": discord_id})

        return user.get("lastfm_user")
    except:
        return None


def get_token_info(discord_id):
    """Gets token information for a user if it exists"""

    try:
        user = collection.find_one({"discord_id": discord_id})

        return user.get("token_info")
    except:
        return None
