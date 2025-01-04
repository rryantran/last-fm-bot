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
    """Create a new user in the database"""
    user = {
        "discord_id": discord_id,
        "lastfm_user": lastfm_user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    collection.insert_one(user)
